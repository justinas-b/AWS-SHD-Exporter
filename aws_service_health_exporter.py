#!/usr/bin/env python

from prometheus_client import start_http_server, generate_latest
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import time
import requests
from lxml import html
import argparse


class AwsShdCollector(object):

    def __init__(self):
        self.continents = ["EU", "NA", "SA", "AP", "ME"]
        self.endpoint = "https://status.aws.amazon.com"

    @staticmethod
    def shd_status_to_int(status):
        status_dict = {
            'Service is operating normally': 4,
            'Informational message': 3,
            'Service degradation': 2,
            'Service disruption': 1
        }
        return status_dict.get(status)

    @staticmethod
    def split_aws_service(name):
        if "(" in name:
            service, region = name.rsplit(sep='(', maxsplit=1)
            service = service[:-1]
            region = region[:-1]
        else:
            service = name
            region = "Global"

        return service, region

    def collect(self):
        g = GaugeMetricFamily(name="aws_service_health",
                              documentation='Metrics for all AWS Services',
                              labels=['continent', 'region', 'service', 'status'])

        raw_page = requests.get(self.endpoint)
        html_page = html.fromstring(raw_page.content)

        for continent in self.continents:
            table = html_page.xpath(f'//div[@id="{continent}_block"]/table/tbody')[1]
            for row in table.xpath('.//tr'):
                td = row.xpath('.//td')
                service, region = self.split_aws_service(td[1].text)
                g.add_metric(labels=[continent, region, service, td[2].text],
                             value=self.shd_status_to_int(td[2].text))
        yield g


def parse_args():
    parser = argparse.ArgumentParser(
        description='Prometheus exporter for AWS Service Health Dashboard.')
    parser.add_argument(
        '-p',
        metavar='PORT',
        default='8000',
        help='address on which to expose metrics (default "8000")')
    parser.add_argument(
        '-t',
        metavar='DELAY',
        default='5',
        help='refresh rate for metrics in seconds (default "5")')

    return parser.parse_args()


def generate_prometheus_metrics_as_text():
    try:
        REGISTRY.register(AwsShdCollector())
    except ValueError:
        pass

    return generate_latest(registry=REGISTRY).decode('utf-8')


if __name__ == "__main__":
    args = parse_args()

    start_http_server(int(args.p))
    REGISTRY.register(AwsShdCollector())

    while True:
        time.sleep(int(args.t))
