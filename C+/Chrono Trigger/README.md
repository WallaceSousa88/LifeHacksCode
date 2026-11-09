# Chrono Trigger — WebAssembly SNES Player

Projeto para execução de jogos de Super Nintendo (com foco em **Chrono Trigger**) diretamente no navegador (otimizado para **Microsoft Edge**) utilizando **WebAssembly (WASM)**, **WebGL** e **Web Audio API**.

---

## ⚡ Como Funciona a Tecnologia?

1. **Núcleo em C++ / WebAssembly:**
   - O núcleo do emulador (**Snes9x**) é compilado de C/C++ para bytecode binário **WebAssembly** através do compilador Emscripten.
   - Isso permite que as instruções da CPU do SNES (arquitetura **Ricoh 5A22 / W65C816** de 16-bits) sejam executadas com velocidade nativa (60 FPS) diretamente no motor V8 do Edge, sem plugins externos.

2. **Renderização Acelerada por Hardware (WebGL):**
   - Os gráficos Mode 7 e planos de sprites do SNES são renderizados no elemento `<canvas>` utilizando WebGL com aceleração por GPU.

3. **Gerenciador de Saves:**
   - O progresso da bateria (SRAM) e os Save States rápidos ficam salvos localmente no armazenamento do navegador (IndexedDB), permitindo salvar e continuar a qualquer momento.

---

## 🚀 Como Iniciar

1. Dê dois cliques no arquivo **`start.bat`** (ou execute `python server.py` no terminal).
2. O servidor local será iniciado e abrirá automaticamente o **Microsoft Edge** em `http://localhost:8080`.
3. Arraste e solte o arquivo da ROM de **Chrono Trigger** (`.sfc`, `.smc` ou `.zip`) na tela.
4. O jogo começará imediatamente a 60 FPS com áudio estéreo.

---

## 🎮 Controles

### Teclado (Padrão)
* **Setas Direcionais:** Mover o Crono
* **Z:** Botão A (Confirmar / Conversar)
* **X:** Botão B (Cancelar / Correr)
* **A:** Botão X (Menu de Itens e Techs)
* **S:** Botão Y (Ação secundária)
* **Q / W:** Botões L / R
* **Enter:** Start
* **Shift Direito:** Select

### Controle USB / Bluetooth (Xbox, PlayStation, etc.)
- O navegador detecta seu controle automaticamente via **Gamepad API**.
- Basta plugar o controle ou conectar via Bluetooth antes ou depois de carregar a ROM.
