from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

from exporter.config import config
from exporter.collectors.rpc_collector import RpcCollector
from exporter.collectors.validator_collector import ValidatorCollector
from exporter.collectors.common_collector import CommonCollector

registry = CollectorRegistry()

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(generate_latest(registry))
        else:
            self.send_response(404)
            self.end_headers()

def start_http_server_with_collectors(port):
    if config.role == "rpc":
        registry.register(RpcCollector())
    elif config.role == "validator":
        registry.register(ValidatorCollector())
    elif config.role == "both":
        registry.register(CommonCollector())       # Register first!
        registry.register(RpcCollector())
        registry.register(ValidatorCollector())

    start_http_server(port, registry=registry)
    print(f"Starting Prometheus exporter on port {port}...")

    import time
    while True:
        time.sleep(60)
