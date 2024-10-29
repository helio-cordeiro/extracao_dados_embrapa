import requests
from bs4 import BeautifulSoup
import time

def extrair_dados(ano, opcao, subopcao, max_retries=5, retry_delay=5):
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php'
    params = {
        'opcao': str(opcao),
        'subopcao': str(subopcao),
        'ano': str(ano),
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            tabela = soup.find('table', {'class': 'tb_base tb_dados'})

            if tabela:
                cabecalhos = [th.text.strip() for th in tabela.find_all('th')]
                if not cabecalhos:
                    return None

                dados_tabela = []
                for tr in tabela.find_all('tr')[1:]:
                    colunas = tr.find_all('td')
                    dados = [td.text.strip() for td in colunas]
                    if dados and len(cabecalhos) == len(dados):
                        item = dict(zip(cabecalhos, dados))
                        item['Ano'] = ano
                        item['Opcao'] = opcao
                        item['Subopcao'] = subopcao
                        dados_tabela.append(item)

                return dados_tabela
            else:
                return None

        except requests.exceptions.RequestException:
            time.sleep(retry_delay)
            continue

    return None
