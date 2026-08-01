cask "sane-break" do
  arch arm: "arm64", intel: "x86_64"

  version "0.10.4"
  sha256 arm:   "3edd2eb617698de9394aacc211c54b58196e6e81b265045c3f3fce1e545871b0",
         intel: "715f5855f9811368010a301e5bf4e423dd9536ce8a9fae4228c581ae861a17b3"

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
