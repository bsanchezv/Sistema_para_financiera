import os
from dotenv import load_dotenv

# Imprimir el directorio de trabajo actual
print("Directorio de trabajo actual:", os.getcwd())  

# Cargar variables de entorno desde el archivo .env

## Opción 1:

resultado = load_dotenv('./API_KEY.env') #Solo si tiene nombre el archivo. Debería ser solo .env

## Opción 2:

resultado = load_dotenv()

print("load_dotenv() result:", resultado)

# Obtener la API key de SendGrid

sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

print("API Key:", sendgrid_api_key)  # Para asegurarte de que se cargó correctamente
