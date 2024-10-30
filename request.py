import requests
import csv

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
    'opcao': 'opt_03',
    'subopcao': 'subopt_01'
}

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

    # 3. Constrói o nome do arquivo CSV usando os parâmetros da API
    nome_arquivo_csv = f"dados_extracao_{params['ano']}_{params['opcao']}_{params['subopcao']}.csv"

    # 4. Armazena os dados em um arquivo CSV com o nome gerado
    if isinstance(dados, list) and len(dados) > 0 and isinstance(dados[0], dict):
        fieldnames = dados[0].keys()
        with open(nome_arquivo_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dados)
        print(f"Dados armazenados com sucesso no arquivo CSV: {nome_arquivo_csv}")
    else:
        print("Nenhum dado para armazenar ou formato de dados inválido.")

except requests.exceptions.HTTPError as http_err:
    print(f"Erro HTTP: {http_err}")
except Exception as err:
    print(f"Ocorreu um erro: {err}")