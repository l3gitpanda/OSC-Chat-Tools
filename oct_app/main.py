import os
import time
import threading
from threading import Thread, Lock
import ast
from collections import defaultdict
import ctypes
import json
#import traceback
import re
# FreeSimpleGUI removed - now using web UI
from datetime import datetime, timezone
# pythonosc, keyboard, pyperclip, asyncio, psutil, webbrowser,
# winsdk, websocket all imported lazily where used
import socket
import hashlib
import base64
#import GPUtil
# pynvml imported lazily in gpu plugin
# tendo.singleton imported lazily at startup check

from .config import APP_CONFIG, RUNTIME_STATE
from .plugins import create_default_registry

#importantest variables :)

# Legacy globals are initialized from explicit state objects for compatibility.
run = RUNTIME_STATE.run
playMsg = RUNTIME_STATE.playMsg
version = APP_CONFIG.version

#Deprecated Variables
deprecated_topTextToggle = False #Deprecated, only in use for converting old save files
deprecated_topTimeToggle = False #Deprecated, only in use for converting old save files
deprecated_topSongToggle = False #Deprecated, only in use for converting old save files
deprecated_topCPUToggle = False #Deprecated, only in use for converting old save files
deprecated_topRAMToggle = False #Deprecated, only in use for converting old save files
deprecated_topNoneToggle = True #Deprecated, only in use for converting old save files
deprecated_topHRToggle = False #Deprecated, only in use for converting old save files

deprecated_bottomHRToggle = False #Deprecated, only in use for converting old save files
deprecated_bottomTextToggle = False #Deprecated, only in use for converting old save files
deprecated_deprecated_bottomTimeToggle = False #Deprecated, only in use for converting old save files
deprecated_bottomSongToggle = False #Deprecated, only in use for converting old save files
deprecated_bottomCPUToggle = False #Deprecated, only in use for converting old save files
deprecated_bottomRAMToggle = False #Deprecated, only in use for converting old save files
deprecated_bottomNoneToggle = True #Deprecated, only in use for converting old save files

deprecated_hideMiddle = False #Deprecated, only in use for converting old save files

#conf variables
message_delay = 1.5 # in conf
messageString = '' #in conf
FileToRead = '' #in conf
scrollText = False #in conf
scrollTexTSpeed = 6
hideSong = False #in conf
hideOutside = True #in conf
showPaused = True #in conf
songDisplay = ' 🎵\'{title}\' ᵇʸ {artist}🎶' #in conf
showOnChange = False #in conf
songChangeTicks = 1 #in conf
minimizeOnStart = False #in conf
keybind_run = '`' #in conf
keybind_afk = 'end' #in conf
topBar = '╔═════════════╗' #in conf
middleBar = '╠═════════════╣' #in conf
bottomBar = '╚═════════════╝' #in conf
avatarHR = False #in conf
blinkOverride = False #in conf
blinkSpeed  = .5 #in conf
useAfkKeybind = False #in conf
toggleBeat = True #in conf
updatePrompt = True #in conf
outOfDate = False
confVersion = '' #in conf
oscListenAddress = '127.0.0.1' #in conf
oscListenPort = '9001' #in conf
oscSendAddress = '127.0.0.1' #in conf
oscSendPort = '9000' #in conf
oscForewordAddress = '127.0.0.1' #in conf
oscForewordPort = '9002' #in conf
oscListen = False #in conf
oscForeword = False #in conf
logOutput = False  #in conf
layoutString = '' #in conf
verticalDivider = "〣" #in conf
animateVerticalDivider = False #in conf
verticalDividerFrames = "〣,〢,〡,〢" #in conf
dividerFrameIndex = 0
cpuDisplay = 'ᴄᴘᴜ: {cpu_percent}%'#in conf
ramDisplay = 'ʀᴀᴍ: {ram_percent}%  ({ram_used}/{ram_total})'#in conf
gpuDisplay = 'ɢᴘᴜ: {gpu_percent}%'#in conf
hrDisplay = '💓 {hr}'#in conf
playTimeDisplay = '⏳{hours}:{remainder_minutes}'#in conf
mutedDisplay = 'Muted 🔇'#in conf
unmutedDisplay = '🔊'#in conf
darkMode = True #in conf
# New text feature globals
textStyle = 'none' #in conf
flipText = False #in conf
mirrorText = False #in conf
zalgoEnabled = False #in conf
zalgoIntensity = 2 #in conf
kaomojiCategory = 'random' #in conf
textAccentFrames = '✧,✦,★,☆,✶,✷' #in conf
eightBallDisplay = '🎱 {response}' #in conf
eightBallInterval = 30 #in conf
diceDisplay = '🎲 {result}' #in conf
diceSides = 6 #in conf
diceCount = 1 #in conf
diceInterval = 30 #in conf
fortuneDisplay = '🥠 {fortune}' #in conf
fortuneFile = '' #in conf
fortuneInterval = 60 #in conf
typewriterSpeed = 2 #in conf
cyclerMessages = '' #in conf
cyclerInterval = 5 #in conf
reactionDisplay = '💜 {label}: {count}' #in conf
reactionLabel = 'Headpats' #in conf
borderStyle = 'double' #in conf
marqueeWidth = 20 #in conf
marqueeSpeed = 1 #in conf
textAlignment = 'left' #in conf
textAlignWidth = 30 #in conf
smartTruncateMax = 144 #in conf
animateFrames = '[ Loading . ],[ Loading .. ],[ Loading ... ]' #in conf
animateSpeed = 1 #in conf
sparkleFrameIndex = 0
sendBlank = True
suppressDuplicates = False
sendASAP = False
useMediaManager = True
useSpotifyApi = False
appleMusicOnly = False
spotifySongDisplay =  '🎵\'{title}\' ᵇʸ {artist}🎶 『{song_progress}/{song_length}』'
spotifyAccessToken = ''
spotifyRefreshToken = ''
spotify_client_id = '915e1de141b3408eb430d25d0d39b380'
pulsoidToken = '' 
usePulsoid = True
useHypeRate = False
hypeRateKey = 'FIrXkWWlf57iHjMu0x3lEMNst8IDIzwUA2UD6lmSxL4BqBUTYw8LCwQlM2n5U8RU' #<- my personal token that may or may not be working depending on how the hyperate gods are feeling today
hypeRateSessionId = ''
timeDisplayAM = "{hour}:{minute} AM"
timeDisplayPM = "{hour}:{minute} PM"
showSongInfo = True
useTimeParameters = False
removeParenthesis = False
timerDisplay = "{hours}:{minutes}:{seconds}"
timerEndStamp = int(datetime.now().timestamp() * 1000)

###########Program Variables (not in conf)######### 

previousSongTitle = '' #used to prevent song title from updating when not changed to allow tooltip to appear.

current_tab = 'layout'

code_verifier = '' #for manual code entry

layoutStorage = ''

layoutUpdate = '' #making sure the code for updating the layout editor only run when needed as opposed to every .1 seconds!

output = ''

textParseIterator = 0

msgOutput = ''

afk = False

songName = ''

tickCount = 2

hrConnected = False
heartRate = 0

windowAccess = None

playTime = 0

oscForewordPortMemory = ''
oscForewordAddressMemory = ''
runForewordServer = False
oscListenPortMemory = ''
oscListenAddressMemory = ''
isListenServerRunning = False
listenServer = None
useForewordMemory = False

isAfk = False
isVR = False #Never used as the game never actually updates vrmode (well, it does *sometimes*)
isMute = False
isInSeat = False
voiceVolume = 0
isUsingEarmuffs = False
isBooped= False
isPat = False

vrcPID = None
playTimeDat = None

# vrcPID is always None at startup; playtime is calculated in vrcRunningCheck

client = None
lastSent = ''
sentTime = 0
sendSkipped = False

spotifyAuthCode = None #<- only needed for the spotify linking process (temp var)

spotify_redirect_uri = 'https://lioncat6.github.io/redirect'
spotifyLinkStatus = 'Unlinked'
cancelLink = False
spotifyPlayState = ''

pulsoidLastUsed = True
hypeRateLastUsed = False

textStorage = ""

cpu_percent = 0

spotifySongUrl = 'https://spotify.com'

nameToReturn = ''

CHATBOX_PLUGIN_REGISTRY = None

#check to see if code is already running

try:
    from tendo import singleton
    me = singleton.SingleInstance() #also me (who's single)
except Exception:
    try:
        ctypes.windll.user32.MessageBoxW(None, u"OSC Chat Tools is already running!.", u"OCT is already running!", 16)
    except (AttributeError, OSError):
        print("OSC Chat Tools is already running!")
    run = False
    os._exit(0)

def fatal_error(error = None):
  import webbrowser
  global run
  run = False
  try:
    ctypes.windll.user32.MessageBoxW(None, u"OSC Chat Tools has encountered a fatal error.", u"OCT Fatal Error", 16)
  except (AttributeError, OSError):
    print("OSC Chat Tools has encountered a fatal error.")
  if error != None:
    try:
      result = ctypes.windll.user32.MessageBoxW(None, u"The program crashed with an error message. Would you like to copy it to your clipboard?", u"OCT Fatal Error", 3 + 64)
      if result == 6:
        import pyperclip
        pyperclip.copy(str(datetime.now())+" ["+threading.current_thread().name+"] "+str(error))
    except (AttributeError, OSError):
      print(f"Error: {error}")
  try:
    result = ctypes.windll.user32.MessageBoxW(None, u"Open the github page to get support?", u"OCT Fatal Error", 3 + 64)
    if result == 6:
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/wiki/Fatal-Error-Crash')
  except (AttributeError, OSError):
    pass
  time.sleep(5)
  os._exit(0)

def afk_handler(unused_address, args):
    global isAfk
    isAfk = args
    #print('isAfk', isAfk)
    outputLog(f'isAfk {isAfk}')
    
def mute_handler(unused_address, args):
    global isMute
    isMute = args
    #print('isMute',isMute)
    outputLog(f'isMute {isMute}')
    
def inSeat_handler(unused_address, args):
    global isInSeat
    isInSeat = args
    #print('isInSeat',isInSeat)
    outputLog(f'isInSeat {isInSeat}')
    
def volume_handler(unused_address, args):
    global voiceVolume
    voiceVolume = args
    #print('voiceVolume',voiceVolume)
    #outputLog(f'voiceVolume {voiceVolume}')
def usingEarmuffs_handler(unused_address, args):
    global isUsingEarmuffs
    isUsingEarmuffs = args
    #print('isUsingEarmuffs', isUsingEarmuffs)
    outputLog(f'isUsingEarmuffs {isUsingEarmuffs}')
    
def vr_handler(unused_address, args):# The game never sends this value from what I've seen
    global isVR
    if args == 1:
        isVR = True
    else:
        isVR = False
    # This was a comparison, not an assignment, which is probably why this didn't work.
    #print('isVR', isVR)
    outputLog(f'isVR {isVR}')

"""def thread_exists(name):
    for thread in threading.enumerate():
        if thread.name == name:
            return True
    return False"""
    
def boop_handler(unused_address, args):  
    global isBooped
    isBooped = args
    outputLog(f'isBooped {isBooped}')

def pat_handler(unused_address, args):  
    global isPat
    if isinstance(args, int) or isinstance(args, float):
      if args > 0:
        isPat = True
      else:
        isPat = False
    else:
      isPat = args
    outputLog(f'isPat {isPat}') 

# message_queue and queue_lock removed - log output now handled by web module
def outputLog(text):
    from .web import web_output_log
    if logOutput:
        try:
            with open('OCT_debug_log.txt', 'a+', encoding="utf-8") as f:
                f.write("\n" + str(datetime.now()) + " [" + threading.current_thread().name + "] " + text)
        except Exception:
            pass
    web_output_log(text)

outputLog("OCT Starting...")


try:
  if not os.path.isfile('please-do-not-delete.txt'):
    with open('please-do-not-delete.txt', 'w', encoding="utf-8") as f:
        f.write('[]')
except Exception as e:
  outputLog("Failed to create settings file "+str(e))


def update_checker(a):
  pass

async def get_media_info():
    from winsdk.windows.media.control import \
        GlobalSystemMediaTransportControlsSessionManager as MediaManager
    import winsdk.windows.media.control as wmc
    sessions = await MediaManager.request_async()
    def is_apple_music_session(session):
      if session is None:
        return False
      source_id = str(session.source_app_user_model_id).lower()
      return "applemusic" in source_id or "applemusicwin" in source_id

    current_session = sessions.get_current_session()
    if appleMusicOnly and not is_apple_music_session(current_session):
      all_sessions = list(sessions.get_sessions())
      apple_sessions = [x for x in all_sessions if is_apple_music_session(x)]
      current_session = None
      for x in apple_sessions:
        if int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus["PLAYING"]) == x.get_playback_info().playback_status:
          current_session = x
          break
      if current_session is None and len(apple_sessions) > 0:
        current_session = apple_sessions[0]

    if current_session:  # there needs to be a media session running
        
        info = await current_session.try_get_media_properties_async()

        # song_attr[0] != '_' ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

    # It could be possible to select a program from a list of current
    # available ones. I just haven't implemented this here for my use case.
    # See references for more information.
    raise Exception('TARGET_PROGRAM is not the current media session')
  
async def getMediaSession():
    from winsdk.windows.media.control import \
        GlobalSystemMediaTransportControlsSessionManager as MediaManager
    sessions = await MediaManager.request_async()
    session = sessions.get_current_session()
    if appleMusicOnly and session is not None:
      source_id = str(session.source_app_user_model_id).lower()
      if "applemusic" not in source_id and "applemusicwin" not in source_id:
        apple_sessions = [x for x in list(sessions.get_sessions()) if "applemusic" in str(x.source_app_user_model_id).lower() or "applemusicwin" in str(x.source_app_user_model_id).lower()]
        session = apple_sessions[0] if len(apple_sessions) > 0 else None
    return session
_media_loop = None
_media_loop_lock = threading.Lock()

def _get_media_loop():
    global _media_loop
    if _media_loop is None or _media_loop.is_closed():
        with _media_loop_lock:
            if _media_loop is None or _media_loop.is_closed():
                import asyncio
                _media_loop = asyncio.new_event_loop()
    return _media_loop

def _run_async_media_info():
    return _get_media_loop().run_until_complete(get_media_info())

def mediaIs(state):
    import winsdk.windows.media.control as wmc
    session = _get_media_loop().run_until_complete(getMediaSession())
    if session == None:
        return False
    return int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus[state]) == session.get_playback_info().playback_status
  
confDataDict = { #this dictionary will always exclude position 0 which is the config version!
  "1.4.1" : ['confVersion', 'deprecated_topTextToggle', 'deprecated_topTimeToggle', 'deprecated_topSongToggle', 'deprecated_topCPUToggle', 'deprecated_topRAMToggle', 'deprecated_topNoneToggle', 'deprecated_bottomTextToggle', 'deprecated_deprecated_bottomTimeToggle', 'deprecated_bottomSongToggle', 'deprecated_bottomCPUToggle', 'deprecated_bottomRAMToggle', 'deprecated_bottomNoneToggle', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'deprecated_hideMiddle', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'deprecated_topHRToggle', 'deprecated_bottomHRToggle', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt'],
  "1.4.20" : ['confVersion', 'deprecated_topTextToggle', 'deprecated_topTimeToggle', 'deprecated_topSongToggle', 'deprecated_topCPUToggle', 'deprecated_topRAMToggle', 'deprecated_topNoneToggle', 'deprecated_bottomTextToggle', 'deprecated_deprecated_bottomTimeToggle', 'deprecated_bottomSongToggle', 'deprecated_bottomCPUToggle', 'deprecated_bottomRAMToggle', 'deprecated_bottomNoneToggle', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'deprecated_hideMiddle', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'deprecated_topHRToggle', 'deprecated_bottomHRToggle', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput'],
  "1.5.0" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay'],
  "1.5.1" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode'],
  "1.5.2" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode'],
  "1.5.3" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP'],
  "1.5.4" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP'],
  "1.5.5" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken'],
  "1.5.6" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId'],
  "1.5.7" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM'],
  "1.5.8" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM'],
  "1.5.8.1" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM'],
  "1.5.8.2" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM'],
  "1.5.9" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo'],
  "1.5.9.1" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo'],
  "1.5.10" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo'],
  "1.5.11" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id'],
  "1.5.12" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters'],
  "1.5.13" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters'],
  "1.5.14" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters'],
  "1.5.15" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'removeParenthesis'],
  "1.5.69.42" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'removeParenthesis', 'timerDisplay', 'timerEndStamp'],
  "1.5.70" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'removeParenthesis', 'timerDisplay', 'timerEndStamp'],
  "1.5.71" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'removeParenthesis', 'timerDisplay', 'timerEndStamp'],
  "1.5.72" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'removeParenthesis', 'timerDisplay', 'timerEndStamp'],
  "1.5.73" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'appleMusicOnly', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'removeParenthesis', 'timerDisplay', 'timerEndStamp'],
  "1.5.74" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'appleMusicOnly', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'removeParenthesis', 'timerDisplay', 'timerEndStamp', 'animateVerticalDivider', 'verticalDividerFrames'],
  "1.5.75" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'appleMusicOnly', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'removeParenthesis', 'timerDisplay', 'timerEndStamp', 'animateVerticalDivider', 'verticalDividerFrames', 'textStyle', 'flipText', 'mirrorText', 'zalgoEnabled', 'zalgoIntensity', 'kaomojiCategory', 'textAccentFrames', 'eightBallDisplay', 'eightBallInterval', 'diceDisplay', 'diceSides', 'diceCount', 'diceInterval', 'fortuneDisplay', 'fortuneFile', 'fortuneInterval', 'typewriterSpeed', 'cyclerMessages', 'cyclerInterval', 'reactionDisplay', 'reactionLabel', 'borderStyle', 'marqueeWidth', 'marqueeSpeed', 'textAlignment', 'textAlignWidth', 'smartTruncateMax', 'animateFrames', 'animateSpeed']
}

if os.path.isfile('please-do-not-delete.txt'):
  with open('please-do-not-delete.txt', 'r', encoding="utf-8") as f:
    try:
      fixed_list = ast.literal_eval(f.read())
      if type(fixed_list[0]) is str:
        confVersion = fixed_list[0]
        confLoaderIterator = 1
        if len(fixed_list) != len(confDataDict[confVersion]):
          raise Exception('Data list length mismatch')
        for i, x in enumerate(confDataDict[confVersion]):
          globals()[x] = fixed_list[i]
          #print(f"{x} = {fixed_list[i]}")
        #print("Successfully Loaded config file version "+fixed_list[0])
        outputLog("Successfully Loaded config file version "+fixed_list[0])
      else:
        #print('Config file is Too Old! Not Updating Values...')
        outputLog('Config file is Too Old! Not Updating Values...')
    except Exception as e:
      #print('Config File Load Error! Not Updating Values...')
      outputLog('Config File Load Error! Not Updating Values...\n'+str(e))
  if confVersion == "1.4.1" or confVersion ==  "1.4.20":
    outputLog("Converting old layout system, please update your config by pressing apply!")
    if deprecated_topTextToggle:
      layoutString = layoutString + '{text(0)}'
    if deprecated_topTimeToggle:
      layoutString = layoutString + '{time(0)}'
    if deprecated_topSongToggle:
      layoutString = layoutString + '{song(0)}'
    if deprecated_topCPUToggle:
      layoutString = layoutString + '{cpu(0)}'
    if deprecated_topRAMToggle:
      layoutString = layoutString + '{ram(0)}'
    if not deprecated_hideMiddle and (deprecated_topTextToggle or deprecated_topTimeToggle or deprecated_topSongToggle or deprecated_topCPUToggle or deprecated_topRAMToggle) and (deprecated_bottomTextToggle or deprecated_deprecated_bottomTimeToggle or deprecated_bottomSongToggle or deprecated_bottomCPUToggle or deprecated_bottomRAMToggle):
      layoutString = layoutString + '{div(0)}'
    if deprecated_bottomTextToggle:
      layoutString = layoutString + '{text(0)}'
    if deprecated_deprecated_bottomTimeToggle:
      layoutString = layoutString + '{time(0)}'
    if deprecated_bottomSongToggle:
      layoutString = layoutString + '{song(0)}'
    if deprecated_bottomCPUToggle:
      layoutString = layoutString + '{cpu(0)}'
    if deprecated_bottomRAMToggle:
      layoutString = layoutString + '{ram(0)}'
      
forewordServerLastUsed = oscForeword


layoutDisplayDict = {
    "playtime(" : "⌚Play Time",
    "text(" : "💬Text",
    "time(" : "🕒Time",
    "song(" : "🎵Song",
    "cpu(" : "⏱️CPU Usage",
    "ram(" : "🚦RAM Usage",
    "gpu(" : "⏳GPU Usage",
    "hr(" : "💓Heart Rate",
    "mute(" : "🔇Mute Status",
    "stt(" : "⌨Speech To Text",
    "div(" : "☵Divider",
    "timer(" : "⏲️Timer",
                      }
def layoutPreviewBuilder(layout, window=None):
  """Legacy function - layout preview is now handled in the web UI JavaScript."""
  pass
 
def refreshAccessToken(oldRefreshToken):
  import requests
  global spotifyRefreshToken
  global spotifyAccessToken
  global spotify_client_id
  token_url = 'https://accounts.spotify.com/api/token'
  data = {
      'grant_type': 'refresh_token',
      'refresh_token': oldRefreshToken,
      'client_id': spotify_client_id
    }       
  response = requests.post(token_url, data=data)
  if response.status_code != 200: 
    raise Exception('AccessToken refresh error... '+str(response.json()))
  #print(response.json())
  spotifyRefreshToken = response.json().get('refresh_token')
  spotifyAccessToken =  response.json().get('access_token')    

def getSpotifyPlaystate():
  import requests
  global spotifySongUrl
  global spotifyRefreshToken
  global spotifyAccessToken
  
  def get_playstate(accessToken):
    global spotifyRefreshToken
    global spotifyAccessToken
    #print(spotifyAccessToken)
    #print(accessToken)
    headers = {
        'Authorization': 'Bearer ' + accessToken,
    }

    response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
    if response.status_code == 204:
      data = ''
    else:
      data = response.json()
    return data
  try:
      playState = get_playstate(spotifyAccessToken)
      if playState != '' and playState != None:
        if 'error' in str(playState):
          raise Exception(str(playState))
  except Exception as e:
      if "expired" in str(e):
        outputLog("Attempting to regenerate outdated access token...\nReason: "+str(e))
        refreshAccessToken(spotifyRefreshToken)
        # Config auto-saved via web API on apply
        playState = get_playstate(spotifyAccessToken) 
      else:
        outputLog("Spotify connection error... retrying\nFull Error: "+str(e))
        playState = get_playstate(spotifyAccessToken) 
  if playState == None:
    playState = ''
  return playState
def loadSpotifyTokens():
  import requests
  global spotifyLinkStatus
  outputLog("Loading spotify tokens...")
  def get_profile(accessToken):
      headers = {
          'Authorization': 'Bearer ' + accessToken,
      }
      response = requests.get('https://api.spotify.com/v1/me', headers=headers)
      data = response.json()
      if response.status_code != 200:
        raise Exception(response.json())
      return data
  try:
    outputLog("Trying old access token...")
    profile = get_profile(spotifyAccessToken)
  except Exception as e:
    outputLog("Attempting to regenerate outdated access token...\nReason: "+str(e))
    refreshAccessToken(spotifyRefreshToken)    
    profile = get_profile(spotifyAccessToken)
  linkedUserName = profile.get('display_name')  
  outputLog("Spotify linked to "+linkedUserName+" successfully!")
  spotifyLinkStatus = 'Linked to '+linkedUserName  
def _load_spotify_tokens_background():
  global spotifyLinkStatus
  global spotifyAccessToken
  global spotifyRefreshToken
  try:
    if spotifyAccessToken != '' and spotifyAccessToken != None:
      loadSpotifyTokens()
  except Exception as e:
    if "timed out" in str(e):
      outputLog('Spotify API Timed out... tokens may be invalid\nFull Error: '+str(e))
      spotifyLinkStatus = 'Status Unknown'
    elif "Max retries" in str(e) or "aborted" in str(e):
      outputLog('Spotify API connection error... tokens may be invalid. Are you connected to the internet?\nFull Error: '+str(e))
      spotifyLinkStatus = 'Status Unknown'
    else:
      spotifyLinkStatus = 'Error - Please Relink!'
      spotifyAccessToken = ''
      spotifyRefreshToken = ''
      outputLog("Spotify token load error! Please relink!\nFull Error: "+str(e))
def uiThread():
  """Start the web UI server. Replaces the old FreeSimpleGUI-based UI."""
  import webbrowser
  from .web import create_app, socketio, start_update_thread, get_log_history
  from . import main as m

  app = create_app()
  start_update_thread(m)

  # Auto-open browser
  def open_browser():
    import time as t
    t.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')
  Thread(target=open_browser, daemon=True).start()

  outputLog("Web UI starting on http://127.0.0.1:5000")
  try:
    socketio.run(app, host='127.0.0.1', port=5000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
  except Exception as e:
    outputLog(f"Web server error: {e}")
  finally:
    global playMsg, run
    playMsg = False
    run = False
    try:
      listenServer.shutdown()
      listenServer.server_close()
    except Exception:
      pass
    if logOutput:
      with open('OCT_debug_log.txt', 'a+', encoding="utf-8") as f:
        f.write("\n" + str(datetime.now()) + " OCT Shutting down...")
    os._exit(0)


# The old uiThread code (FreeSimpleGUI) has been removed.
# All UI is now served via Flask + SocketIO (see oct_app/web.py).

def _legacy_uiThread_removed():
  """Placeholder - the old FreeSimpleGUI-based UI has been replaced with a web UI.
  See oct_app/web.py, oct_app/templates/index.html, and oct_app/static/app.js."""
  pass
def processMessage(a):
  returnList = []
  if messageString.count('\n')>0:
    posForLoop = 0
    for x in range(messageString.count('\n')):
      returnList.append(messageString[posForLoop:messageString.find('\n', posForLoop+1)].replace('\n', ''))
      posForLoop = messageString.find('\n', posForLoop+1)
    returnList.append(messageString[posForLoop:len(messageString)].replace('\n', ''))
  else:
    returnList.append(messageString)
  return returnList

def oscClientDef():
  from pythonosc import udp_client
  global client
  _last_address = None
  _last_port = None
  while run:
    try:
      port = int(oscSendPort)
    except (TypeError, ValueError):
      outputLog(f"Invalid OSC send port '{oscSendPort}', falling back to 9000")
      port = 9000
    current_address = str(oscSendAddress)
    if current_address != _last_address or port != _last_port:
      try:
        client = udp_client.SimpleUDPClient(current_address, port)
        _last_address = current_address
        _last_port = port
      except Exception as e:
        outputLog(f"Failed to initialize OSC client: {e}")
    time.sleep(.5)

dispatcher = None

def oscForwardingManager():
  global runForewordServer
  global oscListenAddressMemory
  global oscListenPortMemory
  global oscForewordAddressMemory
  global oscForewordPortMemory
  global oscForeword
  global oscListen
  global useForewordMemory
  # windowAccess removed (web UI)
  time.sleep(.5)
  listen_socket = None
  forward_sockets = []
  while run:
      global runForewordServer
      global oscListenAddressMemory
      global oscListenPortMemory
      global oscForewordAddressMemory
      global oscForewordPortMemory
      global oscForeword
      global oscListen
      global useForewordMemory
      # windowAccess removed (web UI)
      # Create a socket to listen for incoming data
      def create_sockets():
          nonlocal listen_socket
          global runForewordServer
          global oscListenAddressMemory
          global oscListenPortMemory
          global oscForewordAddressMemory
          global oscForewordPortMemory
          global oscForeword
          global oscListen
          global useForewordMemory
          # windowAccess removed (web UI)
          try:
              listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
              listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
              listen_socket.bind((oscListenAddress, int(oscListenPort)))
              listen_socket.settimeout(.5)
          except Exception as err:
              outputLog(f'OSC Listen Error: {err}')
              oscListen = False
              oscForeword = False

      # Set the IP addresses and port numbers to forward data to
      if oscForeword:
          forward_addresses = [
              ('127.0.0.1', 61394), #for the listen server
              (oscForewordAddress, int(oscForewordPort)),
          ]
      else:
          forward_addresses = [
              ('127.0.0.1', 61394) #for the listen server
          ]

      def dataSender():
          global runForewordServer
          global oscListenAddressMemory
          global oscListenPortMemory
          global oscForewordAddressMemory
          global oscForewordPortMemory
          global oscForeword
          global oscListen
          global useForewordMemory
          # windowAccess removed (web UI)
          nonlocal forward_sockets
          runForewordServer = True
          #print('Starting Forwarding server on '+str(forward_addresses))
          create_sockets()
          outputLog('Starting Forwarding server on '+str(forward_addresses))
          oscListenAddressMemory = oscListenAddress
          oscListenPortMemory = oscListenPort
          oscForewordPortMemory = oscForewordPort
          oscForewordAddressMemory = oscForewordAddress
          useForewordMemory = oscForeword
          forward_sockets = [
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for _ in forward_addresses
          ]
          while run and runForewordServer:
              try:
                  data, addr = listen_socket.recvfrom(1024)

                  # Forward the data to each forward socket
                  if 'Contact' in str(data):
                    print(data)
                  for forward_socket, (ip, port) in zip(forward_sockets, forward_addresses):
                      forward_socket.sendto(data, (ip, port))
              except Exception as e:
                time.sleep(.01)
                pass


      if oscForeword:
          if not runForewordServer:
            if forewordServerLastUsed != oscForeword:
              outputLog("Foreword Server Toggled On... Waiting For Listen Server To Change Ports...")
              time.sleep(3)
            else:
              dataSenderThread = Thread(target=dataSender)
              dataSenderThread.start()
      time.sleep(.1)
      if oscListenAddressMemory != oscListenAddress or oscListenPortMemory != oscListenPort or oscForewordPortMemory != oscForewordPort or oscForewordAddressMemory != oscForewordAddress or useForewordMemory != oscForeword or useForewordMemory != oscForeword:
          if oscForeword:
              #print('Foreword/Listen Server Config Updated, Restarting Forwarding Server...\n')
              outputLog('Foreword/Listen Server Config Updated, Restarting Forwarding Server...\n')
              runForewordServer = False
              time.sleep(.5)
              if not runForewordServer:
                  dataSenderThread = Thread(target=dataSender)
                  dataSenderThread.start()
      if runForewordServer and not(oscForeword):
          if listen_socket is not None:
              listen_socket.close()
          for forward_socket in forward_sockets:
              forward_socket.close()
          runForewordServer = False
          #print('No OSC Foreword/Listening Options are selected, stopping Forwarding Server...')
          outputLog('No OSC Foreword/Listening Options are selected, stopping Forwarding Server...')
      time.sleep(.5)

  # Close all sockets on shutdown
  if listen_socket is not None:
      listen_socket.close()
  for forward_socket in forward_sockets:
      forward_socket.close()
def oscListenServerManager():
    from pythonosc import osc_server
    global oscListenAddress
    global oscListenPort
    global oscListen
    global isListenServerRunning
    global forewordServerLastUsed
    while run:
        if oscListen:
            if oscForeword:
              listen_ip = '127.0.0.1'
              listen_port = 61394
            else:
              listen_ip = oscListenAddress
              try:
                listen_port = int(oscListenPort)
              except (TypeError, ValueError):
                listen_port = 9001
            def listenServerThread():
                global isListenServerRunning
                global oscListenAddress
                global oscListenPort
                global listenServer
                try:
                    if oscForeword:
                      location = "127.0.0.1:61394"
                    else:
                      location = f"{str(oscListenAddress)}:{str(oscListenPort)}"
                    outputLog('Attempting To Start Listen Server on '+location)
                    listenServer = osc_server.ThreadingOSCUDPServer(
                        (listen_ip, listen_port), dispatcher)
                    #print("Osc Listen Server Serving on {}".format(listenServer.server_address))
                    outputLog("Osc Listen Server Serving on {}".format(listenServer.server_address))
                    sockett = listenServer.socket
                    sockett.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                    isListenServerRunning = True

                    listenServer.serve_forever()
                except Exception as e:
                    #print('Osc Listen Server Failed to Start, Retying...'+str(e))
                    outputLog(f'Osc Listen Server Failed to Start, Retying...\nPlease make sure another program isn\'t using {location}\n'+str(e))
                    pass

            if not isListenServerRunning:
                oscServerThread = Thread(target=listenServerThread)
                oscServerThread.start()
        if not oscListen and isListenServerRunning:
          #print('No OSC Listen Options are Selected, Shutting Down OSC Listen Server...')
          outputLog('No OSC Listen Options are Selected, Shutting Down OSC Listen Server...')
          isListenServerRunning = False
          listenServer.shutdown()
          listenServer.server_close()
        if oscForeword != forewordServerLastUsed  and isListenServerRunning:
          outputLog('Foreword Server Toggled, Restarting Listen Server...')
          isListenServerRunning = False
          try:
            listenServer.shutdown()
            listenServer.server_close()
          except:
            pass
          forewordServerLastUsed = oscForeword
        time.sleep(.5)


_BORDER_STYLES = {
    "double":  ("╔═════════════╗", "╠═════════════╣", "╚═════════════╝"),
    "rounded": ("╭─────────────╮", "├─────────────┤", "╰─────────────╯"),
    "light":   ("┌─────────────┐", "├─────────────┤", "└─────────────┘"),
    "heavy":   ("┏━━━━━━━━━━━━━┓", "┣━━━━━━━━━━━━━┫", "┗━━━━━━━━━━━━━┛"),
    "fancy":   ("♢═════════════♢", "◈═════════════◈", "♢═════════════♢"),
    "ascii":   ("+-------------+", "+-------------+", "+-------------+"),
}


def _apply_border_style():
    global topBar, middleBar, bottomBar, borderStyle
    if borderStyle in _BORDER_STYLES:
        topBar, middleBar, bottomBar = _BORDER_STYLES[borderStyle]


def sendMsg(a):
    global msgOutput
    global message_delay
    global messageString
    global playMsg
    global run
    global songName
    global songDisplay
    global songChangeTicks
    global tickCount
    global topBar
    global middleBar
    global bottomBar
    global pulsoidToken
    global avatarHR
    global blinkOverride
    global blinkSpeed
    global useAfkKeybind
    global toggleBeat
    global layoutString
    global verticalDivider
    global animateVerticalDivider
    global verticalDividerFrames
    global dividerFrameIndex
    global cpuDisplay
    global ramDisplay
    global gpuDisplay
    global hrDisplay
    global playTimeDisplay
    global mutedDisplay
    global unmutedDisplay
    global playTimeDat
    global timeDisplayAM
    global timeDisplayPM
    # New text feature globals
    global textStyle
    global flipText
    global mirrorText
    global zalgoEnabled
    global zalgoIntensity
    global kaomojiCategory
    global textAccentFrames
    global eightBallDisplay
    global eightBallInterval
    global diceDisplay
    global diceSides
    global diceCount
    global diceInterval
    global fortuneDisplay
    global fortuneFile
    global fortuneInterval
    global typewriterSpeed
    global cyclerMessages
    global cyclerInterval
    global reactionDisplay
    global reactionLabel
    global borderStyle
    global marqueeWidth
    global marqueeSpeed
    global textAlignment
    global textAlignWidth
    global smartTruncateMax
    global animateFrames
    global animateSpeed
    global sparkleFrameIndex
    #stupid crap
    global letsGetThatTime
    global songInfo
    global cpuDat
    global ramDat
    global hrInfo
    global gpuDat
    global lastSent
    global sentTime
    global sendSkipped
    #end of stupid crap
    global timeVar
    try:
     timeVar = time.time()
     _apply_border_style()
     if playMsg:
      #message Assembler:
      if not scrollText and not afk:
        
        def msgGen(a):
          global verticalDivider
          global animateVerticalDivider
          global verticalDividerFrames
          global dividerFrameIndex
          global msgOutput
          global spotifySongUrl
          global songName
          global tickCount
          global timerEndStamp
          global timerVar

          if animateVerticalDivider:
            frames = [f.strip() for f in verticalDividerFrames.split(',') if f.strip()]
            if frames:
              currentDivider = frames[dividerFrameIndex % len(frames)]
              dividerFrameIndex = (dividerFrameIndex + 1) % len(frames)
            else:
              currentDivider = verticalDivider
          else:
            currentDivider = verticalDivider

          def checkData(msg, data):
            lf = "\v"
            if data == 1 or data == 3:
              msg = msg + " " + currentDivider
            if data == 2 or data == 3:
              msg = msg + lf
            return msg

          plugin_context = {
            "check_data": checkData,
            "vertical_divider": currentDivider,
            "middle_bar": middleBar,
            "muted_display": mutedDisplay,
            "unmuted_display": unmutedDisplay,
            "is_muted": isMute,
            "time_display_am": timeDisplayAM,
            "time_display_pm": timeDisplayPM,
            "timer_display": timerDisplay,
            "timer_end_stamp": timerEndStamp,
            "song_display": songDisplay,
            "spotify_song_display": spotifySongDisplay,
            "show_paused": showPaused,
            "hide_song": hideSong,
            "show_on_change": showOnChange,
            "song_change_ticks": songChangeTicks,
            "song_name": songName,
            "tick_count": tickCount,
            "use_media_manager": useMediaManager,
            "use_spotify_api": useSpotifyApi,
            "spotify_play_state": spotifyPlayState,
            "remove_parenthesis": removeParenthesis,
            "window_access": None,
            "output_log": outputLog,
            "get_media_info": _run_async_media_info,
            "media_is": mediaIs,
            "cpu_display": cpuDisplay,
            "ram_display": ramDisplay,
            "gpu_display": gpuDisplay,
            "hr_display": hrDisplay,
            "heart_rate": heartRate,
            "play_time_display": playTimeDisplay,
            "time_var": timeVar,
            "play_time_dat": playTimeDat,
            "vrc_pid": vrcPID,
            "song_info": '',
            "spotify_song_url": spotifySongUrl,
            # New text feature context
            "text_style": textStyle,
            "flip_text": flipText,
            "mirror_text": mirrorText,
            "zalgo_enabled": zalgoEnabled,
            "zalgo_intensity": zalgoIntensity,
            "kaomoji_category": kaomojiCategory,
            "text_accent_frames": textAccentFrames,
            "sparkle_frame_index": sparkleFrameIndex,
            "eightball_display": eightBallDisplay,
            "eightball_interval": eightBallInterval,
            "dice_display": diceDisplay,
            "dice_sides": diceSides,
            "dice_count": diceCount,
            "dice_interval": diceInterval,
            "fortune_display": fortuneDisplay,
            "fortune_file": fortuneFile,
            "fortune_interval": fortuneInterval,
            "typewriter_speed": typewriterSpeed,
            "cycler_messages": cyclerMessages,
            "cycler_interval": cyclerInterval,
            "reaction_display": reactionDisplay,
            "reaction_label": reactionLabel,
            "marquee_width": marqueeWidth,
            "marquee_speed": marqueeSpeed,
            "text_alignment": textAlignment,
            "text_align_width": textAlignWidth,
            "smart_truncate_max": smartTruncateMax,
            "animate_frames": animateFrames,
            "animate_speed": animateSpeed,
          }

          text = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("text", plugin_context, a, data)
          time = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("time", plugin_context, a, data)
          timer = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("timer", plugin_context, a, data)
          song = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("song", plugin_context, a, data)
          cpu = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("cpu", plugin_context, a, data)
          ram = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("ram", plugin_context, a, data)
          gpu = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("gpu", plugin_context, a, data)
          hr = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("hr", plugin_context, a, data)
          stt = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("stt", plugin_context, a, data)
          div = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("div", plugin_context, a, data)
          mute = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("mute", plugin_context, a, data)
          playtime = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("playtime", plugin_context, a, data)
          textstyle = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("textstyle", plugin_context, a, data)
          fliptext = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("fliptext", plugin_context, a, data)
          zalgo = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("zalgo", plugin_context, a, data)
          kaomoji = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("kaomoji", plugin_context, a, data)
          sparkle = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("sparkle", plugin_context, a, data)
          eightball = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("8ball", plugin_context, a, data)
          dice = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("dice", plugin_context, a, data)
          fortune = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("fortune", plugin_context, a, data)
          typewriter = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("typewriter", plugin_context, a, data)
          cycler = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("cycler", plugin_context, a, data)
          reaction = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("reaction", plugin_context, a, data)
          marquee = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("marquee", plugin_context, a, data)
          textalign = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("textalign", plugin_context, a, data)
          smarttruncate = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("smarttruncate", plugin_context, a, data)
          animate = lambda data=0: CHATBOX_PLUGIN_REGISTRY.render("animate", plugin_context, a, data)

          try:
            msgOutput = eval("f'"f'{layoutString}'"'")
          except Exception as e:
            msgOutput = "Layout Error!\v"+str(e)

          timerEndStamp = plugin_context["timer_end_stamp"]
          timerVar = plugin_context.get("timer_var", 0)
          songName = plugin_context["song_name"]
          tickCount = plugin_context["tick_count"]
          spotifySongUrl = plugin_context["spotify_song_url"]
          sparkleFrameIndex = plugin_context.get("sparkle_frame_index", 0)

          if msgOutput[-len(currentDivider+" "): ] == currentDivider+" ":
            msgOutput = msgOutput[:-len(currentDivider+" ")-1]
          if msgOutput[-len(middleBar+" "): ] == middleBar+" ":
            msgOutput = msgOutput[:-len(middleBar+" ")]
          if "\v " in msgOutput[-2:]:
            msgOutput = msgOutput[:-2]
          if "\v" in msgOutput[-2:]:
            msgOutput = msgOutput[:-1]
          if not hideOutside:
            msgOutput = topBar + " " + msgOutput + " " + bottomBar
          msgOutput = msgOutput.replace("\\n", "\v").replace("\\v", "\v")
        msgGen(a)
      elif afk:
        msgOutput = topBar+a+bottomBar
      else:
        msgOutput = a
      if playMsg:
        if (str(msgOutput) != lastSent) or (not suppressDuplicates) or sentTime > 30:
          try:
            global client
            if client is None:
              try:
                _port = int(oscSendPort)
              except (TypeError, ValueError):
                _port = 9000
              from pythonosc import udp_client
              client = udp_client.SimpleUDPClient(str(oscSendAddress), _port)
              outputLog(f"OSC client created inline: {oscSendAddress}:{_port}")
            client.send_message("/chatbox/input", [ str(msgOutput), True, False])
            lastSent = str(msgOutput)
            sentTime = 0
            sendSkipped = False
          except Exception as e:
            outputLog(f"OSC send error: {e}")
        else:
          sendSkipped = True
      msgDelayMemory = message_delay
      for x in range(int(message_delay*10)):
        if not playMsg or not run or ((msgDelayMemory != message_delay) and sendASAP) or sendSkipped == True:
          break
        time.sleep(.1)
    except Exception as e:
     outputLog(f"sendMsg error: {e}")

def timeParameterUpdate():
  while run:
    global useTimeParameters
    if useTimeParameters:
      now = datetime.now()
      hour = now.strftime("%H")
      minute = now.strftime("%M")
      second = now.strftime("%S")
      isPm = False
      if int(hour) >= 12:
          hour = int(hour)-12
          isPm = True
          if int(hour) == 0:
            hour = 12
      else:
          if int(hour) == 0:
            hour = 12  
          isPm = False
      try:
        client.send_message("/avatar/parameters/Hours", int(hour))
        client.send_message("/avatar/parameters/Minutes", int(minute))
        client.send_message("/avatar/parameters/Seconds", int(second))
        client.send_message("/avatar/parameters/Period", isPm)
      except Exception as e:
        outputLog("Error sending time parameters:\n"+str(e))
    time.sleep(1)



def hrConnectionThread():
  from websocket import create_connection
  while run:
    global hrConnected
    global heartRate
    global pulsoidToken
    global client
    global blinkOverride
    global blinkSpeed
    global useAfkKeybind
    global toggleBeat
    global ws
    global pulsoidLastUsed
    global hypeRateLastUsed
    if ("hr(" in layoutString or avatarHR) and (playMsg or avatarHR):
      if not hrConnected:
        try:
          url = "wss://dev.pulsoid.net/api/v1/data/real_time?access_token="+pulsoidToken+"&response_mode=text_plain_only_heart_rate"
          if useHypeRate:
            url = "wss://app.hyperate.io/socket/websocket?token="+hypeRateKey
          ws = create_connection(url)
          ws.settimeout(.4)
          hrConnected = True
          def heartRateListen():
              global ws
              global heartRate
              global pulsoidLastUsed
              global hypeRateLastUsed
              global hrConnected
              join_msg = {
                    "topic": "hr:"+hypeRateSessionId,  # replace <ID> with the user session id
                    "event": "phx_join",
                    "payload": {},
                    "ref": 0
                }
              if useHypeRate:
                ws.send(json.dumps(join_msg))
              while run:
                  try:
                    event = ws.recv()
                    if usePulsoid:
                      heartRate = event
                    else:
                      try:
                        heartRate = json.loads(event).get('payload').get('hr')
                        if heartRate == None:
                          heartRate = 1
                      except Exception as e:
                        outputLog('Refreshing hyperate...')
                        try:
                          ws.close()
                        except Exception:
                          pass
                        ws = create_connection(url)
                        ws.send(json.dumps(join_msg))
                    client.send_message("/avatar/parameters/isHRActive", True)
                    client.send_message("/avatar/parameters/isHRConnected", True)
                    client.send_message("/avatar/parameters/HR", int(heartRate))
                    
                  except Exception as e:
                    if not 'Connection timed out' in str(e):
                      outputLog(str(e))
                      hrConnected = False
                      try:
                        ws.close()
                      except Exception:
                        pass
                      break
                    pass
                    time.sleep(.01)
                  if not run or not hrConnected:
                      try:
                        ws.close()
                      except Exception:
                        pass
                      break
          heartRateListenThread = Thread(target=heartRateListen)
          heartRateListenThread.start()
          def blinkHR():
            global blinkThread
            global heartRate
            global blinkOverride
            global blinkSpeed
            global toggleBeat
            while hrConnected and run and (playMsg or avatarHR):
              if toggleBeat:
                client.send_message("/avatar/parameters/isHRBeat", True)
                time.sleep(.1)
                client.send_message("/avatar/parameters/isHRBeat", False)
                if blinkOverride:
                  time.sleep(blinkSpeed)
                try:
                  hr_val = int(heartRate) if heartRate else 0
                except (ValueError, TypeError):
                  hr_val = 0
                if hr_val <= 0:
                  heartRate = 1
                  hr_val = 1
                if 60 / hr_val > 5:
                  time.sleep(1)
                else:
                  time.sleep(60 / hr_val)
          blinkHRThread = Thread(target=blinkHR)
          blinkHRThread.start()
          #print('Pulsoid Connection Started...')
          if usePulsoid:
            outputLog('Heart Rate Connection Started... Connected to Pulsoid')
            pulsoidLastUsed = True
            hypeRateLastUsed = False
          else:
            outputLog('Heart Rate Connection Started... Connected to HypeRate')
            pulsoidLastUsed = False
            hypeRateLastUsed = True
        except Exception as e:
          if playMsg:
              outputLog(f'Heart Rate Error: {e}')
    if (((not "hr(" in layoutString and not avatarHR) or not (playMsg or avatarHR)) or (pulsoidLastUsed and useHypeRate) or (hypeRateLastUsed and usePulsoid)) and hrConnected:
      hrConnected = False
      #print('Pulsoid Connection Stopped')
      if (pulsoidLastUsed and useHypeRate) or (hypeRateLastUsed and usePulsoid):
        outputLog('Switching HR Data source...')
      heartRate = 0
      if pulsoidLastUsed:
        outputLog('Pulsoid Connection Stopped')
      else:
        outputLog('HypeRate Connection Stopped')
    time.sleep(.5)
pulsoidLastUsed = usePulsoid
hypeRateLastUsed = useHypeRate
pulsoidConnectionThread = Thread(target=hrConnectionThread).start()

def spotifyConnectionManager():
  global spotifyPlayState
  while run:
    if playMsg and "song(" in layoutString and useSpotifyApi:
      try:
        if spotifyAccessToken == '':
          raise Exception('Spotify access token missing!\nCheck output tab for more details...')
        spotifyPlayState = getSpotifyPlaystate()
      except Exception as e:  
        if "timed out" in str(e): 
          outputLog('Spotify API Timed out... retrying in 5 seconds\nFull Error: '+str(e))
          time.sleep(5)
        elif "Max retries" in str(e) or "aborted" in str(e):
          outputLog('Spotify API Timed out... retrying in 5 seconds\nFull Error: '+str(e))
          time.sleep(5)
        else: 
          spotifyPlayState = ''
          outputLog(f'Spotify API Error: {e}') 
    for x in range(2): #This sets the polling rate of the spotify api!!! Value is seconds minus 1, so a timeout of 3 seconds would be 2
      if run:
        time.sleep(1)
spotifyConnectionThread = Thread(target=spotifyConnectionManager).start()
def linkSpotify():
  import requests
  from flask import Flask, request
  from werkzeug.serving import make_server
  outputLog('Begin Spotify Linking...')
  global spotify_client_id
  global spotify_redirect_uri
  global checkForCancel
  global NameToReturn
  global spotifyAccessToken
  global spotifyRefreshToken
  global code_verifier
  
  code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
  code_verifier = code_verifier.rstrip('=')

  code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
  code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
  code_challenge = code_challenge.replace('=', '')

  auth_url = 'https://accounts.spotify.com/authorize'
  params = {
      'client_id': spotify_client_id,
      'response_type': 'code',
      'scope': "user-read-playback-state, user-read-currently-playing",
      'redirect_uri': spotify_redirect_uri,
      'code_challenge_method': 'S256',
      'code_challenge': code_challenge
  }
  spotify_auth_url = requests.Request('GET', auth_url, params=params).prepare().url
  
  outputLog("Attempting to open url: \n"+spotify_auth_url)
  
  app = Flask(__name__)
  server = make_server('127.0.0.1', 8000, app)
  
  @app.route('/callback')


  def callback():
      global authCode
      global spotifyAccessToken
      global spotifyRefreshToken
      global checkForCancel
      global nameToReturn
      global cancelLink
      def shutdown():
        server.shutdown()
      if 'error' in request.args:
        outputLog('Spotify Link Error: '+str(request.args.get('error')))
        shutdownThread = Thread(target=shutdown).start()
        cancelLink = True
        nameToReturn = 'Error'
        return """<!DOCTYPE html> <html> <head> <title>OSC Chat Tools | Spotify Authorization</title> <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> </head> <body> <style> body { font-family: sans-serif; background-color: darkslategrey; color: whitesmoke; } .mainbox { position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%); } h1 { text-align: center; } p { text-align: center; } img { display: block; margin-left: auto; margin-right: auto; width: 50%; } </style> <div class="mainbox"> <img src="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> <h1 class="maintext">Authorization Failed</h1><p class="subtext">If you did not cancel the authentication at the previous screen please submit a bug report at <a href='https://github.com/Lioncat6/OSC-Chat-Tools/issues'>https://github.com/Lioncat6/OSC-Chat-Tools/issues</a></p><div><p>Full error:<b style="color:red;"> """+str(request.args.get('error'))+""" </b></p></div> </div> </body> </html>"""
      try:   
        code = request.args.get('code')
        #print('Authorization code:', code)
        authCode = code 
        def getAccessToken(code):
            global spotifyRefreshToken
            token_url = 'https://accounts.spotify.com/api/token'
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': spotify_redirect_uri,
                'client_id': spotify_client_id,      
                'code_verifier': code_verifier
            }
            response = requests.post(token_url, data=data)
            if response.status_code != 200:
              raise Exception('Access token fetch error '+str(response.status_code)+' : '+response.text)
            spotifyRefreshToken = response.json().get('refresh_token')
            return response.json().get('access_token')

        spotifyAccessToken = getAccessToken(code)
        #print('Access token:', accessToken)
        
        def get_profile(accessToken):
            headers = {
                'Authorization': 'Bearer ' + accessToken,
            }

            response = requests.get('https://api.spotify.com/v1/me', headers=headers)
            if response.status_code != 200:
              raise Exception('Profile fetch error '+str(response.status_code)+' : '+response.text)
            data = response.json()
            return data
        profile = get_profile(spotifyAccessToken)
        shutdownThread = Thread(target=shutdown).start()
        nameToReturn = profile.get('display_name')
        outputLog("Spotify linked to "+nameToReturn+" successfully!")
        return """<!DOCTYPE html> <html> <head> <title>OSC Chat Tools | Spotify Authorization</title> <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> </head> <body> <style> body { font-family: sans-serif; background-color: darkslategrey; color: whitesmoke; } .mainbox { position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%); } h1 { text-align: center; } p { text-align: center; } img { display: block; margin-left: auto; margin-right: auto; width: 50%; } </style> <div class="mainbox"> <img src="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> <h1 class="maintext">Authorization Successful</h1><p class="subtext">You can now close this tab and return to OCT</p> <div><p>Linked to:<b style="color:green;"> """+profile.get('display_name')+""" </b></p></div> </div> </body> </html>"""
      except Exception as e:
        shutdownThread = Thread(target=shutdown).start()
        cancelLink = True
        nameToReturn = 'Error'
        outputLog('Spotify Link Error: '+str(e))
        return """<!DOCTYPE html> <html> <head> <title>OSC Chat Tools | Spotify Authorization</title> <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> </head> <body> <style> body { font-family: sans-serif; background-color: darkslategrey; color: whitesmoke; } .mainbox { position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%); } h1 { text-align: center; } p { text-align: center; } img { display: block; margin-left: auto; margin-right: auto; width: 50%; } </style> <div class="mainbox"> <img src="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> <h1 class="maintext">Authorization Failed</h1><p class="subtext">If you did not cancel the authentication at the previous screen please submit a bug report at <a href='https://github.com/Lioncat6/OSC-Chat-Tools/issues'>https://github.com/Lioncat6/OSC-Chat-Tools/issues</a></p><div><p>Full error:<b style="color:red;"> """+str(e)+""" </b></p></div> </div> </body> </html>"""
  
  webbrowser.open_new(spotify_auth_url)
  
  def spotifyLinkCancelCheck():
    global checkForCancel
    checkForCancel = True
    global cancelLink
    global nameToReturn
    while checkForCancel:
      time.sleep(.1)
      if cancelLink:
        outputLog("Spotify linking canceled")
        server.shutdown()
        checkForCancel = False
        cancelLink = False
        break
  spotifyLinkCancelCheckThread= Thread(target=spotifyLinkCancelCheck).start()
  server.serve_forever()
  checkForCancel = False 
  return nameToReturn
def runmsg():
  global textParseIterator
  global playMsg
  global afk
  global FileToRead
  global scrollText
  global textStorage
  # Wait for OSC client to be ready
  for _ in range(20):
    if client is not None:
      break
    time.sleep(0.1)
  while playMsg:
    try:
      textStorage = messageString
      if not afk and not scrollText:
        for x in processMessage(messageString):
          if afk or scrollText or (not playMsg) or (not run) or (messageString != textStorage):
            textStorage = messageString
            break
          if x == "*":
            sendMsg(" ㅤ")
          else:
            sendMsg(" "+x)

      elif afk:
        sendMsg('\vAFK\v')
        sendMsg('\vㅤ\v')
      elif scrollText:
        try:
          fileToOpen = open(FileToRead, "r", encoding="utf-8")
          fileText = fileToOpen.read()
          if textParseIterator + 144 < len(fileText):
            sendMsg(fileText[textParseIterator:textParseIterator+144])
            textParseIterator = textParseIterator +144
          else:
            sendMsg(fileText[textParseIterator:textParseIterator+len(fileText)-textParseIterator])
            textParseIterator = 0
        except Exception as e:
          outputLog(f'File Read Error: {e}')
          sendMsg('')
      else:
        sendMsg('')
    except Exception as e:
      outputLog(f"Message loop error: {e}")
      time.sleep(1)
  textParseIterator = 0
  if sendBlank and client is not None:
    client.send_message("/chatbox/input", [ "", True, False])
    
def msgPlayCheck():
  try:
    import keyboard
    if keyboard.is_pressed(keybind_run):
      msgPlayToggle()
  except:
    pass

_toggle_lock = Lock()
# adding a lock to prevent multiple threads from toggling playMsg at the same time, which can cause issues
def msgPlayToggle():
    global playMsg
    with _toggle_lock:
        if playMsg:
            playMsg = False
            time.sleep(.5)
        else:
            playMsg = True  
            msgThread = Thread(target=runmsg)
            msgThread.start()
            time.sleep(.5)
    
def afkCheck():
  import keyboard
  global isAfk
  global afk
  if useAfkKeybind:
    try:
      if keyboard.is_pressed(keybind_afk):
        afkToggle()
    except:
      pass
  elif isAfk:
    afk = True
  else:
    afk = False
    
def afkToggle():
  global afk
  afk = not afk
  time.sleep(.5) 

def restartMsg():
  global playMsg
  playMsg = False
  time.sleep(1.5)
  playMsg = True  
  msgThread = Thread(target=runmsg)
  msgThread.start()


def vrcRunningCheck():
  import psutil
  global vrcPID
  global playTimeDat
  def pid_check(pid):
    try:
      if psutil.pid_exists(vrcPID):
        return True
      else:
        return False
    except:
      return False
  while run:
    if not pid_check(vrcPID): 
      vrcPID = None
      for proc in psutil.process_iter():
          if not run:
            break
          if "VRChat.exe" in proc.name():
              vrcPID = proc.pid
              break
          time.sleep(.01)
      if vrcPID is not None:
        playTimeDat = time.mktime(time.localtime(psutil.Process(vrcPID).create_time()))
    time.sleep(1)


def run_app():
  global client
  global CHATBOX_PLUGIN_REGISTRY
  global dispatcher
  CHATBOX_PLUGIN_REGISTRY = create_default_registry()
  from pythonosc.dispatcher import Dispatcher
  dispatcher = Dispatcher()
  dispatcher.map("/avatar/parameters/AFK", afk_handler)
  dispatcher.map("/avatar/parameters/VRMode", vr_handler)
  dispatcher.map("/avatar/parameters/MuteSelf", mute_handler)
  dispatcher.map("/avatar/parameters/Boop", boop_handler)
  dispatcher.map("/avatar/parameters/boop", boop_handler)
  dispatcher.map("/avatar/parameters/Booped", boop_handler)
  dispatcher.map("/avatar/parameters/Contact/Receiver/Boop", boop_handler)
  dispatcher.map("/avatar/parameters/HeadPat", pat_handler)
  dispatcher.map("/avatar/parameters/Pat", pat_handler)
  dispatcher.map("/avatar/parameters/PatBool", pat_handler)
  dispatcher.map("/avatar/parameters/Headpat", pat_handler)
  dispatcher.map("/avatar/parameters/Contact/Receiver/Pat", pat_handler)
  # Create initial OSC client synchronously before starting any threads.
  from pythonosc import udp_client
  try:
    port = int(oscSendPort)
  except (TypeError, ValueError):
    port = 9000
  try:
    client = udp_client.SimpleUDPClient(str(oscSendAddress), port)
    outputLog(f"OSC client initialized: {oscSendAddress}:{port}")
  except Exception as e:
    outputLog(f"Failed to initialize OSC client: {e}")
  # Background thread refreshes client when config changes
  Thread(target=oscClientDef, daemon=True).start()
  Thread(target=oscForwardingManager, daemon=True).start()
  Thread(target=oscListenServerManager, daemon=True).start()
  Thread(target=vrcRunningCheck, daemon=True).start()
  Thread(target=runmsg, daemon=True).start()
  Thread(target=_load_spotify_tokens_background, daemon=True).start()
  Thread(target=uiThread).start()
  Thread(target=timeParameterUpdate, daemon=True).start()


def main():
  run_app()


if __name__ == "__main__":
  main()
