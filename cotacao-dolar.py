from PyQt5 import uic,QtWidgets
import requests

# Inserir o valor em Reais
valor = float(input('Digite o valor em Reais para saber quantos Doláres pode comprar: ').replace(',','.'))

# Data cotação do dólar
data = input('Digite a data(mês-dia-ano) que deseja ver a cotação (ex:04-28-2024): ')

# API para cotação do dólar
url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data}'&$top=100&$format=json"

# Fazendo a requisição GET
response = requests.get(url)

# Verificando o status da resposta
if response.status_code == 200:
    # Convertendo a resposta em JSON
    data = response.json()
    # Exibindo o JSON obtido
    print(data)
else:
    print(f"Erro na requisição: {response.status_code}")

# Selecionando dados de Compra e Venda 
compra = data["value"][0]["cotacaoCompra"]
venda = data["value"][0]["cotacaoVenda"]

# Calculando quantidade de dólares e formatando o resultado
dolares = (valor / compra)
dolares_format = f'{dolares:.2f}'.replace('.',',')


# Resultado final
print(f'Valor de Compra: R$ {compra}')
print(f'Valor de Venda: R$ {venda}')

print(f"Com R${str(valor).replace('.',',')} Reais você pode comprar ${dolares_format} Dólares.")
