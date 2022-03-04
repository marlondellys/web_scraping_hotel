import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import os

usuario = os.getlogin()
df_geral = pd.DataFrame()

# --------------------------------
# [BAIRROS QUE IREI REALIZAR A PROCURA]
# --------------------------------
bairros = [
    'pinheiros',
    'vila-madalena',
    'bela-vista'
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
    link_requisicao = f'https://www.quintoandar.com.br/alugar/imovel/{bairro}-sao-paulo-sp-brasil/de-500-a-2000-aluguel/proximo-ao-metro'
    response = requests.get(link_requisicao)
    response = response.text
    soup = BeautifulSoup(response, 'html.parser')

    # PROCURANDO OS ELEMENTOS:
    get_url_anuncio = [url_base + n['href'] for n in soup.find_all('a', class_ = 'sc-15oj7uq-0 iOyGjI')]
    get_rua = [n.get_text() for n in soup.find_all('p', attrs = {'data-testid': 'house-card-address'})]
    get_cidade = [n.get_text() for n in soup.find_all('p', attrs = {'data-testid': 'house-card-region'})]
    get_valor = [str(n.get_text()[9:]).strip().replace('.', '') for n in soup.find_all('p', class_ = 'sc-pGacB kCvCZV sc-jrAFXE dmnSCg CozyTypography')]
    get_url_imagem = [url_base + n['src'] for n in soup.find_all('img', class_ = 'sc-1tws8s7-1 kvoNyn')]
    
    # DETERMINANDO CONTROLE
    zipagem = zip(
        get_cidade,
        get_rua,
        get_valor,
        get_url_anuncio,
        get_url_imagem
    )

    # TRATANDO OS ZIPS
    unzipped_object = zip(*zipagem)
    unzipped_object = list(unzipped_object)
    agora = dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    # DATAFRAME
    try:
        df = pd.DataFrame(
            {
                'usuario': usuario,
                'data-execução': agora,
                'bairro_pesquisa': bairro,
                'cidade': unzipped_object[0],
                'rua': unzipped_object[1],
                'valor': unzipped_object[2],
                'url_anuncio': unzipped_object[3],
                'url_imagem': unzipped_object[4]
            }
        )
        df_geral = df_geral.append(df)

    except:
        continue
    
    print(f'Relatório {bairro} - gerado com sucesso!')

df_geral.to_excel('relatório_consolidado.xlsx', index=False)
print('----------------------------------------FIM-----------------------------------------')

""""
anuncios:       <div> class: sc-1qwl1yl-0 dZQOEt                        
link_Anuncio:   <a> class: sc-15oj7uq-0 iOyGjI - ['href']                      OK
rua:            <p> class: sc-pGacB kIfXDx sc-jrAFXE dmnSCg CozyTypography     PROBLEMA (2 BRANCOS)
cidade:         <p> class: sc-pGacB jYyyno sc-jrAFXE dmnSCg CozyTypography     PROBLEMA (2 BRANCOS)
valor:          <p> class: sc-pGacB kCvCZV sc-jrAFXE dmnSCg CozyTypography     PROBLEMA (2 BRANCOS)
imagem:         <div> class: sc-1tws8s7-0 gnCXVl - ['src']                      OK
link01:         https://www.quintoandar.com.br/alugar/imovel/{bairro}-sao-paulo-sp-brasil/de-500-a-2000-aluguel/mobiliado/proximo-ao-metro
link02:         https://www.quintoandar.com.br/alugar/imovel/{bairro}-sao-paulo-sp-brasil/apartamento/kitnet/de-500-a-2000-aluguel/1-2-3-4-quartos/mobiliado/de-20-a-50-m2
"""