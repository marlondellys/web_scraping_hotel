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

# --------------------------------
# [INÍCIO DA EXECUÇÃO]
# --------------------------------
for bairro in bairros:
    # REALIZANDO A REQUISIÇÃO
    response = requests.get('https://www.quintoandar.com.br/alugar/imovel/{bairro}-sao-paulo-sp-brasil/de-500-a-2000-aluguel/mobiliado/proximo-ao-metro')
    response = response.text
    soup = BeautifulSoup(response, 'html')

    # PROCURANDO OS ELEMENTOS:
    get_url_anuncio = [url_base + n['href'] for n in soup.find_all('a', class_ = 'sc-15oj7uq-0 iOyGjI')]
    get_rua = [n.get_text() for n in soup.find_all('p', class_ = 'sc-pGacB kIfXDx sc-jrAFXE dmnSCg CozyTypography')]
    get_cidade = [n.get_text() for n in soup.find_all('p', class_ = 'sc-pGacB jYyyno sc-jrAFXE dmnSCg CozyTypography')]
    get_valor = [str(n.get_text()[9:]).strip().replace('.', '') for n in soup.find_all('p', class_ = 'sc-pGacB kCvCZV sc-jrAFXE dmnSCg CozyTypography')]
    get_url_imagem = [url_base + n['src'] for n in soup.find_all('img', class_ = 'sc-1tws8s7-1 kvoNyn')]

    # DEIXANDO AS LISTAS DO MESMO TAMANHO PARA RESOLVER PROBLEMA DOS VAZIOS:
    x = zip(
        get_cidade, 
        get_rua, 
        get_valor, 
        get_url_anuncio,
        get_url_imagem
    )

    y = [list(x)]

    z = zip(y)

    resultados = []

    for n in z:
        resultados.append(n)
    
    # DATAFRAME
    df = pd.DataFrame(
        {
            'Cidade': [n for n in resultados[::][0]],
        }
    )

    df.to_excel(f'relatório_bairro_{bairro}.xlsx', index=False)
    print('Relatório exportado com sucesso...!')
    del x

""""
anuncios:       <div> class: sc-1qwl1yl-0 dZQOEt                        
link_Anuncio:   <a> class: sc-15oj7uq-0 iOyGjI - ['href']                      OK
rua:            <p> class: sc-pGacB kIfXDx sc-jrAFXE dmnSCg CozyTypography     PROBLEMA (2 BRANCOS)
cidade:         <p> class: sc-pGacB jYyyno sc-jrAFXE dmnSCg CozyTypography     PROBLEMA (2 BRANCOS)
valor:          <p> class: sc-pGacB kCvCZV sc-jrAFXE dmnSCg CozyTypography     PROBLEMA (2 BRANCOS)
imagem:         <div> class: sc-1tws8s7-0 gnCXVl - ['src']                      OK
"""