# pip install pytests

import asyncio
import os
from torrent_downloader import download_torrent

async def test_download_torrent(tmpdir):
    """Testa o download de um arquivo torrent pequeno."""
    torrent_file = "caminho/para/seu/arquivo_de_teste.torrent"
    download_path = str(tmpdir.join("downloads"))
    download_limit = 1024 * 1024

    await download_torrent(torrent_file, download_path, download_limit)

    assert os.path.exists(download_path)

    nomes_arquivos_esperados = ["arquivo1.txt", "arquivo2.jpg"]
    tamanhos_arquivos_esperados = {
        "arquivo1.txt": 1234,
        "arquivo2.jpg": 5678,
    }

    for nome_arquivo in nomes_arquivos_esperados:
        caminho_completo = os.path.join(download_path, nome_arquivo)
        assert os.path.isfile(caminho_completo), f"Arquivo não encontrado: {nome_arquivo}"

    for nome_arquivo, tamanho_esperado in tamanhos_arquivos_esperados.items():
        caminho_completo = os.path.join(download_path, nome_arquivo)
        tamanho_real = os.path.getsize(caminho_completo)
        assert tamanho_real == tamanho_esperado, f"Tamanho do arquivo '{nome_arquivo}' incorreto. Esperado: {tamanho_esperado} bytes, Obtido: {tamanho_real} bytes"

