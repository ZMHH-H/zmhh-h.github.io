#!/usr/bin/env python3
"""Install pinned, project-local tools on an Apple Silicon Mac.

Uses only Python's standard library. Python is not used to build the website.
Requires Apple's Command Line Tools (clang, make, codesign, install_name_tool).
"""

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / ".local"
DOWNLOADS = LOCAL / "downloads"
RUBY_VERSION = "3.3.11"
NODE_VERSION = "24.19.0"
BUNDLER_VERSION = "4.0.6"


def run(args, cwd=ROOT, env=None, log=None):
    print("Running:", args[0], " ".join(args[1:3]), flush=True)
    if log:
        with log.open("w") as output:
            subprocess.run(args, cwd=cwd, env=env, stdout=output, stderr=subprocess.STDOUT, check=True)
    else:
        subprocess.run(args, cwd=cwd, env=env, check=True)


def download(name, url, digest):
    path = DOWNLOADS / name
    if not path.exists():
        command = ["curl", "-fL", "--retry", "2", "--connect-timeout", "20", "--max-time", "300"]
        if url.startswith("https://ghcr.io/"):
            command += ["-H", "Authorization: Bearer QQ=="]  # Public, anonymous Homebrew bottles.
        run(command + [url, "-o", str(path)])
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise RuntimeError("Checksum mismatch; move aside and re-download: " + str(path))
    return path


def extract(archive, destination):
    destination.mkdir(parents=True, exist_ok=True)
    # Only checksum-verified archives from the pinned official URLs reach here.
    run(["tar", "-xzf", str(archive), "-C", str(destination)])


def main():
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise SystemExit("This installer targets Apple Silicon macOS. See README.md for other systems.")
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    marker = LOCAL / "environment.json"
    if marker.exists() and json.loads(marker.read_text())["project_root"] != str(ROOT):
        raise SystemExit("Project was moved. Archive .local and run setup again; do not reuse an environment from another path.")

    env = dict(os.environ)
    for key in ("RUBYLIB", "RUBYOPT", "DYLD_LIBRARY_PATH", "GEM_PATH", "BUNDLE_BIN_PATH", "BUNDLE_GEMFILE"):
        env.pop(key, None)
    sdk = Path("/Library/Developer/CommandLineTools/SDKs/MacOSX15.4.sdk")
    env["SDKROOT"] = str(sdk) if sdk.exists() else subprocess.check_output(["xcrun", "--show-sdk-path"], text=True).strip()
    env.update({
        "GEM_HOME": str(LOCAL / "gems"),
        "GEM_PATH": str(LOCAL / "gems"),
        "BUNDLE_PATH": str(LOCAL / "bundle"),
        "BUNDLE_APP_CONFIG": str(LOCAL / "bundle-config"),
        "BUNDLE_USER_HOME": str(LOCAL / "bundler-home"),
        "BUNDLE_FROZEN": "true",
        "SSL_CERT_FILE": "/etc/ssl/cert.pem",
        "npm_config_cache": str(LOCAL / "npm-cache"),
    })
    env["PATH"] = ":".join(str(LOCAL / p) for p in ("gems/bin", "ruby/bin", "node/bin")) + ":" + env["PATH"]

    ruby = LOCAL / "ruby/bin/ruby"
    if not ruby.exists():
        bottles = {
            "openssl": ("openssl/3", "0994a8029175af4578c3b93b3020e58dffa638ca21dc22d862c6bc02fea7e73b"),
            "libyaml": ("libyaml", "0ec9bf8082245c008803b42dcae3e6a0c8cd7a67aed589d9b6482b115c0a543b"),
        }
        for name, (repository, digest) in bottles.items():
            archive = download(name + ".tar.gz", "https://ghcr.io/v2/homebrew/core/" + repository + "/blobs/sha256:" + digest, digest)
            extract(archive, LOCAL / "native")
        libraries = {p.name: p for p in (LOCAL / "native").glob("*/*/lib/*.dylib") if not p.is_symlink()}
        for library in libraries.values():
            run(["install_name_tool", "-id", str(library), str(library)])
            dependencies = subprocess.check_output(["otool", "-L", str(library)], text=True)
            for line in dependencies.splitlines()[1:]:
                dependency = line.strip().split(" (", 1)[0]
                name = Path(dependency).name
                if name in libraries and dependency != str(libraries[name]):
                    run(["install_name_tool", "-change", dependency, str(libraries[name]), str(library)])
            run(["codesign", "--force", "--sign", "-", str(library)])
        archive = download("ruby-3.3.11.tar.gz", "https://cache.ruby-lang.org/pub/ruby/3.3/ruby-3.3.11.tar.gz", "59f0fafb1a59a05dc3765117af3fa68e153eb48254708549f321c1e9e078d7a0")
        extract(archive, LOCAL / "build")
        source = LOCAL / "build/ruby-3.3.11"
        run(["./configure", "--prefix=" + str(LOCAL / "ruby"), "--disable-shared", "--disable-install-doc", "--disable-yjit", "--without-gmp", "--with-openssl-dir=" + str(LOCAL / "native/openssl@3/3.6.5"), "--with-libyaml-dir=" + str(LOCAL / "native/libyaml/0.2.5")], cwd=source, env=env, log=LOCAL / "configure.log")
        run(["make", "-j6"], cwd=source, env=env, log=LOCAL / "ruby-build.log")
        run(["make", "install"], cwd=source, env=env, log=LOCAL / "ruby-install.log")

    if not (LOCAL / "node/bin/node").exists():
        archive = download("node-v24.19.0-darwin-arm64.tar.gz", "https://nodejs.org/dist/v24.19.0/node-v24.19.0-darwin-arm64.tar.gz", "8294b7aa9b03997481c06babf1e8b270c859358f27da57a11509afe537ac381d")
        extract(archive, LOCAL)
        (LOCAL / "node-v24.19.0-darwin-arm64").rename(LOCAL / "node")

    run([str(ruby), "-ropenssl", "-rpsych", "-e", "puts RUBY_DESCRIPTION; puts OpenSSL::OPENSSL_VERSION"], env=env)
    if not (LOCAL / "gems/bin/bundle").exists():
        run([str(ruby), str(LOCAL / "ruby/bin/gem"), "install", "bundler", "--version", BUNDLER_VERSION, "--no-document"], env=env)
    run([str(ruby), str(LOCAL / "gems/bin/bundle"), "install", "--jobs", "4"], env=env, log=LOCAL / "bundle-install.log")
    run([str(LOCAL / "node/bin/npm"), "ci", "--ignore-scripts", "--no-audit", "--no-fund"], env=env)
    marker.write_text(json.dumps({"project_root": str(ROOT), "ruby": RUBY_VERSION, "node": NODE_VERSION, "bundler": BUNDLER_VERSION}, indent=2) + "\n")
    print("Environment ready. Run bin/site build, bin/site check, then bin/site serve.")


if __name__ == "__main__":
    main()
