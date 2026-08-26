cask "sane-break" do
  arch arm: "arm64", intel: "x86_64"

  version "0.10.5"
  sha256 arm:   "d8e454c1802bf8659f7d3a16af00131da54c4a9c5bb09d81443e295182a2d0c6",
         intel: "19479d1965fa9edbadf5a3a7020ec083ac32ad7ca41997c5776a51f17a95c8da"

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
