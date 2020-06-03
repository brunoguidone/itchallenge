import psutil
import requests
import time
from log import sendLogToES

# Modulos para criação da API
from flask import Flask, request, jsonify

# Importação de funcao da classe do banco de dados
from db import queryAllBreeds, queryBreedById, queryByTemperament, queryByOrigin, queryImgById, customQuery, \
    queryImgByHat, queryImgBySunglass

app = Flask(__name__)

sendLogToES(message="Inicializacao da API", severity="Debug", latency=0, category="background", route="background")


# Rota inicial da API
@app.route('/v1/cats', methods=['GET'])
def index():
    return jsonify({
        'message': 'Bem vindo'
    })


# Rota para erro de página não encontrada, erro 400
@app.errorhandler(404)
def page_not_found(e):
    # Registro de log
    sendLogToES(message="Tentativa de abertura de pagina incorreta. Erro 404.", severity="Error", latency=0,
                category="resposta", route="404")
    return jsonify({'message': 'Rota nao encontrada'}), 404


# Rota para listagem de todas as raças de gatos
@app.route('/v1/cats/breeds/all', methods=['GET'])
def getBreeds():
    # Iniciar contador de tempo de execução da função
    initialTime = time.clock()

    # Query e recuperação de valores do banco de dados

    queryCatBreeds = queryAllBreeds()

    # Registro de valores // Loop para varrer todas as raças
    breeds = []
    for cat in sorted(queryCatBreeds):
        breeds.append(dict(cat))

    # Ponto de calculo de tempo
    executionTime = time.clock() - initialTime

    # Registro de Log
    sendLogToES(message="Execucao da query para listar todas as raças", severity="Info", latency=executionTime,
                category="execucao", route="/v1/cats/breeds/all")

    return jsonify(breeds)


# Rota para buscar gatos por ID
@app.route('/v1/cats/breeds/info', methods=['GET'])
def getBreedByID():
    # Iniciar contador de tempo de execução da função
    initialTime = time.clock()

    # Variaveis de campos de query string
    breedId = request.args.get('breedId')

    try:
        # Recuperação de valores do banco de dados
        returnOfQuery = queryBreedById(breedId)

        # Verifica se o valor foi encontrado no banco
        if len(returnOfQuery) == 0:
            timeOfFirstValidation = time.clock() - initialTime
            sendLogToES(message="Valor não encontrado no banco de dados", severity="Debug",
                        latency=timeOfFirstValidation, category="execucao", route="/v1/cats/breeds/info")
            return jsonify({'mensagem': 'Valor não encontrado no banco de dados.'})
        else:
            # Salva os valores recuperados pela query // Loop para varrer todos os valores
            result = []
            for cat in sorted(returnOfQuery):
                result.append(dict(cat))

            # Ponto de calculo de tempo
            totalTime = time.clock() - initialTime

            # Registro de Log
            sendLogToES(message="Procura de raça de gato realizada", severity="Info", latency=totalTime,
                        category="execucao", route="/v1/cats/breeds/info")

            return jsonify(result)

    # Tratamento de exception
    except Exception:
        errorTime = time.clock() - initialTime
        sendLogToES(message="Não foi possivel efetuar a busca de gatos", severity="Error", latency=errorTime,
                    category="execucao", route="/v1/cats/breeds/info")
        return jsonify({'mensagem': 'Não foi possível efetuar a busca.'})


# Rota para buscar gatos por temperamentos
@app.route('/v1/cats/temperaments', methods=['GET'])
def getBreedByTemperament():
    # Iniciar contador de tempo de execução da função
    initialTime = time.clock()

    # Variaveis de campos de query string
    temperament = request.args.get('temperament')

    try:
        # Recuperação de valores do banco de dados
        returnOfQuery = queryByTemperament(temperament)

        # Verifica se o valor foi encontrado no banco
        if len(returnOfQuery) == 0:
            timeOfFirstValidation = time.clock() - initialTime
            sendLogToES(message="Valor nao encontrado no banco de dados", severity="Debug",
                        latency=timeOfFirstValidation, category="execucao", route="/v1/cats/temperaments")
            return jsonify({'mensagem': 'Valor nao encontrado no banco de dados.'})
        else:
            # Salva os valores recuperados pela query // Loop para varrer todos os valores
            result = []
            for cat in sorted(returnOfQuery):
                result.append(dict(cat))

            # Ponto de calculo de tempo
            totalTime = time.clock() - initialTime

            # Registro de Log
            sendLogToES(message="Procura de raça de gato realizada", severity="Info", latency=totalTime,
                        category="execucao", route="/v1/cats/temperaments")

            return jsonify(result)

    # Tratamento de exception
    except Exception:
        errorTime = time.clock() - initialTime
        sendLogToES(message="Não foi possivel efetuar a busca de gatos", severity="Error", latency=errorTime,
                    category="execucao", route="/v1/cats/temperaments")
        return jsonify({'mensagem': 'Não foi possível efetuar a busca.'})


# Rota para buscar gatos por origem
@app.route('/v1/cats/origins', methods=['GET'])
def getBreedByOrigin():
    # Iniciar contador de tempo de execução da função
    initialTime = time.clock()

    # Variaveis de campos de query string
    origin = request.args.get('origin')

    try:
        # Recuperação de valores do banco de dados
        returnOfQuery = queryByOrigin(origin)

        # Verifica se o valor foi encontrado no banco
        if len(returnOfQuery) == 0:
            timeOfFirstValidation = time.clock() - initialTime
            sendLogToES(message="Valor não encontrado no banco de dados", severity="Debug",
                        latency=timeOfFirstValidation, category="execucao", route="/v1/cats/origins")
            return jsonify({'mensagem': 'Valor não encontrado no banco de dados.'})
        else:
            # Salva os valores recuperados pela query // Loop para varrer todos os valores
            result = []
            for cat in sorted(returnOfQuery):
                result.append(dict(cat))

            # Ponto de calculo de tempo
            totalTime = time.clock() - initialTime

            # Registro de Log
            sendLogToES(message="Procura de raça de gato realizada", severity="Info", latency=totalTime,
                        category="execucao", route="/v1/cats/origins")

            return jsonify(result)

    # Tratamento de exception
    except Exception:
        errorTime = time.clock() - initialTime
        sendLogToES(message="Não foi possivel efetuar a busca de gatos", severity="Error", latency=errorTime,
                    category="execucao", route="/v1/cats/origins")
        return jsonify({'mensagem': 'Não foi possível efetuar a busca.'})


# Rota para procurar imagens - PLUS ao Projeto
@app.route('/v1/cats/searchimgs', methods=['GET'])
def searchimg():
    # Iniciar contador de tempo de execução da função
    initialTime = time.clock()

    # Variaveis de campos de query string
    breedId = request.args.get('breedId')
    hashat = request.args.get('hashat')
    hassunglass = request.args.get('hassunglass')

    returnOfQuery = ''

    try:
        # Condicionais de validação das query strings
        # Definição de variaveis querys que serão executadas com base nas buscas
        if breedId is not None:
            returnOfQuery = queryImgById(breedId)
        elif hashat is not None:
            returnOfQuery = queryImgByHat(hashat)
        elif hassunglass is not None:
            returnOfQuery = queryImgBySunglass(hassunglass)
        else:
            return jsonify({'Mensagem': 'Efetue uma busca por imagem'})

        # Verifica se o valor foi encontrado no banco
        if len(returnOfQuery) == 0:
            timeToFirstValidation = time.clock() - initialTime
            sendLogToES(message="Imagem não encontrada no banco de dados", severity="Debug",
                        latency=timeToFirstValidation, category="execucao", route="/v1/cats/searchimgs")
            return jsonify({'Mensagem': 'Imagem não encontrada no banco de dados.'})
        else:
            # Salva os valores recuperados pela query // Loop para varrer todos os valores
            result = []
            for img in returnOfQuery:
                result.append(dict(img))

            # Ponto de calculo de tempo
            totalTime = time.clock() - initialTime

            # Registro de Log
            sendLogToES(message="Procura por imagem de gato realizada", severity="Info", latency=totalTime,
                        category="execucao", route="/v1/cats/searchimgs")

            return jsonify(result)

    # Tratamento de exception
    except Exception:
        errorTime = time.clock() - initialTime
        sendLogToES(message="Não foi possivel efetuar a busca por imagens", severity="Error", latency=errorTime,
                    category="execucao", route="/v1/cats/searchimgs")
        return jsonify({'Mensagem': 'Erro ao efetuar busca de imagem'})


# Função para uso do Health Check - PLUS ao Projeto
def checkDB():
    # Iniciar contador de tempo de execução da função
    initialTime = time.clock()
    try:
        # Query aleatoria apenas para validar o banco
        customQuery("SELECT 1")

        # Ponto de calculo de tempo
        executionTime = time.clock() - initialTime

        # Registro de Log
        sendLogToES(message="Health check com o Banco de dados", severity="Info", latency=executionTime,
                    category="healthcheck", route="background")

        return 'OK'

    # Tratamento de exception
    except:
        # Ponto de calculo de tempo
        errorTime = time.clock() - initialTime

        # Registro de Log
        sendLogToES(message="Erro ao efetuar health check com o banco de dados", severity="Error",
                    latency=errorTime, category="healthcheck", route="background")
        return 'Down'


# Função para uso do Health Check - PLUS ao Projeto
def checkAPI(route):
    try:
        # Consulta URL // Retorno da consulta
        status = requests.get(route)
        if status.ok:
            return "OK"
        else:
            return "Down"
    except:
        return "Parametro invalido"


# Rota de Health Check - PLUS ao projeto
@app.route('/v1/cats/healthcheck', methods=['GET'])
def healthcheck():
    # Iniciar contador de tempo de execução da função
    initialTime = time.clock()

    # Ponto de calculo de tempo
    executionTime = time.clock() - initialTime

    # Registro de Log
    sendLogToES(message="Health check realizado", severity="Debug", latency=executionTime, category="healthcheck",
                route="/v1/cats/healthcheck")

    # Consultas Health Check
    return jsonify({
        'Banco de Dados': checkDB(),
        'Rota Breeds': checkAPI('http://localhost:5000/v1/cats/breeds/all'),
        'Rota Breeds Info': checkAPI('http://localhost:5000/v1/cats/breeds/info'),
        'Rota Temperaments': checkAPI('http://localhost:5000/v1/cats/temperaments'),
        'Rota Origins': checkAPI('http://localhost:5000/v1/cats/origins'),
        'Rota Imgs': checkAPI('http://localhost:5000/v1/cats/searchimgs'),
        'CPU%': psutil.cpu_percent(),
        'Memory': psutil.virtual_memory()
    })


# Execução do programa, definição de Porta e IP. Necessário 0.0.0.0 pois o Flask adota o loopback como padrão.
if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
