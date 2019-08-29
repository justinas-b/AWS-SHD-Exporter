from aws_service_health_exporter import generate_prometheus_metrics_as_text


def lambda_handler(event, context):

    return {
        'statusCode': 200,
        'headers': {
          'Content-Type': 'text/plain; version=0.0.4; charset=utf-8',
        },
        'body': generate_prometheus_metrics_as_text()
    }
