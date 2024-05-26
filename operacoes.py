from bs4 import BeautifulSoup # Biblioteca para pegar informações de uma página HTML
import requests # Biblioteca para entrar em sites pela URL
import json
# parâmetros
# banco = 'caixa-economica-federal'
# trimestre = '20221'
# funcaoCartao = 'Débito'

# separando os valores coletados da api
info1 = 'qtdCartoesAtivos'
info2 = 'qtdTransacoesNacionais'
info3 = 'produto'
info4 = 'bandeira'




def nomeBanco(banco):
  bancos = {
    "Banco do Brasil": 'bb',
    "Caixa Econômica Federal": 'caixa-economica-federal',
    "Itaú Unibanco": 'itau',
    "Bradesco": 'bradesco',
    "Banco Santander": 'santander',
    "Safra": 'safra',
    "BTG Pactual": 'btg-pactual',
    "C6 Bank": 'c6',
    "Nubank": 'nubank',
    "Neon": 'banco-neon-sa',
    "Sofisa Direto": 'sofisa',
    "XP Investimentos": 'xp-investimentos-cctvm-sa',
    "Clear Corretora": 'clear-ctvm',
    "Rico Investimentos": 'rico-ctvm-sa',
    "Inter": 'intermedium',
    "Pagseguro": 'pagseguro',
    "Banco Pan": 'pan',
    "Banco BMG": 'bgm',
  }

  nome_completo = ''.join([i for i in bancos if bancos[i] == banco])
  return nome_completo

## ----------------WEB SCRAPING------------------##

def scrapping(banco):
    url = f'https://bancodata.com.br/relatorio/{banco}/'

    r = requests.get(url) # Pegando o código fonte do site pela URL
    soup = BeautifulSoup(r.text, "html.parser") # Organizando esse código HTML

    # Separando as informações que serão mostradas para o usuário
    informacoes = [
    'Publicação',
    'Lucro Líquido',
    'Patrimônio Líquido',
    'Ativo Total',
    'Captações',
    'Carteira de Crédito Classificada (R$)',
    'Patrimônio de Referência RWA (R$)',
    'Número de Agências',
    'Número de Pontos de Atendimento'
    ]

    # Criando um arquivo de .txt (ou abrindo se já existe)
    # e apagando seu conteúdo

    # w = write (escrever ou sobrescrever)
    # a = append (adicionar ao final do arquivo)

    # Criando arquivo .txt como append

    # Laço de repetição para encontrar todos os dados presentes
    # na div que contem a classe "main-info"
    n = 0
    info_dict = {}
    for x in soup.find_all("div", {"class": "main-info"}):
        info_dict[informacoes[n]] = x.strong.get_text().strip()
        n += 1
    return info_dict
  

## -------------COLETANDO A BANDEIRA------------------##

def coletarBandeiras(nome_completo_banco):
  banco_escolhido = nome_completo_banco
  modelo_lista_bandeiras = {
      'MasterCard': [
          'Bradesco',
          'Itaú Unibanco',
          'Banco do Brasil',
          'Banco Santander',
          'Nubank',
          'Banco Inter',
          'C6 Bank',
          'BTG Pactual',
          'Sofisa Direto',
          'XP Investimentos',
          'Inter',
          'Pagseguro',
          'Banco BMG'
      ],
      'Visa':       [
          'Banco do Brasil',
          'Banco Santander',
          'Caixa Econômica Federal',
          'Itaú Unibanco',
          'Safra',
          'Neon',
          'Rico Investimentos',
          'Pagseguro'
      ],
      'Elo': [
          'Banco do Brasil',
          'Bradesco',
          'Caixa Econômica Federal',
          'Pagseguro',
          'Banco Pan'
      ]
  }

  bandeirasBanco = []
  for bandeira in modelo_lista_bandeiras:
    for banco in modelo_lista_bandeiras[bandeira]:
      if banco_escolhido in modelo_lista_bandeiras[bandeira]:
        bandeirasBanco.append(bandeira)
        break
  
  return bandeirasBanco


## -------------USANDO API------------------##
info_importantes = []
dicionario = {}
def usar_api(trimestre, bandeiraLista, funcaoCartao):
  bandeira = bandeiraLista[0]
  dicionario[bandeira] = []

  # preparando para a recursividade
  trimestre_recursivo = trimestre
  bandeiraLista_recursivo = bandeiraLista
  funcaoCartao_recursivo = funcaoCartao

  # API
  link = f"https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/Quantidadeetransacoesdecartoes(trimestre=@trimestre)?@trimestre='{trimestre}'&$top=100&$filter=nomeBandeira%20eq%20'{bandeira}'%20and%20nomeFuncao%20eq%20'{funcaoCartao}'&$select=trimestre,nomeBandeira,nomeFuncao,qtdCartoesAtivos,qtdTransacoesNacionais,produto&$format=json"

  # Modificando os resultados da API
  request = requests.get(link) # pegando a resposta da API
  resposta = json.loads(request.text) # transformando o texto (string) em um dict
  valores = resposta["value"]

  # Trabalhando com a API
  for value in valores:
    for idx, val in value.items():

      # pegando apenas valores do trimestre 20231
      if val != trimestre:
        continue

      # salvando informações que serão usadas de comparativo
      adicionar = {}
      adicionar[info1] = value[info1]
      adicionar[info2] = value[info2]
      adicionar[info3] = value[info3]
      adicionar[info4] = bandeira
      info_importantes.append(adicionar)
  
      dicionario[bandeira].append(adicionar)

  if len(bandeiraLista) > 1:
    bandeiraLista.remove(bandeira)
    usar_api(trimestre_recursivo, bandeiraLista_recursivo, funcaoCartao_recursivo)
  
  return dicionario

def limpar_dict():
  dicionario.clear()


  




