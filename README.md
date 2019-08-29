# AWS SHD Exporter

## Purpose

This code contains Prometheus Exporter which monitors status of AWS
Services ( [Service Health Dashboard](https://status.aws.amazon.com) )
as AWS does not provide public APIs for this. The only possible solution
is to use Health API/Personal health Dashboard, but for this you [must be
subscribed to AW Business supportplan](https://aws.amazon.com/premiumsupport/technology/personal-health-dashboard/).

This exporter scrapes AWS Status web-page and provides metrics per
continent/region/service.

## Usage

```
usage: aws_service_health_exporter.py [-h] [-p PORT] [-t DELAY]

Prometheus exporter for AWS Service Health Dashboard.

optional arguments:
  -h, --help  show this help message and exit
  -p PORT     address on which to expose metrics (default "8000")
  -t DELAY    refresh rate for metrics in seconds (default "5")

```

## Sample metrics
```
# HELP AWSServiceHealthDashboard1 Metrics for all AWS Services
# TYPE AWSServiceHealthDashboard1 gauge
aws_service_health{continent="EU",region="Frankfurt",service="Amazon API Gateway",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Ireland",service="Amazon API Gateway",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="London",service="Amazon API Gateway",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Paris",service="Amazon API Gateway",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Stockholm",service="Amazon API Gateway",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Frankfurt",service="Amazon AppStream 2.0",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Ireland",service="Amazon AppStream 2.0",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Frankfurt",service="Amazon Athena",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Ireland",service="Amazon Athena",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="London",service="Amazon Athena",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Global",service="Amazon Chime",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Frankfurt",service="Amazon Cloud Directory",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="Ireland",service="Amazon Cloud Directory",status="Service is operating normally"} 4.0
aws_service_health{continent="EU",region="London",service="Amazon Cloud Directory",status="Service is operating normally"} 4.0
```

## Labels

| Label     | Values             | Description |
|-----------|--------------------|-------------|
| continent | EU<br>NA<br>SA<br>AP<br>ME | Continent in which service is operating | 
| region    | [AWS reference](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html) | Region in which service is operating | 
| service   | [AWS reference](https://aws.amazon.com/products/) | AWS service name |
| status    | Service is operating normally<br>Informational message<br>Service degradation<br>Service disruption | Status of AWS service |


## Values

Prometheus metric value for each AWS service can be between between 1 and 4.
Metric values are described below:

| Value | Description                    |
|-------|-------------------------------|
|   4   | Service is operating normally	|
|   3   | Informational message	        |
|   2   | Service degradation	        |
|   1   | Service disruption            |


## Prometheus server configuration

To configure this exporter on Prometheus server, add below job to
`/etc/prometheus/prometheus.yml` file:

```
scrape_configs:
  - job_name: 'aws_service_health_exporter'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:8888']
```

## Docer container

You can then build and run this exporter as Docker image:

```
$ docker build -t my-python-app .
$ docker run -it --rm --name aws_service_health_exporter aws_service_health_exporter
```

## Deploying exporter as AWS Lambda function

You can configure this exporter to run as AWS Lambda function. To run
this module as Lambda, configure `Handler` as `lambda_handler.lambda_handler`
and map this Lambda Function to AWS Application Load Balancer. Then in 
Prometheus configuration change target to AWS Application Load Balancer
DNS name.