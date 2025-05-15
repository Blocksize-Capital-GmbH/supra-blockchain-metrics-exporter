import requests
from exporter.config import config

def get_block_height():
    try:
        # Ensure correct URL: append '/block' to the base RPC URL
        base_url = config.rpc_url.rstrip("/")
        url = f"{base_url}/block"

        response = requests.get(url, timeout=3)
        response.raise_for_status()

        data = response.json()
        return int(data["height"])
    except Exception as e:
        print(f"[ERROR] Failed to get local RPC block height from {config.rpc_url}: {e}")
        return 0
