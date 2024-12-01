# Calculadora de Probabilidade Genética
# Autor: Amanda Caroline da Silva
# Data: 01/12/2024
# Versão: 0.0.1

from flask import Flask, render_template, request

import itertools

app = Flask(__name__)

def gerar_combinacoes(genotipo):
    return [
        "".join(comb)
        for comb in itertools.product(*[genotipo[i:i+2] for i in range(0, len(genotipo), 2)])
    ]

def calcular_probabilidade(gametas_pai, gametas_mae):
    combinacoes = ["".join(sorted(p + m)) for p,m in itertools.product(gametas_pai, gametas_mae)]
    total_comb = len(combinacoes)
    frequencia = {}

    for comb in combinacoes:
        if comb in frequencia:
            frequencia[comb] += 1
        
        else: 
            frequencia[comb] = 1

    probabilidades = {genotipo: freq/total_comb for genotipo, freq in frequencia.items()}
    return probabilidades

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular', methods=["POST"])
def calcular():
    genotipo_pai = request.form['genotipo_pai'].strip()
    genotipo_mae = request.form['genotipo_mae'].strip()
    
    if len(genotipo_pai) != len(genotipo_mae) or len(genotipo_pai)%2 != 0:
        return render_template('index.html', error='Os genótipos devem ter o mesmo tamanho e conter pares de alelos (ex.: Aa, Bb, etc.).')
    
    try: 
        gametas_pai = gerar_combinacoes(genotipo_pai)
        gametas_mae = gerar_combinacoes(genotipo_mae)

        probabilidades = calcular_probabilidade(gametas_pai, gametas_mae)

        resultados = [
            {
                "genotipo": genotipo,
                "frequencia": f'{probabilidade * 16:.0f}/16',
                "probabilidade": f"{probabilidade * 100:.2f}%"
            }
            for genotipo, probabilidade in sorted(probabilidades.items())
        ]

        return render_template('result.html', resultados=resultados)
    
    except Exception as e:
        return render_template('index.html', error=f'Ocorreu um erro: {e}')
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)