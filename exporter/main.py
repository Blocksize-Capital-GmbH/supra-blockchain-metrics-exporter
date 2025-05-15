from exporter.config import config
from exporter.server import start_http_server_with_collectors

# This will call the collectors internally
start_http_server_with_collectors(config.port)
