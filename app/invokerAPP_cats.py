import requests
import time
from db import recordCatsInfo, recordImgInfo, countImg, countCatById, countImgURL
from log import sendLogToES

# Aguardar inicialização
time.sleep(120)
sendLogToES(message="Inicializacao do Invoker", severity="Debug", latency=0, category="background", route="background")

# URLS para consulta de dados
url = "https://api.thecatapi.com/v1/breeds"
urlImg = "https://api.thecatapi.com/v1/images/search"
HEADERS = {'x-api-key': 'eaa958a0-20a1-4dc4-80aa-8148be50e555'}

# Consultar raças
def getImgUrlFromBreedId(breedId):
    query = "?breed_ids="
    concatQuery = urlImg+query+breedId
    reqImg = requests.get(concatQuery, headers=HEADERS)
    convertReqImg = reqImg.json()

    for x in convertReqImg:
        return x['url']

# Consultar imagens com chapeu
def getImgUrlWithHats():
    queryHat = "?category_ids=1"
    concatQueryHat = urlImg + queryHat
    reqImgHat = requests.get(concatQueryHat, headers=HEADERS)
    convertReqImgHat = reqImgHat.json()

    for y in convertReqImgHat:
        return y['url']

# Consultar imagens com oculos escuros
def getImgUrlWithSunglass():
    querySunglass = "?category_ids=4"
    concatQuerySunglass = urlImg + querySunglass
    reqImgSunglass = requests.get(concatQuerySunglass, headers=HEADERS)
    convertReqImgSunglass = reqImgSunglass.json()

    for z in convertReqImgSunglass:
        return z['url']

# Processar informacoes dos gatos e salvar no banco de dados
def parseCatInfos():
    req = requests.get(url, headers=HEADERS)
    convertReq = req.json()

    # Filtrar informações solicitadas
    for getInfos in convertReq:
        commitCatToDB = (
             getInfos['id'],
             getInfos['name'],
             getInfos['origin'],
             getInfos['temperament'],
             getInfos['description']
        )
        breedId = getInfos['id']

        # Verifica se o gato já existe na base
        catExist = countCatById(breedId)
        if catExist == 1:
            print("Gato {0} já existe na base de dados.".format(breedId))
        else:
            recordCatsInfo(commitCatToDB)

        # Conta quantas imagens este gato já possui
        countImgsCats = countImg(breedId, 'false', 'false')

        # Se ele não possuir 3 imagens, salvar as imagens
        if countImgsCats == 3:
            print("Ja existem 3 imagens para esta raça")
        else:
            while countImgsCats < 3:
                returnOfBreedImg = getImgUrlFromBreedId(breedId)

                # imgExist = queryImgURL(returnOfBreedImg)
                # if imgExist == 1:
                #     print("Imagem já existente")
                # else:
                commitImgToDB = (
                    breedId,
                    returnOfBreedImg,
                    "false",
                    "false"
                )
                recordImgInfo(commitImgToDB)
                countImgsCats = countImg(breedId, 'false', 'false')

# Processar imagens com chapeus e salvar no banco de dados
def parseImgWithHats():
    countImgsWithHats = countImg('', 'true', 'false')

    # Conta a quantidade de imagens e verifica se ja existem 3 imagens com chapeus
    if countImgsWithHats == 3:
        print("Já existem 3 imagens com chapeu")
    else:
        while countImgsWithHats < 3:
            returnOfHatsImg = getImgUrlWithHats()
            commitImgHatToDB = (
                "",
                returnOfHatsImg,
                "true",
                "false"
            )
            recordImgInfo(commitImgHatToDB)
            countImgsWithHats = countImg('', 'true', 'false')

# Processar imagens com oculos escuros e salvar no banco de dados
def parseImgWithSunglass():
    countImgsSunGlass = countImg('', 'false', 'true')

    # Verifica se ja existem 3 imagens no banco de dados e salva
    if countImgsSunGlass == 3:
        print("Já existem 3 imagens com oculos")
    else:
        while countImgsSunGlass < 3:
            returnOfHatsImg = getImgUrlWithSunglass()
            commitImgSunglassToDB = (
                "",
                returnOfHatsImg,
                "false",
                "true"
            )
            recordImgInfo(commitImgSunglassToDB)
            countImgsSunGlass = countImg('', 'false', 'true')

# Iniciar o invoker para processamento
parseCatInfos()
parseImgWithHats()
parseImgWithSunglass()