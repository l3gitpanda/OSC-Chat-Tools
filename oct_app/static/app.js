/* OSC Chat Tools - Web UI Frontend */

// ---- SocketIO connection ----
const socket = io();

// ---- Layout display names ----
const layoutDisplayDict = {
    'playtime(': '\u231A Play Time',
    'text(': '\uD83D\uDCAC Text',
    'time(': '\uD83D\uDD52 Time',
    'song(': '\uD83C\uDFB5 Song',
    'cpu(': '\u23F1 CPU Usage',
    'ram(': '\uD83D\uDEA6 RAM Usage',
    'gpu(': '\u231B GPU Usage',
    'hr(': '\uD83D\uDC93 Heart Rate',
    'mute(': '\uD83D\uDD07 Mute Status',
    'stt(': '\u2328 Speech To Text',
    'div(': '\u2635 Divider',
    'timer(': '\u23F2 Timer',
};

// ---- State ----
let currentConfig = {};

// ---- Tab switching ----
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
});

// Sub-tab switching (Behavior tab)
document.querySelectorAll('.sub-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.sub-tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.sub-tab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.subtab).classList.add('active');
    });
});

// ---- Slider value display ----
['msgDelay', 'songChangeTicks', 'blinkSpeed'].forEach(id => {
    const el = document.getElementById(id);
    const valEl = document.getElementById(id + '-val');
    if (el && valEl) {
        el.addEventListener('input', () => { valEl.textContent = el.value; });
    }
});

// ---- Load config on page load ----
async function loadConfig() {
    try {
        const resp = await fetch('/api/config');
        const data = await resp.json();
        currentConfig = data;
        populateForm(data);
    } catch (e) {
        console.error('Failed to load config:', e);
    }
}

function populateForm(data) {
    // Text inputs
    const textFields = [
        'FileToRead', 'songDisplay', 'spotifySongDisplay', 'spotify_client_id',
        'cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay',
        'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay',
        'topBar', 'middleBar', 'bottomBar', 'verticalDivider', 'verticalDividerFrames',
        'timeDisplayAM', 'timeDisplayPM', 'pulsoidToken', 'hypeRateKey', 'hypeRateSessionId',
        'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort',
        'oscForewordAddress', 'oscForewordPort',
        'keybind_run', 'keybind_afk', 'timerDisplay',
    ];
    textFields.forEach(id => {
        const el = document.getElementById(id);
        if (el && data[id] !== undefined) el.value = data[id];
    });

    // Textareas
    if (data.messageString !== undefined) {
        document.getElementById('messageInput').value = data.messageString;
    }
    if (data.layoutString !== undefined) {
        document.getElementById('layoutStorage').value = data.layoutString;
        renderLayoutEditor(data.layoutString);
    }

    // Checkboxes
    const checkboxes = [
        'scrollText', 'sendBlank', 'suppressDuplicates', 'sendASAP',
        'hideSong', 'hideOutside', 'showPaused', 'showOnChange',
        'appleMusicOnly', 'removeParenthesis',
        'avatarHR', 'blinkOverride', 'toggleBeat',
        'animateVerticalDivider',
        'minimizeOnStart', 'updatePrompt', 'darkMode', 'showSongInfo',
        'useAfkKeybind', 'oscListen', 'oscForeword', 'logOutput',
        'useTimeParameters',
    ];
    checkboxes.forEach(id => {
        const el = document.getElementById(id);
        if (el && data[id] !== undefined) el.checked = data[id];
    });

    // Radio buttons
    if (data.useMediaManager) {
        document.getElementById('useMediaManager').checked = true;
    } else if (data.useSpotifyApi) {
        document.getElementById('useSpotifyApi').checked = true;
    }
    if (data.usePulsoid) {
        document.getElementById('usePulsoid').checked = true;
    } else if (data.useHypeRate) {
        document.getElementById('useHypeRate').checked = true;
    }

    // Sliders
    const sliders = {
        'msgDelay': 'message_delay',
        'songChangeTicks': 'songChangeTicks',
        'blinkSpeed': 'blinkSpeed',
    };
    Object.entries(sliders).forEach(([elId, key]) => {
        const el = document.getElementById(elId);
        const valEl = document.getElementById(elId + '-val');
        if (el && data[key] !== undefined) {
            el.value = data[key];
            if (valEl) valEl.textContent = data[key];
        }
    });

    // Version
    if (data.confVersion) {
        document.getElementById('versionText').textContent = 'Version ' + data.confVersion;
    }

    // Spotify link status
    updateSpotifyStatus(data.spotifyLinkStatus || 'Unlinked');

    // Dark mode
    if (data.darkMode === false) {
        document.body.classList.add('light-mode');
    } else {
        document.body.classList.remove('light-mode');
    }
}

// ---- Collect form data ----
function collectFormData() {
    const data = {};

    // Text inputs
    const textFields = [
        'FileToRead', 'songDisplay', 'spotifySongDisplay', 'spotify_client_id',
        'cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay',
        'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay',
        'topBar', 'middleBar', 'bottomBar', 'verticalDivider', 'verticalDividerFrames',
        'timeDisplayAM', 'timeDisplayPM', 'pulsoidToken', 'hypeRateKey', 'hypeRateSessionId',
        'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort',
        'oscForewordAddress', 'oscForewordPort',
        'keybind_run', 'keybind_afk', 'timerDisplay',
    ];
    textFields.forEach(id => {
        const el = document.getElementById(id);
        if (el) data[id] = el.value;
    });

    // Textareas
    data.messageString = document.getElementById('messageInput').value;
    data.layoutString = document.getElementById('layoutStorage').value;

    // Checkboxes
    const checkboxes = [
        'scrollText', 'sendBlank', 'suppressDuplicates', 'sendASAP',
        'hideSong', 'hideOutside', 'showPaused', 'showOnChange',
        'appleMusicOnly', 'removeParenthesis',
        'avatarHR', 'blinkOverride', 'toggleBeat',
        'animateVerticalDivider',
        'minimizeOnStart', 'updatePrompt', 'darkMode', 'showSongInfo',
        'useAfkKeybind', 'oscListen', 'oscForeword', 'logOutput',
        'useTimeParameters',
    ];
    checkboxes.forEach(id => {
        const el = document.getElementById(id);
        if (el) data[id] = el.checked;
    });

    // Radio buttons
    data.useMediaManager = document.getElementById('useMediaManager').checked;
    data.useSpotifyApi = document.getElementById('useSpotifyApi').checked;
    data.usePulsoid = document.getElementById('usePulsoid').checked;
    data.useHypeRate = document.getElementById('useHypeRate').checked;

    // Sliders
    data.message_delay = parseFloat(document.getElementById('msgDelay').value);
    data.songChangeTicks = parseFloat(document.getElementById('songChangeTicks').value);
    data.blinkSpeed = parseFloat(document.getElementById('blinkSpeed').value);

    return data;
}

// ---- Apply config ----
async function applyConfig() {
    const data = collectFormData();
    try {
        await fetch('/api/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data),
        });
        // Apply dark mode immediately
        if (data.darkMode === false) {
            document.body.classList.add('light-mode');
        } else {
            document.body.classList.remove('light-mode');
        }
        showToast('Settings applied!');
    } catch (e) {
        showToast('Error applying settings', true);
    }
}

// ---- Reset config ----
async function resetConfig() {
    if (!confirm('Are you sure? This will erase all entered text and reset the configuration file!')) {
        return;
    }
    try {
        const resp = await fetch('/api/config/reset', { method: 'POST' });
        const data = await resp.json();
        populateForm(data);
        showToast('Settings reset to defaults!');
    } catch (e) {
        showToast('Error resetting settings', true);
    }
}

// ---- Toggle Run / AFK ----
async function toggleRun() {
    try {
        const resp = await fetch('/api/toggle/run', { method: 'POST' });
        const data = await resp.json();
        document.getElementById('runToggle').checked = data.playMsg;
    } catch (e) {
        console.error('Toggle run failed:', e);
    }
}

async function toggleAfk() {
    try {
        const resp = await fetch('/api/toggle/afk', { method: 'POST' });
        const data = await resp.json();
        document.getElementById('afkToggle').checked = data.afk;
    } catch (e) {
        console.error('Toggle afk failed:', e);
    }
}

// ---- Layout editor ----
function addLayoutElement(element) {
    fetch('/api/layout/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ element }),
    }).then(r => r.json()).then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        document.getElementById('layoutStorage').value = data.layoutString;
        renderLayoutEditor(data.layoutString);
    });
}

function removeLayoutElement(index) {
    fetch('/api/layout/remove', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ index }),
    }).then(r => r.json()).then(data => {
        document.getElementById('layoutStorage').value = data.layoutString;
        renderLayoutEditor(data.layoutString);
    });
}

function moveLayoutElement(index, direction) {
    fetch('/api/layout/reorder', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ index, direction }),
    }).then(r => r.json()).then(data => {
        document.getElementById('layoutStorage').value = data.layoutString;
        renderLayoutEditor(data.layoutString);
    });
}

function toggleLayoutOption(index, divider, newLine) {
    let value = 0;
    if (divider && newLine) value = 3;
    else if (divider) value = 1;
    else if (newLine) value = 2;

    fetch('/api/layout/toggle', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ index, value }),
    }).then(r => r.json()).then(data => {
        document.getElementById('layoutStorage').value = data.layoutString;
        renderLayoutEditor(data.layoutString);
    });
}

function parseLayout(layoutStr) {
    if (!layoutStr || !layoutStr.trim()) return [];
    try {
        const items = [];
        const regex = /\{([^}]+)\}/g;
        let match;
        while ((match = regex.exec(layoutStr)) !== null) {
            items.push(match[1]);
        }
        return items;
    } catch (e) {
        return [];
    }
}

function getDisplayName(item) {
    for (const [key, name] of Object.entries(layoutDisplayDict)) {
        if (item.includes(key)) return name;
    }
    return item;
}

function getItemOptions(item) {
    const match = item.match(/\((\d)\)/);
    const val = match ? parseInt(match[1]) : 0;
    return {
        divider: val === 1 || val === 3,
        newLine: val === 2 || val === 3,
    };
}

function renderLayoutEditor(layoutStr) {
    const container = document.getElementById('layout-editor');
    const items = parseLayout(layoutStr);
    container.innerHTML = '';

    items.forEach((item, i) => {
        const opts = getItemOptions(item);
        const div = document.createElement('div');
        div.className = 'layout-item';
        div.innerHTML = `
            <button onclick="removeLayoutElement(${i})" title="Delete">\u274C</button>
            <button onclick="moveLayoutElement(${i}, 'up')" ${i === 0 ? 'disabled' : ''} title="Move up">\u2B06</button>
            <button onclick="moveLayoutElement(${i}, 'down')" ${i === items.length - 1 ? 'disabled' : ''} title="Move down">\u2B07</button>
            <span class="item-name">${getDisplayName(item)}</span>
            <label><input type="checkbox" ${opts.divider ? 'checked' : ''} onchange="toggleLayoutOption(${i}, this.checked, this.parentElement.nextElementSibling.querySelector('input').checked)"> \u250B</label>
            <label><input type="checkbox" ${opts.newLine ? 'checked' : ''} onchange="toggleLayoutOption(${i}, this.parentElement.previousElementSibling.querySelector('input').checked, this.checked)"> \u21A5</label>
        `;
        container.appendChild(div);
    });

    if (items.length === 0) {
        container.innerHTML = '<p class="hint" style="padding:8px">No elements added yet. Use "Add to Layout" buttons on the left.</p>';
    }
}

// Manual layout textarea sync
document.getElementById('layoutStorage').addEventListener('change', function() {
    fetch('/api/layout/set', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ layoutString: this.value }),
    }).then(r => r.json()).then(data => {
        renderLayoutEditor(data.layoutString);
    });
});

// ---- Timer ----
async function addTimer(unit) {
    const data = { hours: 0, minutes: 0, seconds: 0 };
    const el = document.getElementById('add' + unit.charAt(0).toUpperCase() + unit.slice(1));
    if (el && el.value) {
        data[unit] = parseInt(el.value) || 0;
        el.value = '';
    }
    try {
        await fetch('/api/timer/add', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data),
        });
    } catch (e) {
        console.error('Timer add failed:', e);
    }
}

async function resetTimer() {
    try {
        await fetch('/api/timer/reset', { method: 'POST' });
    } catch (e) {
        console.error('Timer reset failed:', e);
    }
}

// ---- Spotify ----
async function linkSpotify() {
    try {
        // First apply current spotify settings
        await applyConfig();
        const resp = await fetch('/api/spotify/link', { method: 'POST' });
        const data = await resp.json();
        if (data.status === 'linking') {
            updateSpotifyStatus('Linking...');
        } else if (data.status === 'unlinked') {
            updateSpotifyStatus('Unlinked');
        }
    } catch (e) {
        console.error('Spotify link failed:', e);
    }
}

function updateSpotifyStatus(status) {
    const el = document.getElementById('spotifyLinkStatus');
    const btn = document.getElementById('linkSpotifyBtn');
    el.textContent = status;
    el.className = '';
    if (status.includes('Error')) {
        el.className = 'status-red';
        btn.textContent = 'Relink Spotify \u26A0\uFE0F';
        btn.style.background = '#c00';
    } else if (status.includes('Linked') && !status.includes('Unlinked')) {
        el.className = 'status-green';
        btn.textContent = 'Unlink Spotify \uD83D\uDD17';
        btn.style.background = '#c68341';
    } else {
        el.className = 'status-orange';
        btn.textContent = 'Link Spotify \uD83D\uDD17';
        btn.style.background = '#00a828';
    }
}

// ---- OSC Debug ----
async function sendDebug() {
    const path = document.getElementById('debugPath').value;
    const value = document.getElementById('debugValue').value;
    const type = document.getElementById('debugType').value;
    try {
        const resp = await fetch('/api/osc/debug-send', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ path, value, type }),
        });
        const data = await resp.json();
        if (data.error) alert('Error: ' + data.error);
    } catch (e) {
        console.error('Debug send failed:', e);
    }
}

// ---- Manual help popup ----
function showManualHelp() {
    const objectList = Object.entries(layoutDisplayDict).map(([k, v]) => {
        return k.replace('(', '(data)') + ' : ' + v;
    }).join('\n');

    alert('Manual Editing Guide\n\n' +
        'Warning: Manually editing can cause errors!\n\n' +
        'Objects:\n' + objectList + '\n\n' +
        'Data Guide (Defaults to 0):\n' +
        '0 : No Data\n1 : Vertical Line\n2 : New Line\n3 : Both');
}

// ---- Toast notification ----
function showToast(msg, isError) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    toast.style.cssText = `
        position: fixed; top: 12px; right: 12px; padding: 10px 20px;
        background: ${isError ? '#c00' : '#00a828'}; color: white;
        border-radius: 6px; font-size: 13px; z-index: 9999;
        animation: fadeIn 0.2s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
}

// ---- SocketIO real-time updates ----
socket.on('status_update', (data) => {
    // Update run/afk toggles
    document.getElementById('runToggle').checked = data.playMsg;
    document.getElementById('afkToggle').checked = data.afk;

    // Update preview
    document.getElementById('messagePreview').textContent = data.msgOutput || '';

    // Update sent countdown
    if (data.sendSkipped) {
        document.getElementById('sentCountdown').textContent =
            'Last sent: ' + data.sentTime + '/30 [Skipped Send]';
    } else {
        document.getElementById('sentCountdown').textContent =
            'Last sent: ' + data.sentTime + '/' + data.message_delay;
    }

    // Update timer
    const tr = data.timerRemaining || 0;
    const h = Math.floor(tr / 3600000);
    const m = Math.floor((tr / 60000) % 60);
    const s = Math.floor((tr / 1000) % 60);
    document.getElementById('currentTimer').textContent =
        String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');

    // Update song ribbon
    const song = data.song || {};
    const ribbon = document.getElementById('songRibbon');
    if (data.playMsg && song.showSongInfo && song.name) {
        ribbon.classList.add('visible');
        const isPlaying = song.spotifyPlayState === 'PLAYING';
        document.getElementById('ribbonPlayStatus').textContent = isPlaying ? '\u25B6\uFE0F' : '\u23F8\uFE0F';

        let displayName = song.name;
        if (displayName.length > 30) displayName = displayName.substring(0, 30) + '...';
        document.getElementById('ribbonSongName').textContent = displayName;
        document.getElementById('ribbonSongName').onclick = () => {
            if (song.spotifySongUrl && song.useSpotifyApi) {
                window.open(song.spotifySongUrl);
            }
        };
    } else {
        ribbon.classList.remove('visible');
    }
});

socket.on('log_append', (data) => {
    const logEl = document.getElementById('output-log');
    if (logEl.textContent) {
        logEl.textContent += '\n' + data.line;
    } else {
        logEl.textContent = data.line;
    }
    logEl.scrollTop = logEl.scrollHeight;
});

socket.on('spotify_status', (data) => {
    updateSpotifyStatus(data.spotifyLinkStatus || 'Unlinked');
    if (data.useSpotifyApi !== undefined) {
        document.getElementById('useSpotifyApi').checked = data.useSpotifyApi;
        document.getElementById('useMediaManager').checked = data.useMediaManager;
    }
});

// ---- Initialize ----
loadConfig();
