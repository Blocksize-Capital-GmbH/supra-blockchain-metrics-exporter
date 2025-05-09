from exporter.clients.log_reader import (
    read_last_n_lines,
    extract_validator_block_height,
    compute_keyword_abundance,
)

# Adjust path to your log file
log_path = "/Users/abhinavtaneja/Downloads/supra-local.log"  # or wherever it's mounted

log_data = read_last_n_lines(log_path)

height = extract_validator_block_height(log_data)
abundance = compute_keyword_abundance(log_data, "Block", "abcd1234")

print(f"Block height: {height}")
print(f"Block abundance with pubkey: {abundance}")
