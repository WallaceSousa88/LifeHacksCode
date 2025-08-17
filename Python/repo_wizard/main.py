import os
import sys
import stat
import time
import shutil
import datetime
import subprocess

def get_desktop():
    return os.path.join(os.path.expanduser('~'), 'Desktop')

def clone_repo(url):
    path = get_desktop()
    try:
        subprocess.run(['git', 'clone', url], cwd=path, check=True, capture_output=True, text=True)
        print("Repositório clonado com sucesso.")
    except subprocess.CalledProcessError as e:
        print("Erro ao clonar repositório:", e.stderr)
        sys.exit(1)

def zip_folder(folder_name='Nova Pasta'):
    path = get_desktop()
    folder = os.path.join(path, folder_name)
    date_str = datetime.datetime.now().strftime('%d_%m_%y')
    base_zip_name = f"{date_str}.zip"
    zip_path = os.path.join(path, base_zip_name)

    counter = 1
    while os.path.exists(zip_path):
        zip_path = os.path.join(path, f"{date_str}_{counter}.zip")
        counter += 1

    try:
        temp_zip = shutil.make_archive(folder, 'zip', folder)
        os.rename(temp_zip, zip_path)
        print(f'Pasta compactada como {os.path.basename(zip_path)}.')
    except Exception as e:
        print("Erro ao compactar pasta:", str(e))

def move_and_push():
    desktop = get_desktop()
    archive = os.path.join(desktop, 'Archive')
    zip_folder = os.path.join(archive, 'zip')

    for file in os.listdir(desktop):
        if file.endswith('.zip'):
            src = os.path.join(desktop, file)
            dst = os.path.join(zip_folder, file)
            try:
                shutil.move(src, dst)
                print(f'{file} movido para a pasta zip.')
            except Exception as e:
                print(f'Erro ao mover {file}:', str(e))

    try:
        subprocess.run(['git', 'add', '.'], cwd=archive, check=True)
        subprocess.run(['git', 'commit', '-m', 'add zip'], cwd=archive, check=True)
        subprocess.run(['git', 'push'], cwd=archive, check=True)
        print('Alterações enviadas ao repositório com sucesso.')
        time.sleep(10)

    except subprocess.CalledProcessError as e:
        print('Erro ao executar comandos Git:', e.stderr)

def clean_desktop():
    desktop = get_desktop()
    archive = os.path.join(desktop, 'Archive')
    nova_pasta = os.path.join(desktop, 'Nova Pasta')

    for file in os.listdir(desktop):
        if file.endswith('.zip'):
            try:
                os.remove(os.path.join(desktop, file))
                print(f'{file} apagado da área de trabalho.')
            except Exception as e:
                print(f'Erro ao apagar {file}:', str(e))

    def handle_exception(func, path, exc_info):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception as e:
            print(f'Erro ao forçar remoção de {path}:', str(e))

    if os.path.exists(archive):
        try:
            shutil.rmtree(archive, onexc=handle_exception)
            print('Pasta Archive apagada com sucesso.')
        except Exception as e:
            print('Erro ao apagar a pasta Archive:', str(e))

    if os.path.exists(nova_pasta):
        try:
            shutil.rmtree(nova_pasta, onexc=handle_exception)
            print('Pasta "Nova Pasta" apagada com sucesso.')
        except Exception as e:
            print('Erro ao apagar a pasta "Nova Pasta":', str(e))


def log_step(step_name, func, *args, **kwargs):
    print(f"\nIniciando: {step_name}...")
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start_time
    print(f"Finalizado: {step_name} em {elapsed:.2f} segundos.")
    return result

log_step("Clonagem do repositório", clone_repo, "x")
log_step("Compactação da pasta", zip_folder)
log_step("Movimentação e push", move_and_push)
log_step("Limpeza da área de trabalho", clean_desktop)
