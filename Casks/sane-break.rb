cask "sane-break" do
  arch arm: "arm64", intel: "x86_64"

  version "0.10.3"
  sha256 arm:   "8cb8b1af2b0439f834bb71cc0c68adaaa1ba2d0539ddb942ae80f14cf97dcf4b",
         intel: "6b4c766ca1974557206c283a3be202ca28b2ade9dda3ea5e1e255ae29c4a8355"

  url "https://github.com/AllanChain/sane-break/releases/download/v#{version}/sane-break-macos-#{arch}.dmg"
  name "Sane Break"
  desc "Cross-platform break reminder with a two-phase prompt and break flow"
  homepage "https://github.com/AllanChain/sane-break"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on macos: :ventura

  app "Sane Break.app"
  binary "#{appdir}/Sane Break.app/Contents/MacOS/sane-break", target: "sane-break"

  zap trash: "~/.config/SaneBreak"
end
