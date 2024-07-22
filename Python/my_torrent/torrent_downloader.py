# pip install aiotorrent rich

# Abra o terminal e execute o script com os seguintes argumentos:
# -d download_path: Caminho para salvar o download (opcional, padrão: diretório atual).
# -l download_limit: Limite de velocidade de download em bytes por segundo (opcional, padrão: sem limite).
# -u upload_limit: Limite de velocidade de upload em bytes por segundo (opcional, padrão: sem limite).

# Exemplo
# python torrent_downloader.py "caminho/para/arquivo.torrent" -d "caminho/para/salvar" -l 500000 -u 100000

import asyncio
import aiotorrent
from aiotorrent.client import Client
from aiotorrent.torrent import Torrent
import logging
import time
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

logging.basicConfig(filename='torrent_client.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()

async def download_torrent(torrent_file: str, download_path: str, download_limit: int, upload_limit: int = 0):
    async with Client(max_download_speed=download_limit, max_upload_speed=upload_limit) as client:
        try:
            torrent: Torrent = await client.add_torrent(torrent_file, download_path)
            logging.info(f"Torrent adicionado: {torrent.name}")
        except FileNotFoundError:
            console.print(f"[bold red]Erro: Arquivo torrent não encontrado: {torrent_file}[/]")
            logging.error(f"Arquivo torrent não encontrado: {torrent_file}")
            return
        except aiotorrent.exceptions.TorrentError as e:
            console.print(f"[bold red]Erro ao abrir o arquivo torrent:[/] {e}")
            logging.error(f"Erro ao abrir o arquivo torrent: {e}")
            return

        if len(torrent.files) > 1:
            console.print("[bold blue]Arquivos disponíveis:[/]")
            for i, file in enumerate(torrent.files):
                console.print(f"{i + 1}. {file.name}")

            selected_files = input("Selecione os arquivos para baixar (separe por vírgulas, ou 'todos'): ")
            if selected_files.lower() != 'todos':
                try:
                    selected_indices = [int(x.strip()) - 1 for x in selected_files.split(',')]
                    for i, file in enumerate(torrent.files):
                        if i not in selected_indices:
                            file.download = False
                except Exception as e:
                    console.print(f"[bold red]Erro na seleção de arquivos:[/] {e}")
                    logging.error(f"Erro na seleção de arquivos: {e}")
                    return

        with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                "•",
                DownloadColumn(),
                "•",
                TransferSpeedColumn(),
                "•",
                TimeRemainingColumn(),
                console=console,
        ) as progress:
            task = progress.add_task(f"[blue]{torrent.name}", total=torrent.total_size)

            table = Table(title=f"[bold]{torrent.name}[/]")
            table.add_column("Info", style="cyan", width=12)
            table.add_column("Valor")
            table.add_row("Tamanho:", f"{torrent.total_size / (1024 * 1024):.2f} MB")
            table.add_row("Peers:", f"{len(torrent.peers)}")
            table.add_row("Status:", f"{'Baixando' if torrent.is_downloading else 'Pausado'}")
            console.print(Panel(table))

            while not torrent.is_finished:
                await asyncio.sleep(1)
                progress.update(task, advance=torrent.downloaded - progress.tasks[0].completed)

                table.rows[2].cells[1].text = f"{len(torrent.peers)}"
                table.rows[3].cells[1].text = f"{'Baixando' if torrent.is_downloading else 'Pausado'}"
                console.print(Panel(table), end="\r")

                if not torrent.is_seeding and not torrent.is_downloading:
                    console.print("Download pausado. Pressione Enter para continuar...")
                    input()
                    await torrent.start()

            console.print(f"[bold green]Download completo![/] Salvo em: {download_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Baixe arquivos torrent.")
    parser.add_argument("torrent_file", type=str, help="Caminho para o arquivo .torrent")
    parser.add_argument(
        "-d",
        "--download_path",
        type=str,
        default=".",
        help="Caminho para salvar o download (padrão: diretório atual)",
    )
    parser.add_argument(
        "-l",
        "--download_limit",
        type=int,
        default=0,
        help="Limite de velocidade de download em bytes por segundo (padrão: sem limite)",
    )
    parser.add_argument(
        "-u",
        "--upload_limit",
        type=int,
        default=0,
        help="Limite de velocidade de upload em bytes por segundo (padrão: sem limite)",
    )
    args = parser.parse_args()

    asyncio.run(
        download_torrent(args.torrent_file, args.download_path, args.download_limit, args.upload_limit)
    )
