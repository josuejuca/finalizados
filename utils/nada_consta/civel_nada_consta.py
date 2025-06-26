from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import requests
import os


def espera_humana(seg_min=1, seg_max=2):
    t = random.uniform(seg_min, seg_max)
    print(f"⌛ Aguardando {t:.1f} segundos...")
    time.sleep(t)


def emitir_civel_cnc_tjdft(cpf: str, nome: str, nome_mae: str, id_registro: str):
    print(f"🚀 Iniciando emissão da certidão CNC TJDFT para CPF {cpf}...")

    capabilities = {
        "browserName": "opera",
        "browserVersion": "109.0",
        "selenoid:options": {
            "enableVNC": False,
            "enableVideo": False,
            "name": f"Certidão CNC TJDFT - CPF {cpf}",
        },
        "operaOptions": {
            "binary": "/usr/bin/opera"
        }
    }

    driver = webdriver.Remote(
        command_executor="https://selenoid.juk.re/wd/hub",
        desired_capabilities=capabilities
    )

    wait = WebDriverWait(driver, 20)

    try:
        print("🔗 Acessando o site do CNC TJDFT...")
        driver.get("https://cnc.tjdft.jus.br/solicitacao-externa")
        espera_humana(5, 7)

        # CPF
        print(f"📝 Preenchendo CPF: {cpf}")
        cpf_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='CPF/CNPJ']")))
        cpf_input.clear()
        cpf_input.send_keys(cpf)
        espera_humana()

        # Nome
        print(f"📝 Preenchendo Nome: {nome}")
        nome_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Primeiro Nome']")))
        nome_input.clear()
        nome_input.send_keys(nome)
        espera_humana()

        # Tipo de certidão: Especial (Cível e Criminal)
        print("🔘 Selecionando Tipo de Certidão: Cível")
        radio_criminal = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@role='radio' and @aria-label='Cível']")))
        radio_criminal.click()
        espera_humana()

        # Próximo - Tela 1
        print("➡️ Clicando em 'Próximo' (1ª tela)...")
        proximo_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button//span[contains(text(),'Próximo')]")))
        proximo_btn.click()
        espera_humana(3, 5)

        # Nome da mãe
        print(f"📝 Preenchendo Nome da Mãe: {nome_mae}")
        nome_mae_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@aria-label='Nome da Mãe']")))
        nome_mae_input.clear()
        nome_mae_input.send_keys(nome_mae)
        espera_humana()

        # Próximo - Tela 2
        print("➡️ Clicando em 'Próximo' (2ª tela)...")
        proximo_btn_2 = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button//span[contains(text(),'Próximo')]")))
        proximo_btn_2.click()
        espera_humana(3, 5)

        print("✅ Formulário preenchido! Buscando PDF...")

        # Download do PDF
        download_link_elem = wait.until(EC.presence_of_element_located((
            By.XPATH, "//a[starts-with(@href, 'https://certidoes.tjdft.jus.br/certidoes')]"
        )))
        pdf_url = download_link_elem.get_attribute("href")
        print(f"✅ URL do PDF encontrada: {pdf_url}")

        # Faz o download do PDF
        print("⬇️ Baixando o PDF...")
        response = requests.get(pdf_url)

        if response.status_code == 200:
            # Pasta de saída
            pasta = f"certidoes_bot/{id_registro}"
            os.makedirs(pasta, exist_ok=True)

            filename = f"{pasta}/civel_cnc_tjdft_{cpf}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)

            print(f"✅ PDF salvo em: {filename}")

            # Envia o PDF para a API
            # print("🚀 Enviando PDF para a API...")
            # with open(filename, "rb") as file_data:
            #     files = {'file': (os.path.basename(filename), file_data)}
            #     response_upload = requests.post(
            #         f"https://api-dev-imogo.juk.re/upload/bot/{id_registro}",
            #         files=files
            #     )

            # if response_upload.status_code in [200, 201]:
            #     print(f"✅ PDF enviado com sucesso para o ID {id_registro}")
            # else:
            #     print(f"⚠️ Falha no upload. Status: {response_upload.status_code}")

        else:
            print(f"⚠️ Erro ao baixar PDF. Status HTTP: {response.status_code}")

    except Exception as e:
        print(f"❌ Erro durante o processo: {e}")

    finally:
        driver.quit()
        print("🛑 Navegador fechado.")
