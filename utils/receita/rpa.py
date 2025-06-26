import pyautogui
import time
import random
import webbrowser
import os
import pyperclip
import shutil

# Caminho base do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # Sobe duas pastas

def gerar_nome_arquivo(cpf, id_emisssao):
    return f"{id_emisssao}_{cpf}_receita.pdf"

def arquivo_existe(nome_arquivo, docs_relativo="./rpa"):
    docs_path = os.path.abspath(os.path.join(BASE_DIR, docs_relativo))
    file_path = os.path.join(docs_path, nome_arquivo)
    return os.path.exists(file_path), file_path

def mover_arquivo(origem, id_emisssao):
    destino_dir = os.path.join(BASE_DIR, "certidoes_bot", str(id_emisssao))
    os.makedirs(destino_dir, exist_ok=True)
    destino_path = os.path.join(destino_dir, os.path.basename(origem))
    shutil.move(origem, destino_path)
    return destino_path

def receita_cpf(cpf, id_emisssao):
    novo_nome_arquivo = gerar_nome_arquivo(cpf, id_emisssao)
    url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir"
    webbrowser.open(url)
    time.sleep(10)

    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.write(cpf, interval=0.1)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(10)

    pyautogui.write(novo_nome_arquivo, interval=0.1)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)

    existe, caminho_arquivo = arquivo_existe(novo_nome_arquivo)
    if not existe:
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(1)
        nova_url = f"https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni={cpf}"
        pyperclip.copy(nova_url)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(10)

        pyautogui.write(novo_nome_arquivo, interval=0.1)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(5)
        
        existe, caminho_arquivo = arquivo_existe(novo_nome_arquivo)
        if not existe:
            return {
                "status": "erro",
                "mensagem": "Arquivo não foi gerado. Verifique o processo manualmente."
            }

    # Move para a pasta correta
    novo_caminho = mover_arquivo(caminho_arquivo, id_emisssao)

    # Fecha o navegador (Alt + F4)
    time.sleep(2)  # Pequena pausa antes de fechar
    pyautogui.hotkey('alt', 'f4')
    return {
        "status": "sucesso",
        "arquivo": os.path.basename(novo_caminho),
        "arquivo_path": novo_caminho,
        "tipo_doc": "RECEITA",
    }

if __name__ == "__main__":
    print(receita_cpf("09240380124", "23"))
