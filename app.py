from flask import Flask, render_template, url_for, request
from operacoes import scrapping,usar_api, coletarBandeiras, nomeBanco, limpar_dict

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        limpar_dict()
        trimestre = '20221'
        funcaoCartao = 'Débito'
        banco = request.form['banco']
        nome_completo_banco = nomeBanco(banco)
        bandeiras = coletarBandeiras(nome_completo_banco)
        info = scrapping(banco)
        dicionario = usar_api(trimestre, bandeiras, funcaoCartao)
        return render_template("menu.html",info = info, dicionarios = dicionario, nome_banco = nome_completo_banco)
    else:
        return render_template("index.html")

@app.route('/menu', methods=['GET','POST'])
def menu():
    return render_template("menu.html")

if __name__ == "__main__":
    app.run(debug=True)