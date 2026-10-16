# frozen_string_literal: true

# Check real generated pages, internal links, and resources without fetching
# external services. This deliberately ignores external GitHub stats images.
require 'bundler/setup'
require 'nokogiri'
require 'uri'
require 'pathname'

root = Pathname.new(ARGV.fetch(0, '_site')).expand_path
required = %w[index.html news/index.html publications/index.html repositories/index.html cv/index.html]
missing = required.reject { |path| root.join(path).file? }
abort "Missing pages: #{missing.join(', ')}" unless missing.empty?

errors = []
count = 0
pages = root.glob('**/*.html')
pages.each do |file|
  document = Nokogiri::HTML(file.read)
  document.css('[href], [src], [poster]').each do |element|
    %w[href src poster].each do |attribute|
      reference = element[attribute]
      next if reference.nil? || reference.empty? || reference.start_with?('#', '//')
      next if reference.match?(/\A[a-z][a-z0-9+.-]*:/i)

      path = URI::DEFAULT_PARSER.unescape(reference.split(/[?#]/, 2).first)
      target = path.start_with?('/') ? root.join(path.delete_prefix('/')) : file.dirname.join(path)
      target = target.join('index.html') if target.directory?
      count += 1
      errors << "#{file.relative_path_from(root)}: #{reference}" unless target.file?
    end
  end
end
abort "Broken internal references:\n#{errors.uniq.join("\n")}" unless errors.empty?
puts "Checked #{pages.length} generated HTML pages and #{count} local references; all passed."
