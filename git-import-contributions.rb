class GitImportContributions < Formula
  desc "Tool to import contributions into a Git repository from stats or other repositories"
  homepage "https://github.com/miromannino/Contributions-Importer-For-Github"
  url "https://github.com/miromannino/Contributions-Importer-For-Github/archive/refs/tags/2.0.1.tar.gz"
  sha256 "99df08c418e843c793718a8ea9de24b515e3fa3f9ea4887f5c1f609d4307ab95"
  license "MIT"

  depends_on "python@3.9"

  def install
    system "pip3", "install", "--prefix=#{prefix}", "gitpython"
    system "python3", *Language::Python.setup_install_args(prefix)
  end

  test do
    output = shell_output("#{bin}/git-import-contributions --help", 2)
    assert_match "Unified CLI for Contribution Importer", output
  end
end
