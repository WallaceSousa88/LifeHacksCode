import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Permite SharedArrayBuffer e isolamento de alta performance para WASM
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def run_server():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), CustomHTTPHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print(" [CHRONO TRIGGER - WEBASSEMBLY SNES ENGINE]")
        print(f" Servidor local ativo em: {url}")
        print(" Pressione Ctrl+C para encerrar o servidor.")
        print("=" * 60)
        
        # Tenta abrir o Microsoft Edge diretamente
        try:
            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            if not os.path.exists(edge_path):
                edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            
            if os.path.exists(edge_path):
                import subprocess
                subprocess.Popen([edge_path, url])
            else:
                webbrowser.open(url)
        except Exception:
            webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
            sys.exit(0)

if __name__ == "__main__":
    run_server()
