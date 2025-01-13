from PyQt5 import uic,QtWidgets
import requests
import os
import sys

# Configurar caminho relativo para arquivos .ui
if getattr(sys, 'frozen', False):  # Verifica se está rodando como executável
    script_dir = sys._MEIPASS  # Diretório temporário onde os arquivos do executável estão
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script Python

ui_controle1 = os.path.join(script_dir, "controle1.ui")
ui_controle2 = os.path.join(script_dir, "controle2.ui")

def abrir_controle2():
    linha1 = formulario.lineEdit.text()  # Usuário insere o valor
    linha2 = formulario.lineEdit_2.text()  # Usuário insere a data
    linha1_format = float(linha1.replace(',', '.'))
    
    # API para cotação do dólar
    url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{linha2}'&$top=100&$format=json"

    # Fazendo a requisição GET
    response = requests.get(url)

    # Verificando o status da resposta
    if response.status_code == 200:
        # Convertendo a resposta em JSON
        data = response.json()
        # Exibindo o JSON obtido
        #print(data)
    else:
        print(f"Erro na requisição: {response.status_code}")

    # Selecionando dados de Compra e Venda 
    compra = data["value"][0]["cotacaoCompra"]
    venda = data["value"][0]["cotacaoVenda"]

    # Calculando quantidade de dólares e formatando o resultado
    dolares = linha1_format / compra
    dolares_format = f'{dolares:.2f}'.replace('.',',')

    # Torna o formulário inicial invisível
    formulario.hide()

    # Carrega e exibe o segundo formulário
    global formulario2
    formulario2 = uic.loadUi(ui_controle2)

    formulario2.label_7.setText(linha2)
    
    compra = str(compra)
    formulario2.label_8.setText(compra)

    venda = str(venda)
    formulario2.label_9.setText(venda)

    formulario2.label_10.setText(linha1)

    formulario2.label_11.setText(str(dolares_format))

    formulario2.show()


app=QtWidgets.QApplication([])
formulario=uic.loadUi(ui_controle1)

# Conecta o botão OK à função que abre o segundo formulário
formulario.pushButton.clicked.connect(abrir_controle2)

formulario.show()
app.exec()

# pyinstaller --onefile --noconsole --add-data "controle1.ui;." --add-data "controle2.ui;." seu_script.py
