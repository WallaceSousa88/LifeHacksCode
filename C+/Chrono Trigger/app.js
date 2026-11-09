// Chrono Trigger - WebAssembly SNES Player
// Inicialização do core Snes9x compilado para WebAssembly

const dropzone = document.getElementById('rom-dropzone');
const dropTarget = document.getElementById('drop-target');
const fileInput = document.getElementById('rom-file-input');
const emulatorSection = document.getElementById('emulator-section');
const emulatorContainer = document.getElementById('emulator-container');
const btnFullscreen = document.getElementById('btn-fullscreen');
const btnChangeRom = document.getElementById('btn-change-rom');
const gamepadStatus = document.getElementById('gamepad-status');
const gamepadLabel = document.getElementById('gamepad-label');

let currentRomUrl = null;

// Configuração de Drag & Drop
['dragenter', 'dragover'].forEach(eventName => {
    dropTarget.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropTarget.classList.add('drag-over');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropTarget.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropTarget.classList.remove('drag-over');
    });
});

dropTarget.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleRomFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleRomFile(e.target.files[0]);
    }
});

// Processamento da ROM
function handleRomFile(file) {
    const validExtensions = ['.sfc', '.smc', '.zip'];
    const fileName = file.name.toLowerCase();
    const isValid = validExtensions.some(ext => fileName.endsWith(ext));

    if (!isValid) {
        alert('Formato de arquivo não suportado. Por favor, utilize uma ROM de SNES (.sfc, .smc ou .zip).');
        return;
    }

    if (currentRomUrl) {
        URL.revokeObjectURL(currentRomUrl);
    }

    currentRomUrl = URL.createObjectURL(file);
    startEmulator(currentRomUrl, file.name);
}

// Inicialização do Core WebAssembly
function startEmulator(romUrl, romName) {
    // Alterna a interface
    dropzone.style.display = 'none';
    emulatorSection.style.display = 'flex';
    btnFullscreen.style.display = 'inline-flex';
    btnChangeRom.style.display = 'inline-flex';

    // Limpa o container anterior se houver
    emulatorContainer.innerHTML = '';

    // Configurações globais do EmulatorJS para o Core Snes9x em WASM
    window.EJS_player = '#emulator-container';
    window.EJS_core = 'snes'; // Core Snes9x WebAssembly
    window.EJS_gameUrl = romUrl;
    window.EJS_gameName = romName || 'Chrono Trigger';
    window.EJS_pathtodata = 'https://cdn.emulatorjs.org/stable/data/';
    window.EJS_startOnLoaded = true;
    window.EJS_color = '#00e5ff';
    window.EJS_align = 'center';

    // Injeta o script carregador do EmulatorJS
    const existingScript = document.getElementById('ejs-loader-script');
    if (existingScript) {
        existingScript.remove();
    }

    const script = document.createElement('script');
    script.id = 'ejs-loader-script';
    script.src = 'https://cdn.emulatorjs.org/stable/data/loader.js';
    script.async = true;
    document.body.appendChild(script);
}

// Botão de Tela Cheia
btnFullscreen.addEventListener('click', () => {
    const frame = document.querySelector('.screen-frame');
    if (!document.fullscreenElement) {
        if (frame.requestFullscreen) {
            frame.requestFullscreen();
        } else if (frame.webkitRequestFullscreen) {
            frame.webkitRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
});

// Botão Trocar ROM
btnChangeRom.addEventListener('click', () => {
    if (confirm('Deseja parar o jogo atual e carregar outra ROM? (Certifique-se de ter salvo seu progresso)')) {
        emulatorContainer.innerHTML = '';
        emulatorSection.style.display = 'none';
        btnFullscreen.style.display = 'none';
        btnChangeRom.style.display = 'none';
        dropzone.style.display = 'flex';
        fileInput.value = '';
    }
});

// Detecção de Controles/Gamepads (USB / Bluetooth no Edge)
window.addEventListener('gamepadconnected', (e) => {
    gamepadStatus.classList.add('connected');
    gamepadLabel.textContent = `Controle detectado: "${e.gamepad.id}". Mapeamento automático ativo!`;
});

window.addEventListener('gamepaddisconnected', (e) => {
    const gamepads = navigator.getGamepads ? navigator.getGamepads() : [];
    const active = Array.from(gamepads).some(gp => gp !== null);
    if (!active) {
        gamepadStatus.classList.remove('connected');
        gamepadLabel.textContent = 'Controle desconectado. Usando teclado como controle principal.';
    }
});
