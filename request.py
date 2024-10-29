import requests
import json
import sqlite3

# Configurações da API
API_BASE_URL = 'http://127.0.0.1:8000'
LOGIN_ENDPOINT = '/login'
EXTRACT_ENDPOINT = '/extrair'

# Credenciais de login
credentials = {
    'username': 'admin',
    'password': 'password'
}

# Parâmetros para extração de dados
params = {
    'ano': '2023',
    'opcao': 'opcao_exemplo',
    'subopcao': 'subopcao_exemplo'
}

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Cria a tabela se não existir (ajuste os campos conforme sua necessidade)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados_extracao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conteudo TEXT NOT NULL
    )
''')
conn.commit()

try:
    # 1. Realiza o login para obter o token JWT
    login_response = requests.post(f"{API_BASE_URL}{LOGIN_ENDPOINT}", json=credentials)
    login_response.raise_for_status()  # Lança uma exceção para códigos de status HTTP de erro
    access_token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}

    # 2. Faz a requisição ao endpoint protegido '/extrair'
    extract_response = requests.get(f"{API_BASE_URL}{EXTRACT_ENDPOINT}", headers=headers, params=params)
    extract_response.raise_for_status()
    dados = extract_response.json()

    # 3. Armazena os dados no banco de dados
    # Supondo que 'dados' é uma lista de dicionários
    for item in dados:
        cursor.execute('INSERT INTO dados_extracao (conteudo) VALUES (?)', (json.dumps(item),))
    conn.commit()
    print("Dados armazenados com sucesso no banco de dados.")

except requests.exceptions.HTTPError as http_err:
    print(f"Erro HTTP: {http_err}")
except Exception as err:
    print(f"Ocorreu um erro: {err}")
finally:
    conn.close()