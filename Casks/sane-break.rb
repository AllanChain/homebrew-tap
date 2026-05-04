cask "sane-break" do
  arch arm: "arm64", intel: "x86_64"

  version "0.10.1"
  sha256 arm:   "4d7825ca4eb625ae2f911fc55859898a5693fb254a7a42c520266e0d3bc07877",
         intel: "5a61e893fec307f4025b3234c8200a38a68a4b460bff5f4dc4a5bb716827e519"

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
