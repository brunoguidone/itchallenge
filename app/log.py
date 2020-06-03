from elasticsearch import Elasticsearch
import datetime

# Connection String do ElasticSearch
es = Elasticsearch([{'host': 'es', 'port': 9200}])


# def sendLogToES():
def sendLogToES(message, severity, latency, category, route):
    # Verifica a conexão com o servidor ES
    if es.ping():
        # Tentativa de escrita do log
        try:
            # Criar o indice caso não exista. Caso exista, ignorar.
            es.indices.create(index='catsapi', ignore=400)

            # Informações de Logs a inserir no Elastic Search
            log = {
                "message": message,
                "severity": severity,
                "latency": latency,
                "category": category,
                "date": datetime.datetime.utcnow(),
                "route": route
            }

            # Inserindo informações
            es.index(index='catsapi', doc_type='log', body=log)
            return ("Registro inserido no ES")

        except(Exception) as error:
            return ("Falha ao inserir o registro no ES", error)
    else:
        return ("Nao foi possível conectar ao ElasticSearch")