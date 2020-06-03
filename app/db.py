import psycopg2
import psycopg2.extras
import os

# Connection String do postgres // recebe variavel de ambiente do docker compose
connectionString = os.environ.get("POSTGRES_HOST")

# Função para gravar os gatos no banco, usado pelo Invoker
def recordCatsInfo(commitCatToDB):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        #Chamar connection string
        connectionDB = psycopg2.connect(connectionString)
        #Instancia do cursor
        cursor = connectionDB.cursor()

        #String da query
        queryInserCat = "INSERT INTO cats (ID, NAME, ORIGIN, TEMPERAMENT, DESCRIPTION) VALUES (%s,%s,%s,%s,%s)"

        #Execucao do cursor chamando a query
        cursor.execute(queryInserCat, commitCatToDB)

        #Salvar dados no banco
        connectionDB.commit()

    #Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return ("Falha ao inserir os registros:", error)
        else:
            return "Sem conexao com o banco"

    #Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Função para gravar imagens no banco usado pelo Invoker
def recordImgInfo(commitImgToDB):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        #Instancia do cursor
        cursor = connectionDB.cursor()

        # String da query
        queryInserImg = "INSERT INTO img (breed_id, imgurl, hashat, hassunglass) VALUES (%s,%s,%s,%s)"

        # Execucao do cursor chamando a query
        cursor.execute(queryInserImg, commitImgToDB)

        # Salvar dados no banco
        connectionDB.commit()

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao inserir imagem:", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Função para contar as imagens usada pelo invoker
def countImg(breedId, hasHat, hasSunGlass):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor()

        # String da query
        cursor.execute("SELECT * FROM img WHERE breed_id = %s and hashat = %s and hassunglass = %s;",
                       [breedId, hasHat, hasSunGlass])

        #Contagem de registros
        rows = cursor.fetchall()
        countRows = len(rows)

        return countRows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta countImg", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Função para contar gatos passando ID, usada no Invoker
def countCatById(breedId):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor()

        # String da query
        cursor.execute("SELECT * FROM cats WHERE id = %s;", [breedId])

        # Contagem de registros
        rows = cursor.fetchall()
        countRows = len(rows)

        return countRows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta countCatById", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Função para consultar imagens, usada na API
def countImgURL(checkURL):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor()

        # String da query
        cursor.execute("SELECT * FROM img WHERE imgurl = %s;", [checkURL])

        #Contagem de registros
        rows = cursor.fetchall()
        countRows = len(rows)

        return countRows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta queryImgURL", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Função para consultar os gatos por ID usada na API
def queryAllBreeds():
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "select id,name from cats"

        # Execução da query
        cursor.execute(query)

        # Recuperar valores
        rows = cursor.fetchall()

        return rows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta queryAllBreeds", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Função para consultar os gatos por ID usada na API
def queryBreedById(breedId):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Execução da query
        cursor.execute("SELECT * FROM cats WHERE id = %s;", [breedId])

        # Recuperar valores
        rows = cursor.fetchall()

        return rows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta queryAllBreeds", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Função para consultar os gatos por ID usada na API
def queryByTemperament(temperament):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Execução da query
        cursor.execute("select id,name from cats where temperament like '%"+temperament+"%'")

        # Recuperar valores
        rows = cursor.fetchall()

        return rows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta queryAllBreeds", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Função para consultar os gatos por ID usada na API
def queryByOrigin(origin):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Execução da query
        cursor.execute("select id,name from cats where origin = %s;", [origin])

        # Recuperar valores
        rows = cursor.fetchall()

        return rows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta queryAllBreeds", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Pesquisa por imagens a partir de um ID de Raça
def queryImgById(breedId):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Execução da query
        cursor.execute("select * from img where breed_id = %s;", [breedId])

        # Recuperar valores
        rows = cursor.fetchall()

        return rows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Pesquisa imagens com chapeus
def queryImgByHat(hashat):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Execução da query
        cursor.execute("select * from img where hashat = %s;", [hashat])

        # Recuperar valores
        rows = cursor.fetchall()

        return rows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Pesquisa imagens com chapeus
def queryImgBySunglass(hassunglass):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Execução da query
        cursor.execute("select * from img where hassunglass = %s;", [hassunglass])

        # Recuperar valores
        rows = cursor.fetchall()

        return rows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()

# Consulta customizada
def customQuery(query):
    # Iniciando variaveis
    connectionDB = ''
    cursor = ''
    try:
        # Chamar connection string
        connectionDB = psycopg2.connect(connectionString)

        # Instancia do cursor
        cursor = connectionDB.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Execução da query
        cursor.execute(query)

        # Recuperar valores
        rows = cursor.fetchall()

        return rows

    # Tratamento de exception
    except (Exception, psycopg2.Error) as error:
        if (connectionDB):
            return("Falha ao executar consulta", error)
        else:
            return "Sem conexao com o banco"

    # Fechamento de Conexao
    finally:
        if (connectionDB):
            cursor.close()
            connectionDB.close()