cask "sane-break" do
  arch arm: "arm64", intel: "x86_64"

  version "0.10.6"
  sha256 arm:   "2356898a1358f0e84bd09ab9244bd1dac0bb4f3433e80cb103e76a72b5636dec",
         intel: "d05375b7a52374b7d7cd9371316a6953c1280502d6ae18a8580517dccc3d296c"

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
