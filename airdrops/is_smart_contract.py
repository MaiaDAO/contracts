import json
from web3 import Web3
from collections import defaultdict

def is_smart_contract_address(address, web3_provider):
    code = web3_provider.eth.get_code(Web3.to_checksum_address(address))
    return code != b''

def add_smart_contract_field(input_file, output_file, provider_url):
    # Connect to the blockchain provider
    web3 = Web3(Web3.HTTPProvider(provider_url))

    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Check each address and add the isSmartContract field
    for address, details in data.items():
        if is_smart_contract_address(address, web3):
            details['isSmartContract'] = True

    # Write the updated data to the output file
    with open(output_file, 'w') as out_file:
        json.dump(data, out_file, indent=4)

    print(f'Updated JSON saved to {output_file}')

# Usage example
input_file = 'airdrop.json'
output_file = 'airdrop.json'
provider_url = 'https://metis-pokt.nodies.app'

add_smart_contract_field(input_file, output_file, provider_url)
