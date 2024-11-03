import base64
import platform
import os
import time
import requests
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

def create_driver_selenium():
    options = get_chrome_browser_options()  # Use the method to get Chrome options

    chrome_install = ChromeDriverManager().install()
    folder = os.path.dirname(chrome_install)
    if platform.system() == "Windows":
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
    else:
        chromedriver_path = os.path.join(folder, "chromedriver")
    service = ChromeService(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=options)

def HTML_to_PDF(FilePath):
    gotenberg_url = os.getenv("GOTENBERG_URL")
    if not gotenberg_url:
        raise ValueError("A variável de ambiente 'GOTENBERG_URL' não está definida.")
    gotenberg_uri = f"{gotenberg_url}/forms/chromium/convert/html"

    if not os.path.isfile(FilePath):
        raise FileNotFoundError(f"O arquivo especificado não existe: {FilePath}")

    # Prepara os arquivos para envio
    files = [
        ('files', ('index.html', open(FilePath, 'rb'), 'text/html'))
    ]

    # Opções para personalizar a geração do PDF
    data = {
        'paperWidth': '8.27',      # Largura A4 em polegadas
        'paperHeight': '11.69',    # Altura A4 em polegadas
        'marginTop': '0.8',
        'marginBottom': '0.8',
        'marginLeft': '0.5',
        'marginRight': '0.5',
        'printBackground': 'true',
        'preferCssPageSize': 'true',
    }

    try:
        response = requests.post(gotenberg_uri, files=files, data=data)
        response.raise_for_status()
        pdf_base64 = base64.b64encode(response.content).decode('utf-8')
        return pdf_base64
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Falha ao converter HTML para PDF: {e}")
    finally:
        try:
            for file_tuple in files:
                if hasattr(file_tuple[1][1], 'close'):
                    file_tuple[1][1].close()
        except Exception as e:
            print(f"Erro ao fechar o arquivo: {e}")

def get_chrome_browser_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Avvia il browser a schermo intero
    options.add_argument("--no-sandbox")  # Disabilita la sandboxing per migliorare le prestazioni
    options.add_argument("--disable-dev-shm-usage")  # Utilizza una directory temporanea per la memoria condivisa
    options.add_argument("--ignore-certificate-errors")  # Ignora gli errori dei certificati SSL
    options.add_argument("--disable-extensions")  # Disabilita le estensioni del browser
    options.add_argument("--disable-gpu")  # Disabilita l'accelerazione GPU
    options.add_argument("window-size=1200x800")  # Imposta la dimensione della finestra del browser
    options.add_argument("--disable-background-timer-throttling")  # Disabilita il throttling dei timer in background
    options.add_argument("--disable-backgrounding-occluded-windows")  # Disabilita la sospensione delle finestre occluse
    options.add_argument("--disable-translate")  # Disabilita il traduttore automatico
    options.add_argument("--disable-popup-blocking")  # Disabilita il blocco dei popup
    #options.add_argument("--disable-features=VizDisplayCompositor")  # Disabilita il compositore di visualizzazione
    options.add_argument("--no-first-run")  # Disabilita la configurazione iniziale del browser
    options.add_argument("--no-default-browser-check")  # Disabilita il controllo del browser predefinito
    options.add_argument("--single-process")  # Esegui Chrome in un solo processo
    options.add_argument("--disable-logging")  # Disabilita il logging
    options.add_argument("--disable-autofill")  # Disabilita l'autocompletamento dei moduli
    #options.add_argument("--disable-software-rasterizer")  # Disabilita la rasterizzazione software
    options.add_argument("--disable-plugins")  # Disabilita i plugin del browser
    options.add_argument("--disable-animations")  # Disabilita le animazioni
    options.add_argument("--disable-cache")  # Disabilita la cache
    #options.add_argument('--proxy-server=localhost:8081')
    #options.add_experimental_option("useAutomationExtension", False)  # Disabilita l'estensione di automazione di Chrome
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])  # Esclude switch della modalità automatica e logging

    options.add_argument("--single-process")  # Esegui Chrome in un solo processo
    return options

def printred(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")

def printyellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")
