from flask import Flask, Response
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST

from exporter.config import Config
from exporter.validator import collect_validator_metrics
from exporter.rpc import collect_rpc_metrics

app = Flask(__name__)
config = Config.from_env()


@app.route("/metrics")
def metrics():
    # Create a new registry each time so metrics are fresh
    registry = CollectorRegistry()

    if config.is_validator:
        collect_validator_metrics(config, registry)

    if config.is_rpc_node:
        collect_rpc_metrics(config, registry)

    # Generate Prometheus-compliant response
    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.exporter_port)
