# Bood Donation

<p align="center"> 
<a href="http://www.prosangue.sp.gov.br">
<img border="0" alt="Pró-Sangue Foundation" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/blood-logo.png">
</a>
</p>

Project to collect data on the current **Blood Stock Position** of the Pró-Sangue Foundation of the state of São Paulo Brazil.

## Synopsis

The project is a *web scraper* that collects the blood stock position on the Pro-Blood Foundation of São Paulo website. The idea is to have a dataset with the collected data to be used for analysis and warning (threshold). The data is transformed a Json by a Python micro-service. Nifi creates the data pipeline, and sends the information to Elasticsearch, which Kibana can use to create the visualizations and dashboards. 

For this test the environments were dockerized and the web scraper runs on the local machine.
 
### Architecture

This project uses the following technologies:

  * Python
  * Nifi
  * Elasticsearch
  * Kibana

The machine with NiFi and Elasticsearch with Kibana are dockerized.

<p align="center"> 
<img src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/blood-donation-diagram.png">
</p>

### Data Collect

The web scraper monitors the following status on the site:

<p align="center"> 
<img src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/blood-level.png">
</p>

With python micro-service using the BeautifulSoup library and collected this information and transformed into the following Json:

```json
[
    {
        "blood": "O+",
        "status": 2,
        "timestamp": "2019-10-07T17:48:24.899Z",
        "update": "2019-10-07T15:15:00.000Z"
    },
    {
        "blood": "A+",
        "status": 2,
        "timestamp": "2019-10-07T17:48:24.899Z",
        "update": "2019-10-07T15:15:00.000Z"
    },
    {
        "blood": "AB+",
        "status": 2,
        "timestamp": "2019-10-07T17:48:24.899Z",
        "update": "2019-10-07T15:15:00.000Z"
    },
    {
        "blood": "B+",
        "status": 2,
        "timestamp": "2019-10-07T17:48:24.899Z",
        "update": "2019-10-07T15:15:00.000Z"
    },
    {
        "blood": "O-",
        "status": 0,
        "timestamp": "2019-10-07T17:48:24.899Z",
        "update": "2019-10-07T15:15:00.000Z"
    },
    {
        "blood": "A-",
        "status": 2,
        "timestamp": "2019-10-07T17:48:24.899Z",
        "update": "2019-10-07T15:15:00.000Z"
    },
    {
        "blood": "AB-",
        "status": 2,
        "timestamp": "2019-10-07T17:48:24.899Z",
        "update": "2019-10-07T15:15:00.000Z"
    },
    {
        "blood": "B-",
        "status": 0,
        "timestamp": "2019-10-07T17:48:24.899Z",
        "update": "2019-10-07T15:15:00.000Z"
    }
]
```



-------------
curljson -XGET http://localhost:5000/blood-current-position

docker pull nshou/elasticsearch-kibana
docker run -d -p 9200:9200 -p 5601:5601 nshou/elasticsearch-kibana


