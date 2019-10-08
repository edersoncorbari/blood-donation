# Bood Donation

<p align="center"> 
<a href="http://www.prosangue.sp.gov.br">
<img border="0" alt="Pró-Sangue Foundation" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/blood-logo.png">
</a>
</p>

Project to collect data on the current **Blood Stock Position** of the Pró-Sangue Foundation of the state of São Paulo Brazil.

## Synopsis

The project is a *web scraper* that collects the blood stock position on the **Pró-Sangue** Foundation of São Paulo website. The idea is to have a dataset with the collected data to be used for analysis and warning (threshold). The data is transformed a Json by a Python micro-service. Nifi creates the data pipeline, and sends the information to Elasticsearch, which Kibana can use to create the visualizations and dashboards. 

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

Status is transformed into numbers, and dates are added with timezone, making it easy to create views with Kibana.

| Status | Portuguese | English    |
| ------ | ---------  | ---------- |
| 0      | crítico    | critical   |
| 1      | emergência | emergency  | 
| 2      | estável    | stable     | 

### Quick start

You need to have Python-3 installed on the virtualenv machine and docker. Both dockers must be running with Elasticsearch-Kibana and NiFi for the pipline. 

For the tests just follow the steps described below:

#### 1. Get the code

Now run the commands below to compile the project:

```shell
$ git clone https://github.com/edersoncorbari/blood-donation.git
$ cd blood-donation/web-scraping
```

Enter pipenv at the root of the *web-scraping* folder for the tests:

```shell
$ pipenv shell
$ pipenv install
```

Starting the server:

```shell
$ ./server.py
```

In another terminal either run the command below, or use the URL in the browser:

```shell
$ curljson -XGET http://127.0.0.1:5000/blood-current-position
```

The json output will be like the example above containing the 8 blood types and current level of each.

#### 2. Docking and setting up NiFi 

Download NiFi:

```shell
$ docker pull apache/nifi
```

And then start the docker with the commands:

```shell
$ docker run --name nifi \
  -p 8080:8080 \
  -d \
  apache/nifi:latest
```

Wait about 2 minutes and make sure NiFi has gone up to the address:

[http://localhost:8080/nifi/](http://localhost:8080/nifi/)

You will see the NiFi screen:

<p align="center"> 
<img border="0" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/nifi-start.png">
</p>

>Note: You can use the (*docker ps*) command to see the status.

Now! then right click on (*Upload template*), and select the template that is in the project directory: (*nifi/Blood-Donation-PipeLine-2019-10-07.xml*)

<p align="center"> 
<img border="0" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/nifi-template.png">
</p>

Click (Upload) to upload the template.

Now click on the bar in templates. Simply drag and drop the component into the flow area.

<p align="center"> 
<img border="0" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/nifi-template-icon.png">
</p>

Select template (*Blood-Donation-PipeLine-2019-10-07*) and import. Now you go to a process group:

<p align="center"> 
<img border="0" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/nifi-blood.png">
</p>

Within the process group is the flow. That reads the Python web-scraper and sends it to ElasticSearch.

<p align="center"> 
<img border="0" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/nifi-blood-flow.png">
</p>

Before starting the flow, it is necessary to raise the docker with Elasticsearch.

#### 3. Docking and setting up Elasticsearch with Kibana

Download Elasticsearch and Kibana:

```shell
$ docker pull nshou/elasticsearch-kibana
```

And then start the docker with the commands:

```shell
$ docker run --name elasticsearch-kibana \
  -p 9200:9200 -p 5601:5601 \
  -d \
  nshou/elasticsearch-kibana:latest
```

Wait about 2 minutes and make sure Elasticsearch and Kibana has gone up to the address:

[http://localhost:5601/](http://localhost:5601/)

You will see the Kibana screen:

<p align="center"> 
<img border="0" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/kibana-start.png">
</p>

Click in (*Explore on my own*). Then click management in the left sidebar, and click on Kibana (*Index Pattern*).

<p align="center"> 
<img border="0" src="https://raw.githubusercontent.com/edersoncorbari/blood-donation/master/doc/img/kibana-map-index.png">
</p>

When you start the pipeline, NiFi itself will create the index for Elasticsearch and you can map the index on this screen.

#### 3. Starting full flow

It is important to check your network settings. Check the NiFi IP number, the network 172.xx.x.x/16.

```shell
$ docker exec -it -u0 nifi ip a
```

Do the same thing for the docker with Elasticsearch and Kibana:


```shell
$ docker exec -it -u0 elasticsearch-kibana ip a
```

>Note: Also check your local IP, a visible IP on the network where dockers have access.

Start web scraper on your local machine:

```shell
$ cd web-scraping && pipenv shell
$ ./server
```

