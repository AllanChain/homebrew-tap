cask "sane-break" do
  arch arm: "arm64", intel: "x86_64"

  version "0.10.2"
  sha256 arm:   "bb0e7a2a60831aaa72c1221921857224cfaa06c512ee7299140d864c3923af59",
         intel: "508b1965c9839c8b8226c9cb08cb3ba617d221b14236373f037cb9b2033e06f0"

  url "https://github.com/AllanChain/sane-break/releases/download/v#{version}/sane-break-macos-#{arch}.dmg"
  name "Sane Break"
  desc "Cross-platform break reminder with a two-phase prompt and break flow"
  homepage "https://github.com/AllanChain/sane-break"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on macos: ">= :ventura"

  app "Sane Break.app"
  binary "#{appdir}/Sane Break.app/Contents/MacOS/sane-break", target: "sane-break"

  zap trash: "~/.config/SaneBreak"
end
