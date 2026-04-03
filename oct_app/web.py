"""Web UI backend for OSC Chat Tools using Flask + Flask-SocketIO."""

import os
import time
import ast
import threading
from threading import Thread
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

socketio = SocketIO()
_app = None


def create_app():
    """Create and configure the Flask application."""
    global _app
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    )
    app.config['SECRET_KEY'] = 'oct-local-secret'
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
    _app = app

    # Import main module for access to globals
    from . import main as m

    # ---- Page route ----
    @app.route('/')
    def index():
        return render_template('index.html')

    # ---- REST API: Get all config ----
    @app.route('/api/config', methods=['GET'])
    def get_config():
        return jsonify(_read_all_config(m))

    # ---- REST API: Apply config ----
    @app.route('/api/config', methods=['POST'])
    def apply_config():
        data = request.get_json(force=True)
        _apply_config(m, data)
        _save_config(m)
        return jsonify({'status': 'ok'})

    # ---- REST API: Reset config ----
    @app.route('/api/config/reset', methods=['POST'])
    def reset_config():
        _reset_config(m)
        _save_config(m)
        return jsonify(_read_all_config(m))

    # ---- REST API: Toggle run ----
    @app.route('/api/toggle/run', methods=['POST'])
    def toggle_run():
        m.msgPlayToggle()
        return jsonify({'playMsg': m.playMsg})

    # ---- REST API: Toggle AFK ----
    @app.route('/api/toggle/afk', methods=['POST'])
    def toggle_afk():
        m.afk = not m.afk
        return jsonify({'afk': m.afk})

    # ---- REST API: Layout add element ----
    @app.route('/api/layout/add', methods=['POST'])
    def layout_add():
        data = request.get_json(force=True)
        element = data.get('element', 'text(0)')
        current = m.layoutString
        parsed = _parse_layout(current)
        if len(parsed) < 15:
            m.layoutString = (current + ' {' + element + '}').strip()
            return jsonify({'layoutString': m.layoutString})
        return jsonify({'error': 'Maximum 15 elements reached'}), 400

    # ---- REST API: Layout remove element ----
    @app.route('/api/layout/remove', methods=['POST'])
    def layout_remove():
        data = request.get_json(force=True)
        index = data.get('index', 0)
        parsed = _parse_layout(m.layoutString)
        if 0 <= index < len(parsed):
            del parsed[index]
            m.layoutString = _serialize_layout(parsed)
        return jsonify({'layoutString': m.layoutString})

    # ---- REST API: Layout reorder ----
    @app.route('/api/layout/reorder', methods=['POST'])
    def layout_reorder():
        data = request.get_json(force=True)
        index = data.get('index', 0)
        direction = data.get('direction', 'up')
        parsed = _parse_layout(m.layoutString)
        if direction == 'up' and 0 < index < len(parsed):
            parsed.insert(index - 1, parsed.pop(index))
        elif direction == 'down' and 0 <= index < len(parsed) - 1:
            parsed.insert(index + 1, parsed.pop(index))
        m.layoutString = _serialize_layout(parsed)
        return jsonify({'layoutString': m.layoutString})

    # ---- REST API: Layout toggle element options ----
    @app.route('/api/layout/toggle', methods=['POST'])
    def layout_toggle():
        data = request.get_json(force=True)
        index = data.get('index', 0)
        value = data.get('value', 0)  # 0-7 (bit0=dividerAfter, bit1=newLine, bit2=dividerBefore)
        parsed = _parse_layout(m.layoutString)
        if 0 <= index < len(parsed):
            item = parsed[index]
            edit_pos = item.find('(') + 1
            if edit_pos > 0:
                parsed[index] = item[:edit_pos] + str(value) + ')'
        m.layoutString = _serialize_layout(parsed)
        return jsonify({'layoutString': m.layoutString})

    # ---- REST API: Set layout string directly ----
    @app.route('/api/layout/set', methods=['POST'])
    def layout_set():
        data = request.get_json(force=True)
        m.layoutString = data.get('layoutString', '')
        return jsonify({'layoutString': m.layoutString})

    # ---- REST API: Timer controls ----
    @app.route('/api/timer/add', methods=['POST'])
    def timer_add():
        data = request.get_json(force=True)
        hours = int(data.get('hours', 0))
        minutes = int(data.get('minutes', 0))
        seconds = int(data.get('seconds', 0))
        m.timerEndStamp += hours * 3600000 + minutes * 60000 + seconds * 1000
        return jsonify({'timerEndStamp': m.timerEndStamp})

    @app.route('/api/timer/reset', methods=['POST'])
    def timer_reset():
        m.timerEndStamp = int(datetime.now().timestamp() * 1000)
        return jsonify({'timerEndStamp': m.timerEndStamp})

    # ---- REST API: Reaction counter ----
    @app.route('/api/reaction/increment', methods=['POST'])
    def reaction_increment():
        from .plugins.builtin.reaction import increment
        count = increment()
        return jsonify({'count': count})

    @app.route('/api/reaction/reset', methods=['POST'])
    def reaction_reset():
        from .plugins.builtin.reaction import reset
        reset()
        return jsonify({'count': 0})

    # ---- REST API: Spotify link ----
    @app.route('/api/spotify/link', methods=['POST'])
    def spotify_link():
        if m.spotifyAccessToken and 'Unlinked' not in m.spotifyLinkStatus and 'Error' not in m.spotifyLinkStatus:
            # Unlink
            m.spotifyAccessToken = ''
            m.spotifyRefreshToken = ''
            m.spotifyLinkStatus = 'Unlinked'
            m.useSpotifyApi = False
            m.useMediaManager = True
            _save_config(m)
            return jsonify({'status': 'unlinked', 'spotifyLinkStatus': m.spotifyLinkStatus})
        else:
            # Start linking in background thread
            def do_link():
                result = m.linkSpotify()
                if result and result != 'Canceled' and result != 'Error':
                    m.spotifyLinkStatus = 'Linked to ' + result
                    m.useMediaManager = False
                    m.useSpotifyApi = True
                    _save_config(m)
                elif result == 'Error':
                    m.spotifyLinkStatus = 'Authentication Error'
                socketio.emit('spotify_status', {
                    'spotifyLinkStatus': m.spotifyLinkStatus,
                    'useSpotifyApi': m.useSpotifyApi,
                    'useMediaManager': m.useMediaManager,
                })
            Thread(target=do_link, daemon=True).start()
            return jsonify({'status': 'linking'})

    # ---- REST API: OSC debug send ----
    @app.route('/api/osc/debug-send', methods=['POST'])
    def osc_debug_send():
        data = request.get_json(force=True)
        path = data.get('path', '')
        value = data.get('value', '')
        value_type = data.get('type', 'int')
        try:
            type_map = {'int': int, 'float': float, 'bool': bool, 'str': str}
            converter = type_map.get(value_type, str)
            if converter == bool:
                converted = value.lower() in ('true', '1', 'yes')
            else:
                converted = converter(value)
            if m.client is not None:
                m.client.send_message(path, converted)
                m.outputLog(f"{path} => {value} | {type(converted)}")
            return jsonify({'status': 'ok'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # ---- REST API: Get live status ----
    @app.route('/api/status', methods=['GET'])
    def get_status():
        timer_var = m.timerEndStamp - int(time.time() * 1000)
        if timer_var < 0:
            timer_var = 0
        return jsonify({
            'playMsg': m.playMsg,
            'afk': m.afk,
            'msgOutput': m.msgOutput.replace('\v', '\n') if m.msgOutput else '',
            'sentTime': round(m.sentTime, 1),
            'message_delay': m.message_delay,
            'sendSkipped': m.sendSkipped,
            'version': m.version,
            'spotifyLinkStatus': m.spotifyLinkStatus,
            'timerRemaining': timer_var,
            'heartRate': getattr(m, 'heartRate', 0),
            'hrConnected': getattr(m, 'hrConnected', False),
        })

    # ---- Spotify OAuth callback (moved from linkSpotify) ----
    # The existing linkSpotify creates its own Flask app on port 8000.
    # We keep that behavior since it's a separate temporary server.

    return app


def _read_all_config(m):
    """Read all config values from main module globals."""
    return {
        'confVersion': m.version,
        'message_delay': m.message_delay,
        'messageString': m.messageString,
        'FileToRead': m.FileToRead,
        'scrollText': m.scrollText,
        'hideSong': m.hideSong,
        'hideOutside': m.hideOutside,
        'showPaused': m.showPaused,
        'songDisplay': m.songDisplay,
        'showOnChange': m.showOnChange,
        'songChangeTicks': m.songChangeTicks,
        'minimizeOnStart': m.minimizeOnStart,
        'keybind_run': m.keybind_run,
        'keybind_afk': m.keybind_afk,
        'topBar': m.topBar,
        'middleBar': m.middleBar,
        'bottomBar': m.bottomBar,
        'pulsoidToken': m.pulsoidToken,
        'avatarHR': m.avatarHR,
        'blinkOverride': m.blinkOverride,
        'blinkSpeed': m.blinkSpeed,
        'useAfkKeybind': m.useAfkKeybind,
        'toggleBeat': m.toggleBeat,
        'updatePrompt': m.updatePrompt,
        'oscListenAddress': m.oscListenAddress,
        'oscListenPort': m.oscListenPort,
        'oscSendAddress': m.oscSendAddress,
        'oscSendPort': m.oscSendPort,
        'oscForewordAddress': m.oscForewordAddress,
        'oscForewordPort': m.oscForewordPort,
        'oscListen': m.oscListen,
        'oscForeword': m.oscForeword,
        'logOutput': m.logOutput,
        'layoutString': m.layoutString,
        'verticalDivider': m.verticalDivider,
        'verticalDividerLeft': m.verticalDividerLeft,
        'animateVerticalDivider': m.animateVerticalDivider,
        'verticalDividerFrames': m.verticalDividerFrames,
        'verticalDividerLeftFrames': m.verticalDividerLeftFrames,
        'cpuDisplay': m.cpuDisplay,
        'ramDisplay': m.ramDisplay,
        'gpuDisplay': m.gpuDisplay,
        'hrDisplay': m.hrDisplay,
        'playTimeDisplay': m.playTimeDisplay,
        'mutedDisplay': m.mutedDisplay,
        'unmutedDisplay': m.unmutedDisplay,
        'darkMode': m.darkMode,
        'sendBlank': m.sendBlank,
        'suppressDuplicates': m.suppressDuplicates,
        'sendASAP': m.sendASAP,
        'useMediaManager': m.useMediaManager,
        'useSpotifyApi': m.useSpotifyApi,
        'appleMusicOnly': m.appleMusicOnly,
        'spotifySongDisplay': m.spotifySongDisplay,
        'usePulsoid': m.usePulsoid,
        'useHypeRate': m.useHypeRate,
        'hypeRateKey': m.hypeRateKey,
        'hypeRateSessionId': m.hypeRateSessionId,
        'timeDisplayAM': m.timeDisplayAM,
        'timeDisplayPM': m.timeDisplayPM,
        'showSongInfo': m.showSongInfo,
        'spotify_client_id': m.spotify_client_id,
        'useTimeParameters': m.useTimeParameters,
        'removeParenthesis': m.removeParenthesis,
        'timerDisplay': m.timerDisplay,
        'timerEndStamp': m.timerEndStamp,
        'spotifyLinkStatus': m.spotifyLinkStatus,
        # Text feature config
        'textStyle': m.textStyle,
        'flipText': m.flipText,
        'mirrorText': m.mirrorText,
        'zalgoEnabled': m.zalgoEnabled,
        'zalgoIntensity': m.zalgoIntensity,
        'kaomojiCategory': m.kaomojiCategory,
        'textAccentFrames': m.textAccentFrames,
        'eightBallDisplay': m.eightBallDisplay,
        'eightBallInterval': m.eightBallInterval,
        'diceDisplay': m.diceDisplay,
        'diceSides': m.diceSides,
        'diceCount': m.diceCount,
        'diceInterval': m.diceInterval,
        'fortuneDisplay': m.fortuneDisplay,
        'fortuneFile': m.fortuneFile,
        'fortuneInterval': m.fortuneInterval,
        'typewriterSpeed': m.typewriterSpeed,
        'cyclerMessages': m.cyclerMessages,
        'cyclerInterval': m.cyclerInterval,
        'reactionDisplay': m.reactionDisplay,
        'reactionLabel': m.reactionLabel,
        'borderStyle': m.borderStyle,
        'marqueeWidth': m.marqueeWidth,
        'marqueeSpeed': m.marqueeSpeed,
        'textAlignment': m.textAlignment,
        'textAlignWidth': m.textAlignWidth,
        'smartTruncateMax': m.smartTruncateMax,
        'animateFrames': m.animateFrames,
        'animateSpeed': m.animateSpeed,
    }


def _apply_config(m, data):
    """Apply config values from a dict to main module globals."""
    # Map of config key -> (global name, type converter)
    type_map = {
        'message_delay': float,
        'messageString': str,
        'FileToRead': str,
        'scrollText': bool,
        'hideSong': bool,
        'hideOutside': bool,
        'showPaused': bool,
        'songDisplay': str,
        'showOnChange': bool,
        'songChangeTicks': float,
        'minimizeOnStart': bool,
        'keybind_run': str,
        'keybind_afk': str,
        'topBar': str,
        'middleBar': str,
        'bottomBar': str,
        'pulsoidToken': str,
        'avatarHR': bool,
        'blinkOverride': bool,
        'blinkSpeed': float,
        'useAfkKeybind': bool,
        'toggleBeat': bool,
        'updatePrompt': bool,
        'oscListenAddress': str,
        'oscListenPort': str,
        'oscSendAddress': str,
        'oscSendPort': str,
        'oscForewordAddress': str,
        'oscForewordPort': str,
        'oscListen': bool,
        'oscForeword': bool,
        'logOutput': bool,
        'layoutString': str,
        'verticalDivider': str,
        'verticalDividerLeft': str,
        'animateVerticalDivider': bool,
        'verticalDividerFrames': str,
        'verticalDividerLeftFrames': str,
        'cpuDisplay': str,
        'ramDisplay': str,
        'gpuDisplay': str,
        'hrDisplay': str,
        'playTimeDisplay': str,
        'mutedDisplay': str,
        'unmutedDisplay': str,
        'darkMode': bool,
        'sendBlank': bool,
        'suppressDuplicates': bool,
        'sendASAP': bool,
        'useMediaManager': bool,
        'useSpotifyApi': bool,
        'appleMusicOnly': bool,
        'spotifySongDisplay': str,
        'usePulsoid': bool,
        'useHypeRate': bool,
        'hypeRateKey': str,
        'hypeRateSessionId': str,
        'timeDisplayAM': str,
        'timeDisplayPM': str,
        'showSongInfo': bool,
        'spotify_client_id': str,
        'useTimeParameters': bool,
        'removeParenthesis': bool,
        'timerDisplay': str,
        # New text feature settings
        'textStyle': str,
        'flipText': bool,
        'mirrorText': bool,
        'zalgoEnabled': bool,
        'zalgoIntensity': int,
        'kaomojiCategory': str,
        'textAccentFrames': str,
        'eightBallDisplay': str,
        'eightBallInterval': int,
        'diceDisplay': str,
        'diceSides': int,
        'diceCount': int,
        'diceInterval': int,
        'fortuneDisplay': str,
        'fortuneFile': str,
        'fortuneInterval': int,
        'typewriterSpeed': int,
        'cyclerMessages': str,
        'cyclerInterval': int,
        'reactionDisplay': str,
        'reactionLabel': str,
        'borderStyle': str,
        'marqueeWidth': int,
        'marqueeSpeed': int,
        'textAlignment': str,
        'textAlignWidth': int,
        'smartTruncateMax': int,
        'animateFrames': str,
        'animateSpeed': int,
    }
    for key, converter in type_map.items():
        if key in data:
            try:
                setattr(m, key, converter(data[key]))
            except (ValueError, TypeError):
                pass
    m.confVersion = m.version


def _reset_config(m):
    """Reset all config values to defaults."""
    m.message_delay = 1.5
    m.messageString = 'OSC Chat Tools\nBy Lioncat6'
    m.FileToRead = ''
    m.scrollText = False
    m.hideSong = False
    m.hideOutside = True
    m.showPaused = True
    m.songDisplay = " \U0001f3b5'{title}' \u1d47\u02b8 {artist}\U0001f3b6"
    m.showOnChange = False
    m.songChangeTicks = 1
    m.minimizeOnStart = False
    m.keybind_run = '`'
    m.keybind_afk = 'end'
    m.topBar = '\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557'
    m.middleBar = '\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563'
    m.bottomBar = '\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d'
    m.pulsoidToken = ''
    m.avatarHR = False
    m.blinkOverride = False
    m.blinkSpeed = 0.5
    m.useAfkKeybind = False
    m.toggleBeat = True
    m.updatePrompt = True
    m.oscListenAddress = '127.0.0.1'
    m.oscListenPort = '9001'
    m.oscSendAddress = '127.0.0.1'
    m.oscSendPort = '9000'
    m.oscForewordAddress = '127.0.0.1'
    m.oscForewordPort = '9002'
    m.oscListen = False
    m.oscForeword = False
    m.logOutput = False
    m.layoutString = ''
    m.verticalDivider = '\u3023'
    m.verticalDividerLeft = '\u3023'
    m.animateVerticalDivider = False
    m.verticalDividerFrames = '\u3023,\u3022,\u3021,\u3022'
    m.verticalDividerLeftFrames = '\u3023,\u3022,\u3021,\u3022'
    m.cpuDisplay = '\u1d04\u1d18\u1d1c: {cpu_percent}%'
    m.ramDisplay = '\u0280\u1d00\u1d0d: {ram_percent}%  ({ram_used}/{ram_total})'
    m.gpuDisplay = '\u0262\u1d18\u1d1c: {gpu_percent}%'
    m.hrDisplay = '\U0001f493 {hr}'
    m.playTimeDisplay = '\u231b{hours}:{remainder_minutes}'
    m.mutedDisplay = 'Muted \U0001f507'
    m.unmutedDisplay = '\U0001f50a'
    m.darkMode = True
    m.sendBlank = True
    m.suppressDuplicates = False
    m.sendASAP = False
    m.useMediaManager = True
    m.useSpotifyApi = False
    m.appleMusicOnly = False
    m.spotifySongDisplay = "\U0001f3b5'{title}' \u1d47\u02b8 {artist}\U0001f3b6 \u300e{song_progress}/{song_length}\u300f"
    m.spotifyAccessToken = ''
    m.spotifyRefreshToken = ''
    m.spotifyLinkStatus = 'Unlinked'
    m.usePulsoid = True
    m.useHypeRate = False
    m.hypeRateKey = 'FIrXkWWlf57iHjMu0x3lEMNst8IDIzwUA2UD6lmSxL4BqBUTYw8LCwQlM2n5U8RU'
    m.hypeRateSessionId = ''
    m.timeDisplayAM = '{hour}:{minute} AM'
    m.timeDisplayPM = '{hour}:{minute} PM'
    m.showSongInfo = True
    m.spotify_client_id = '915e1de141b3408eb430d25d0d39b380'
    m.useTimeParameters = False
    m.removeParenthesis = False
    m.timerDisplay = '{hours}:{minutes}:{seconds}'
    m.timerEndStamp = int(datetime.now().timestamp() * 1000)
    # New text feature defaults
    m.textStyle = 'none'
    m.flipText = False
    m.mirrorText = False
    m.zalgoEnabled = False
    m.zalgoIntensity = 2
    m.kaomojiCategory = 'random'
    m.textAccentFrames = '✧,✦,★,☆,✶,✷'
    m.eightBallDisplay = '🎱 {response}'
    m.eightBallInterval = 30
    m.diceDisplay = '🎲 {result}'
    m.diceSides = 6
    m.diceCount = 1
    m.diceInterval = 30
    m.fortuneDisplay = '🥠 {fortune}'
    m.fortuneFile = ''
    m.fortuneInterval = 60
    m.typewriterSpeed = 2
    m.cyclerMessages = ''
    m.cyclerInterval = 5
    m.reactionDisplay = '💜 {label}: {count}'
    m.reactionLabel = 'Headpats'
    m.borderStyle = 'double'
    m.marqueeWidth = 20
    m.marqueeSpeed = 1
    m.textAlignment = 'left'
    m.textAlignWidth = 30
    m.smartTruncateMax = 144
    m.animateFrames = '[ Loading . ],[ Loading .. ],[ Loading ... ]'
    m.animateSpeed = 1


def _save_config(m):
    """Save config to the legacy file format."""
    try:
        m.confVersion = m.version
        config_list = [
            m.confVersion, m.message_delay, m.messageString, m.FileToRead,
            m.scrollText, m.hideSong, m.hideOutside, m.showPaused,
            m.songDisplay, m.showOnChange, m.songChangeTicks, m.minimizeOnStart,
            m.keybind_run, m.keybind_afk, m.topBar, m.middleBar, m.bottomBar,
            m.pulsoidToken, m.avatarHR, m.blinkOverride, m.blinkSpeed,
            m.useAfkKeybind, m.toggleBeat, m.updatePrompt, m.oscListenAddress,
            m.oscListenPort, m.oscSendAddress, m.oscSendPort,
            m.oscForewordAddress, m.oscForeword, m.oscListen, m.oscForeword,
            m.logOutput, m.layoutString, m.verticalDivider, m.cpuDisplay,
            m.ramDisplay, m.gpuDisplay, m.hrDisplay, m.playTimeDisplay,
            m.mutedDisplay, m.unmutedDisplay, m.darkMode, m.sendBlank,
            m.suppressDuplicates, m.sendASAP, m.useMediaManager,
            m.useSpotifyApi, m.appleMusicOnly, m.spotifySongDisplay,
            m.spotifyAccessToken, m.spotifyRefreshToken, m.usePulsoid,
            m.useHypeRate, m.hypeRateKey, m.hypeRateSessionId,
            m.timeDisplayPM, m.timeDisplayAM, m.showSongInfo,
            m.spotify_client_id, m.useTimeParameters, m.removeParenthesis,
            m.timerDisplay, m.timerEndStamp, m.animateVerticalDivider,
            m.verticalDividerFrames, m.verticalDividerLeft,
            m.verticalDividerLeftFrames,
            # New text feature config
            m.textStyle, m.flipText, m.mirrorText, m.zalgoEnabled,
            m.zalgoIntensity, m.kaomojiCategory, m.textAccentFrames,
            m.eightBallDisplay, m.eightBallInterval, m.diceDisplay,
            m.diceSides, m.diceCount, m.diceInterval, m.fortuneDisplay,
            m.fortuneFile, m.fortuneInterval, m.typewriterSpeed,
            m.cyclerMessages, m.cyclerInterval, m.reactionDisplay,
            m.reactionLabel, m.borderStyle, m.marqueeWidth, m.marqueeSpeed,
            m.textAlignment, m.textAlignWidth, m.smartTruncateMax,
            m.animateFrames, m.animateSpeed,
        ]
        with open('please-do-not-delete.txt', 'w', encoding='utf-8') as f:
            f.write(str(config_list))
    except Exception as e:
        m.outputLog('Error saving config: ' + str(e))


def _parse_layout(layout_str):
    """Parse layout string like '{text(0)} {song(1)}' into list ['text(0)', 'song(1)']."""
    if not layout_str or not layout_str.strip():
        return []
    try:
        converted = "[" + layout_str.replace("{", "\"").replace("}", "\",")[:-1] + "]"
        return ast.literal_eval(converted)
    except Exception:
        return []


def _serialize_layout(layout_list):
    """Convert list ['text(0)', 'song(1)'] back to '{text(0)} {song(1)}'."""
    return ' '.join('{' + item + '}' for item in layout_list)


# ---- Background thread for SocketIO real-time updates ----
_update_thread_started = False


def start_update_thread(m):
    """Start background thread that emits real-time updates via SocketIO."""
    global _update_thread_started
    if _update_thread_started:
        return
    _update_thread_started = True

    def update_loop():
        while m.run:
            try:
                timer_var = m.timerEndStamp - int(time.time() * 1000)
                if timer_var < 0:
                    timer_var = 0

                song_info = {
                    'name': getattr(m, 'songName', ''),
                    'spotifyPlayState': getattr(m, 'spotifyPlayState', ''),
                    'spotifySongUrl': getattr(m, 'spotifySongUrl', ''),
                    'useSpotifyApi': m.useSpotifyApi,
                    'showSongInfo': m.showSongInfo,
                }

                socketio.emit('status_update', {
                    'playMsg': m.playMsg,
                    'afk': m.afk,
                    'msgOutput': m.msgOutput.replace('\v', '\n') if m.msgOutput else '',
                    'sentTime': round(getattr(m, 'sentTime', 0), 1),
                    'message_delay': m.message_delay,
                    'sendSkipped': getattr(m, 'sendSkipped', False),
                    'timerRemaining': timer_var,
                    'heartRate': getattr(m, 'heartRate', 0),
                    'hrConnected': getattr(m, 'hrConnected', False),
                    'song': song_info,
                    'layoutString': m.layoutString,
                })
            except Exception:
                pass
            time.sleep(0.5)

    thread = Thread(target=update_loop, daemon=True)
    thread.start()


# ---- Log output hook ----
_log_messages = []
_log_lock = threading.Lock()
MAX_LOG_LINES = 1000


def web_output_log(text):
    """Append a log message and emit via SocketIO."""
    timestamp = datetime.now()
    thread_name = threading.current_thread().name
    formatted = f"{timestamp} [{thread_name}] {text}"
    with _log_lock:
        _log_messages.append(formatted)
        if len(_log_messages) > MAX_LOG_LINES:
            _log_messages.pop(0)
    try:
        socketio.emit('log_append', {'line': formatted})
    except Exception:
        pass
    print(text.replace('\n', '\n    '))


def get_log_history():
    """Return all accumulated log messages."""
    with _log_lock:
        return list(_log_messages)
