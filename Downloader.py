import os
import boto3
import botocore
import pathlib
from dotenv import load_dotenv
load_dotenv()


# Configura las credenciales de AWS
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION')
)

# Nombre del bucket
bucket_name = 'consaludsil'

# "Carpeta" dentro del bucket
folder_name = 'documentos_extraidos/'

# Directorio de descargas
download_dir = os.path.expanduser("~/descargas_CONS")

# Si no existe, crea el directorio de descargas
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Solicitar al usuario el nombre del archivo
file_name = input("Ingrese el nombre del archivo a buscar (dejar en blanco para buscar todos los archivos PDF): ")

try:
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    for obj in response['Contents']:
        # Filtra los archivos que estén dentro de la "carpeta" y tengan extensión .pdf y que contengan el nombre proporcionado
        if obj['Key'].endswith('.pdf') and (file_name == '' or file_name in obj['Key']):
            # Descarga el archivo
            file_path = os.path.join(download_dir, pathlib.Path(obj['Key']).name)
            s3.download_file(bucket_name, obj['Key'], file_path)
            print(f"Archivo descargado: {file_path}")
            # Abre el archivo automáticamente
            os.system(f"open {file_path}")  # Esto funciona en sistemas MacOS
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'AccessDenied':
        print("Error: Acceso denegado.")
    elif e.response['Error']['Code'] == 'NoSuchBucket':
        print("Error: El bucket no existe.")
    else:
        print("Error desconocido:", e)
