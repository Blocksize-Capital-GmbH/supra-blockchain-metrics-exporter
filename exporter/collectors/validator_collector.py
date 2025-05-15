from prometheus_client.core import GaugeMetricFamily
from exporter.utils.public_rpc import get_public_block_height
from exporter.clients.log_reader import (
    read_last_n_lines,
    parse_block_height,
    calculate_keyword_abundance,
)
from exporter.config import config
from exporter.utils.public_block_state import public_block_height

class ValidatorCollector:
    def collect(self):
        try:
            log_data = read_last_n_lines(config.validator_log_path)

            validator_height = parse_block_height(log_data)
            block_abundance = calculate_keyword_abundance(log_data, "Block", config.network_pubkey)
            view_abundance = calculate_keyword_abundance(log_data, "View", config.network_pubkey)

            yield GaugeMetricFamily(
                "supra_validator_block_height",
                "Block height parsed from validator logs",
                value=validator_height or 0,
            )
            yield GaugeMetricFamily(
                "supra_block_relative_abundance",
                "Proportion of 'Block' log lines with validator pubkey",
                value=block_abundance or 0,
            )
            yield GaugeMetricFamily(
                "supra_view_relative_abundance",
                "Proportion of 'View' log lines with validator pubkey",
                value=view_abundance or 0,
            )

            public_height = get_public_block_height()
            healthy = (
                1.0 if validator_height and public_height and abs(validator_height - public_height) <= 10 else 0.0
            )
            yield GaugeMetricFamily(
                "supra_validator_health",
                "1 if validator height is within 10 blocks of public RPC height",
                value=healthy,
            )

        except Exception as e:
            print(f"[ERROR] Validator collector failed: {e}")
