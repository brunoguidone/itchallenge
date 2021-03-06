# Intro

This project has two applications, one of them (invokerAPP_cats) is responsible of fetching data from theCatsApi and store some fields in database. The other one (api) is an API that query this new database to retrieve Cats filtered information.

## itachall - API - v1

## Setup

### Local

>Note: This lab has used Windows10 and Docker for PC for Linux Containers platforms

- Environment preparation:

     - Putting Docker on Linux Containers Mode: Right click on Docker's icon near to clock, "Switch to Linux Containers" 
     
------

## Docker

- Running containers with applications:

```
     cmd> cd ProjectsRootFolder
     cmd> docker-compose -f docker_compose.yaml up -d
```

- To End and Remove Containers
```
     cmd> docker-compose -f docker_compose.yaml down
```

>Note: some resources has a sleep time of 120 seconds to wait until all pre-requirements get ready in sequence.

## Accessing resources (If needed)

- Application API: http://localhost:5000/v1/cats  (Query parameter's on next topic)
- Kibana: http://localhost:5601/
- Elastic Search: http://localhost:9200

------
## Postman Collection

To help the evaluation all requests involving the rules scenarios are inside the [Postman collection file.](https://github.com/brunoguidone/itchallenge/blob/master/postman/get-CatApi.postman_collection.json)

------

## Applications

| Application Name  |  Description  |
| ------------ | -------- |
|  api.py |  Python Rest API used to query data from Cats DB |
| invokerAPP_cats.py |   Fetch data from TheCatsApi and insert in a database |

------

## Technology's and Versions

>Note: Docker compose may use latest version of some images. These were used during this test:

- Python v.3.6.6 (modules installed: requests, psycopg2, flask, elasticsearch, psutil)
- PostgreSQL v12.3
- Kibana v5.5.2 - For log monitoring and Dashboards
- Elastic Search v5.5.2 - For saving logs
- Docker for PC (Linux mode) v2.3
- Postman v7.25.2

------

## Topology

![Topology](https://raw.githubusercontent.com/brunoguidone/itchallenge/master/screenshots/ProjectDraw.png)


------

## Application Flow

![AppFlow](https://github.com/brunoguidone/itchallenge/blob/master/screenshots/ApplicationFlow.png?raw=true)


------


## Endpoints/Routes
| HTTP Method  |  URI  |  Example of Parameter |  Action  |
| ------------ | ----- | -------- | -------- |
|  GET |  /v1/cats/ | N/A |   Welcome |
|  GET |  /v1/cats/breeds/all | N/A |   Listing all breeds |
|  GET |  /v1/cats/breeds/info?breedId= | ?breedId=SomeID |   Listing informations about a breed by passing his ID |
|  GET |  /v1/cats/temperaments?temperament= | ?temperament=SomeTemperament |   Listing breeds with the temperament informed |
|  GET |  /v1/cats/origins?origin= | ?origin=SomeOrigin |   Listing breeds with the origin informed |
|  GET |  /v1/cats/searchimgs? | ?hashat=true or ?hassunglass=true or breedId=SomeID |   Search for images with informed filter |
|  GET |  /v1/cats/healthcheck | N/A |  Provides de health check information of API |

------
### Examples of use:

> Request for all breeds: http://localhost:5000/v1/cats/breeds/all

- Response example:
```
[
  {
    "id": "abob",
    "name": "American Bobtail"
  },
  {
    "id": "abys",
    "name": "Abyssinian"
  }, (.......)
```

> Request for some breed info: http://localhost:5000/v1/cats/breeds/info?breedId=abys

- Response example:
```
[
  {
    "description": "The Abyssinian is easy to care for, and a joy to have in your home. They\u2019re affectionate cats and love both people and other animals.", 
    "id": "abys", 
    "name": "Abyssinian", 
    "origin": "Egypt", 
    "temperament": "Active, Energetic, Independent, Intelligent, Gentle"
  }
]
```

> Request for breeds with this temperament: http://localhost:5000/v1/cats/temperaments?temperament=Intelligent

- Response example:
```
[
  {
    "id": "abob", 
    "name": "American Bobtail"
  }, 
  {
    "id": "abys", 
    "name": "Abyssinian"
  }, 
  {
    "id": "acur", 
    "name": "American Curl"
  }, (.......)
```

> Request for breeds with this origin: http://localhost:5000/v1/cats/origins?origin=Egypt

- Response example:
```
[
  {
    "id": "abys", 
    "name": "Abyssinian"
  }, 
  {
    "id": "chau", 
    "name": "Chausie"
  }, 
  {
    "id": "emau", 
    "name": "Egyptian Mau"
  }
]
```

> Request for images of this breed: http://localhost:5000/v1/cats/searchimgs?breedId=abys \
> Request for images with hats: http://localhost:5000/v1/cats/searchimgs?hashat=true \
> Request for images with sunglass: http://localhost:5000/v1/cats/searchimgs?hassunglass=true \
 
- Response example:
```
[
  {
    "breed_id": "abys", 
    "hashat": false, 
    "hassunglass": false, 
    "imgurl": "https://cdn2.thecatapi.com/images/TGuAku7fM.jpg"
  }, 
  {
    "breed_id": "abys", 
    "hashat": false, 
    "hassunglass": false, 
    "imgurl": "https://cdn2.thecatapi.com/images/p6x60nX6U.jpg"
  }, 
  {
    "breed_id": "abys", 
    "hashat": false, 
    "hassunglass": false, 
    "imgurl": "https://cdn2.thecatapi.com/images/itfFA4NWS.jpg"
  }
]
```

> Request for healthcheck: http://localhost:5000/v1/cats/healthcheck
 
- Response example:
```
{
  "Banco de Dados": "OK", 
  "CPU%": 2.9, 
  "Memory": [
    2088132608, 
    158515200, 
    92.4, 
    1759186944, 
    87547904, 
    323452928, 
    219066368, 
    39956480, 
    201441280, 
    5328896, 
    64696320
  ], 
  "Rota Breeds": "OK", 
  "Rota Breeds Info": "OK", 
  "Rota Imgs": "OK", 
  "Rota Origins": "OK", 
  "Rota Temperaments": "OK"
}
```

------ 
## How to access Log and Dashboards (Step-by-Step)

1- Log into Kibana's page, at [http://localhost:5601](http://localhost:5601).

2- Choose the index that was already created.

![Step1](https://github.com/brunoguidone/itchallenge/blob/master/screenshots/Kibana%20-%20Pass1.png?raw=true)

3- Click on Saved Objects tab and then click on Import Button.

![Step2](https://github.com/brunoguidone/itchallenge/blob/master/screenshots/Kibana%20-%20Pass2.png?raw=true)

4- Choose the document called [All-Dashboards.json](https://github.com/brunoguidone/itchallenge/blob/master/All-Dashboards.json)

------ 

## Navigating through the menu

- Dashboard - Dashboards page to list all the dashboards that was created
- Discover - Saved Search to query logs in real time
- Visualize - Individual graphics used on dashboards

------ 

## Logs

Logs can be watched in real time on the following Kibana query link:

http://localhost:5601/app/kibana#/discover?_g=()&_a=(columns:!(_source),index:catsapi,interval:auto,query:(match_all:()),sort:!(date,desc))

> Dashboard - Query - Log Search - Real Time
![LogSearch](https://github.com/brunoguidone/itchallenge/blob/master/screenshots/Kibana%20-%20Log%20Search.png?raw=true)

------ 
## Dashboards

Dashboards can be accessed by the following link:

http://localhost:5601/app/kibana#/dashboards?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:now-12h,mode:quick,to:now))


> Dashboard - Counting API Execution
![Dash1- Counting API Executions](https://github.com/brunoguidone/itchallenge/blob/master/screenshots/Kibana%20-%20DashBoard%20-%20Count%20Execution.png?raw=true)

> Dashboard - Couting API Errors
![Dash2 - Counting Errors](https://github.com/brunoguidone/itchallenge/blob/master/screenshots/Kibana%20-%20DashBoard%20-%20Error%20Count.png?raw=true)

> Dashboard - Counting Latency
![Dash3 - Counting Latency](https://github.com/brunoguidone/itchallenge/blob/master/screenshots/Kibana%20-%20DashBoard%20-%20Latency.png?raw=true)
