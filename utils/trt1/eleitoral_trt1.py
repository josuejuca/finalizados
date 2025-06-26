from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import random


def espera_humana(seg_min=1, seg_max=2):
    t = random.uniform(seg_min, seg_max)
    print(f"⌛ Aguardando {t:.1f} segundos...")
    time.sleep(t)


def emitir_certidao_eleitoral(cpf: str, id_registro: str):
    print(f"🚀 Iniciando emissão da certidão cível para CPF {cpf} e ID {id_registro}...")

    # Configurações do navegador Opera no Selenoid
    capabilities = {
        "browserName": "opera",
        "browserVersion": "109.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "name": f"Certidão TRF1 - CPF {cpf}",
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
        print("🔗 Acessando o site do TRF1...")
        driver.get("https://sistemas.trf1.jus.br/certidao/#/solicitacao")
        espera_humana(5, 7)

        # Tipo de Certidão: Cível
        print("📝 Selecionando certidão: Cível...")
        wait.until(EC.element_to_be_clickable((By.ID, "mat-select-0"))).click()
        espera_humana()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-option//span[text()=' Para fins eleitorais ']"))).click()
        espera_humana()

        # Órgão: DF
        print("📝 Selecionando órgão emissor: DF...")
        orgao_input = wait.until(EC.element_to_be_clickable((By.ID, "mat-chip-list-input-0")))
        orgao_input.click()
        espera_humana()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//mat-option//span[contains(text(),'SEÇÃO JUDICIÁRIA DO DISTRITO FEDERAL')]"))
        ).click()
        espera_humana()
        orgao_input.send_keys(Keys.ESCAPE)
        espera_humana()

        # CPF
        print(f"📝 Preenchendo CPF: {cpf}...")
        cpf_input = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        cpf_input.clear()
        cpf_input.send_keys(cpf)
        espera_humana()

        # Emitir
        print("🚀 Emitindo a certidão...")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button//span[contains(text(),'Emitir Certidão')]"))
        ).click()

        espera_humana(5, 8)

        print("🖨️ Aguardando botão 'Imprimir'...")
        imprimir_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button//span[contains(text(),'Imprimir')]"))
        )
        espera_humana()
        imprimir_btn.click()

        espera_humana(3, 5)

        # Troca para aba do PDF
        print("🗂️ Trocando para a aba do PDF...")
        driver.switch_to.window(driver.window_handles[-1])
        espera_humana(2, 3)

        pdf_url = driver.current_url
        print(f"ℹ️ URL do PDF (esperado blob): {pdf_url}")

        # Injetar script JS para upload
        print("🚀 Injetando script JS para enviar o PDF para a API...")

        driver.execute_script("""
        fetch(arguments[0])
            .then(r => r.blob())
            .then(blob => {
                const formData = new FormData();
                formData.append('file', blob, arguments[1]);

                fetch(arguments[2], {
                    method: 'POST',
                    body: formData
                })
                .then(r => r.json())
                .then(data => console.log('Arquivo enviado!', data))
                .catch(err => console.error(err));
            });
        """, pdf_url, f"eleitoral_{cpf}.pdf", f"https://api-dev-imogo.juk.re/upload/bot/{id_registro}")

        print("✅ PDF enviado.")       

    except Exception as e:
        print(f"❌ Erro: {e}")

    finally:
        
        print("🛑 Navegador fechado.")


