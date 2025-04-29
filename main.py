import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

# Conexão com o Azure Blob
blobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')
blobAccountName = os.getenv('BLOB_ACCOUNT_NAME')

# Conexão com o Banco SQL
sqlServer = os.getenv('SQL_SERVER')
sqlDatabase = os.getenv('SQL_DATABASE')
sqlUser = os.getenv('SQL_USER')
sqlPassword = os.getenv('SQL_PASSWORD')

# PAGINA DE CADASTRO
st.title('Cadastro de Produtos')

product_name = st.text_input('Nome do Produto')
product_price = st.number_input('Preço do Produto', min_value=0.0, format='%.2f')
product_description = st.text_area('Descrição do Produto')
product_image = st.file_uploader('Imgem do Produto', type=['jpg','png','jpeg'])

#FUNCAO DE UPLOAD DA IMAGEM DO PRODUTO no BLOB
def upload_product_image_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"

# INSERE PRODUTO NA TABELA
def insert_product(product_name,product_price,product_description,product_image):
    try:

        image_url= upload_product_image_blob(product_image)
        conn = pymssql.connect(server=sqlServer, user=sqlUser, password=sqlPassword, database=sqlDatabase)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO dbo.Produtos (nome, preco, descricao, image_url) VALUES ('{product_name}', '{product_price}', '{product_description}','{image_url}')")
        conn.commit()
        conn.close()

        return True
    except Exception as e:

        st.error(f'Erro ao inserir o produto na tabela: `{e}')
        return False

# LISTA PRODUSTO DA TABELA
def list_products():
    try:

        conn = pymssql.connect(server=sqlServer, user=sqlUser, password=sqlPassword, database=sqlDatabase)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    except Exception as e:
        
        st.error(f'Erro em listar os Produtos: {e}')
        return[]

def list_products_screen():
    products = list_products()
    for prodct in products:
        st.write(f'Nome: {prodct[1]}')
        st.write(f'Preco: {prodct[2]}')
        st.write(f'Descricao: {prodct[3]}')
        st.image(product[4], width=200)

if st.button('Salvar Produto'):
    insert_product(product_name,product_price,product_description,product_image)
    return_message = 'Produto salvo com sucesso'

st.header('Produtos Cadastrados')

if st.button('Listar Produtos'):
    list_products_screen()
    return_message = 'Produtos Listados com Sucesso'