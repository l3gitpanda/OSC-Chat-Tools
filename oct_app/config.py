"""Configuration and runtime state dataclasses for OCT."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AppConfig:
    version: str = "1.5.75"
    message_delay: float = 1.5
    messageString: str = ""
    FileToRead: str = ""
    scrollText: bool = False
    scrollTexTSpeed: int = 6
    hideSong: bool = False
    hideOutside: bool = True
    showPaused: bool = True
    songDisplay: str = " 🎵'{title}' ᵇʸ {artist}🎶"
    showOnChange: bool = False
    songChangeTicks: int = 1
    minimizeOnStart: bool = False
    keybind_run: str = "`"
    keybind_afk: str = "end"
    topBar: str = "╔═════════════╗"
    middleBar: str = "╠═════════════╣"
    bottomBar: str = "╚═════════════╝"
    avatarHR: bool = False
    blinkOverride: bool = False
    blinkSpeed: float = 0.5
    useAfkKeybind: bool = False
    toggleBeat: bool = True
    updatePrompt: bool = True
    confVersion: str = ""
    oscListenAddress: str = "127.0.0.1"
    oscListenPort: str = "9001"
    oscSendAddress: str = "127.0.0.1"
    oscSendPort: str = "9000"
    oscForewordAddress: str = "127.0.0.1"
    oscForewordPort: str = "9002"
    oscListen: bool = False
    oscForeword: bool = False
    logOutput: bool = False
    layoutString: str = ""
    verticalDivider: str = "〣"
    verticalDividerLeft: str = "〣"
    animateVerticalDivider: bool = False
    verticalDividerFrames: str = "〣,〢,〡,〢"
    verticalDividerLeftFrames: str = "〣,〢,〡,〢"
    cpuDisplay: str = "ᴄᴘᴜ: {cpu_percent}%"
    ramDisplay: str = "ʀᴀᴍ: {ram_percent}%  ({ram_used}/{ram_total})"
    gpuDisplay: str = "ɢᴘᴜ: {gpu_percent}%"
    hrDisplay: str = "💓 {hr}"
    playTimeDisplay: str = "⏳{hours}:{remainder_minutes}"
    mutedDisplay: str = "Muted 🔇"
    unmutedDisplay: str = "🔊"
    darkMode: bool = True
    # Text styling plugins
    textStyle: str = "none"
    flipText: bool = False
    mirrorText: bool = False
    zalgoEnabled: bool = False
    zalgoIntensity: int = 2
    kaomojiCategory: str = "random"
    textAccentFrames: str = "✧,✦,★,☆,✶,✷"
    # Interactive plugins
    eightBallDisplay: str = "🎱 {response}"
    eightBallInterval: int = 30
    diceDisplay: str = "🎲 {result}"
    diceSides: int = 6
    diceCount: int = 1
    diceInterval: int = 30
    fortuneDisplay: str = "🥠 {fortune}"
    fortuneFile: str = ""
    fortuneInterval: int = 60
    typewriterSpeed: int = 2
    cyclerMessages: str = ""
    cyclerInterval: int = 5
    reactionDisplay: str = "💜 {label}: {count}"
    reactionLabel: str = "Headpats"
    # Text formatting plugins
    borderStyle: str = "double"
    marqueeWidth: int = 20
    marqueeSpeed: int = 1
    textAlignment: str = "left"
    textAlignWidth: int = 30
    smartTruncateMax: int = 144
    animateFrames: str = "[ Loading . ],[ Loading .. ],[ Loading ... ]"
    animateSpeed: int = 1


@dataclass
class RuntimeState:
    run: bool = True
    playMsg: bool = True
    outOfDate: bool = False
    sendBlank: bool = True
    suppressDuplicates: bool = False
    sendASAP: bool = False
    useMediaManager: bool = True
    useSpotifyApi: bool = False
    spotifyAccessToken: str = ""
    spotifyRefreshToken: str = ""
    spotify_client_id: str = "915e1de141b3408eb430d25d0d39b380"
    pulsoidToken: str = ""
    usePulsoid: bool = True
    useHypeRate: bool = False
    hypeRateSessionId: str = ""
    showSongInfo: bool = True
    useTimeParameters: bool = False
    removeParenthesis: bool = False
    timerDisplay: str = "{hours}:{minutes}:{seconds}"
    timerEndStamp: int = field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    previousSongTitle: str = ""
    afk: bool = False
    hrConnected: bool = False
    heartRate: int = 0


APP_CONFIG = AppConfig()
RUNTIME_STATE = RuntimeState()
