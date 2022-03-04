import requests
from bs4 import BeautifulSoup
import pandas as pd

# --------------------------------
# [BAIRROS QUE IREI REALIZAR A PROCURA]
# --------------------------------
bairros = [
    'centro',
    'pinheiros',
    'vila-madalena',
    'butantã',
    'consolação',
    'bela-vista',
    'sumaré',
    'vila-pompeia',
]

# --------------------------------
# [LINKS ÚTEIS PARA O PROGRAMA]
# --------------------------------
url_base = 'https://www.quintoandar.com.br'
url_procura = 'https://www.quintoandar.com.br/alugar/imovel/%s-sao-paulo-sp-brasil/de-500-a-2000-aluguel/mobiliado/proximo-ao-metro'

# --------------------------------
# [INÍCIO DA EXECUÇÃO]
# --------------------------------
for bairro in bairros:
    # REALIZANDO A REQUISIÇÃO
    response = requests.get(url_procura%bairro)
    response = response.text
    soup = BeautifulSoup(response, 'html')

    # PROCURANDO OS ELEMENTOS:
    get_url_anuncio = [url_base + n['href'] for n in soup.find_all('a', class_ = 'sc-15oj7uq-0 iOyGjI')]
    get_rua = [n.get_text() for n in soup.find_all('p', class_ = 'sc-pGacB kIfXDx sc-jrAFXE dmnSCg CozyTypography')]
    get_cidade = [n.get_text() for n in soup.find_all('p', class_ = 'sc-pGacB jYyyno sc-jrAFXE dmnSCg CozyTypography')]
    get_valor = [str(n.get_text()[9:]).strip().replace('.', '') for n in soup.find_all('p', class_ = 'sc-pGacB kCvCZV sc-jrAFXE dmnSCg CozyTypography')]
    get_url_imagem = [url_base + n['src'] for n in soup.find_all('img', class_ = 'sc-1tws8s7-1 kvoNyn')]

    # DEIXANDO AS LISTAS DO MESMO TAMANHO PARA RESOLVER PROBLEMA DOS VAZIOS:
    get_rua = get_rua[:-2]
    get_cidade = get_cidade[:-2]
    get_valor = get_valor[:-2]

    # TESTANDO
    with open('arquivo_teste.txt', 'w') as arq:
        arq.writelines(f'{get_url_anuncio}\n{get_rua}\n{get_cidade}\n{get_valor}\n{get_url_imagem}\n')
        arq.close()

    # DATAFRAME
    df = pd.DataFrame({
        'Cidade': get_cidade,
        'Rua': get_rua,
        'Valor': get_valor,
        'URL_Anúncio': get_url_anuncio,
        'URL_Imagem': get_url_imagem,
    })

    df.to_excel(f'relatório_bairro_{bairro}.xlsx', index=False)
    print('Relatório exportado com sucesso...!')

""""
anuncios:       <div> class: sc-1qwl1yl-0 dZQOEt                        
link_Anuncio:   <a> class: sc-15oj7uq-0 iOyGjI - ['href']                       OK
rua:            <p> class: sc-pGacB kIfXDx sc-jrAFXE dmnSCg CozyTypography     PROBLEMA (2 BRANCOS)
cidade:         <p> class: sc-pGacB jYyyno sc-jrAFXE dmnSCg CozyTypography      PROBLEMA (2 BRANCOS)
valor:          <p> class: sc-pGacB kCvCZV sc-jrAFXE dmnSCg CozyTypography                                 PROBLEMA (2 BRANCOS)
imagem:         <div> class: sc-1tws8s7-0 gnCXVl - ['src']                      OK
"""