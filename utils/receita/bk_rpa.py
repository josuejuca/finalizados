import pyautogui
import time
import random
import webbrowser
import os
import pyperclip  # Certifique-se de instalar: pip install pyperclip

def gerar_nome_arquivo(cpf, id_emisssao):
    """
    Gera um nome de arquivo único a partir do CPF, usando um ID aleatório.
    """
    id_aleatorio = random.randint(1000, 9999)
    
    return f"{id_emisssao}_{cpf}_receita.pdf"

def arquivo_existe(nome_arquivo, docs_relativo="./rpa"):
    """
    Verifica se o arquivo existe na pasta especificada.
    """
    docs_path = os.path.abspath(os.path.join(os.getcwd(), docs_relativo))
    file_path = os.path.join(docs_path, nome_arquivo)
    return os.path.exists(file_path), file_path

def receita_cpf(cpf, id_emisssao):
    """
    Executa o fluxo RPA utilizando o CPF informado.
    Abre o site da Receita Federal, preenche o CPF, tenta salvar o arquivo e verifica se ele foi criado.
    Caso o arquivo não seja gerado na primeira tentativa, utiliza uma segunda abordagem.
    
    Retorna um dicionário com o status do processo e informações do arquivo gerado.
    """
    # Gera o nome do arquivo com base no CPF
    novo_nome_arquivo = gerar_nome_arquivo(cpf, id_emisssao)
    
    # Acessa o site para emissão da certidão
    url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir"
    webbrowser.open(url)
    time.sleep(10)  # Aguarda o carregamento do site

    # Navega até o campo de CPF e informa o CPF
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.write(cpf, interval=0.1)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(10)  # Aguarda a geração da certidão e abertura da caixa de salvamento

    # Primeira tentativa: preenche o nome do arquivo na caixa de salvamento
    pyautogui.write(novo_nome_arquivo, interval=0.1)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)  # Tempo para o arquivo ser salvo

    # Verifica se o arquivo foi criado
    existe, caminho_arquivo = arquivo_existe(novo_nome_arquivo)
    if not existe:
        # Se não foi gerado, tenta acessar uma nova URL para processamento
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(1)
        
        nova_url = f"https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni={cpf}"
        pyperclip.copy(nova_url)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(10)  # Aguarda o carregamento e a nova caixa de salvamento
        
        # Segunda tentativa de salvar o arquivo
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
    
    # Se o arquivo foi gerado com sucesso, retorna os dados conforme o módulo de exemplo
    return {
        "status": "sucesso",
        "arquivo": novo_nome_arquivo,
        "arquivo_url": f"http://local.juk.re:8000/files/{novo_nome_arquivo}",
        "tipo_doc": "RECEITA",
    }

if __name__ == "__main__":
    receita_cpf("09240380124", "14")
