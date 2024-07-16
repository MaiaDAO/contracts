import json
from collections import defaultdict

def merge_json_files(staking_1_file, staking_2_file, lp_1_file, lp_2_file, output_file):
    merged_data = defaultdict(lambda: {
        "bHermes": 0,
        "staking 1 balance": 0,
        "staking 2 balance": 0,
        "LP 1 value": 0,
        "LP 2 value": 0,
        "usdc-usdt 1 balance": 0,
        "metis-usdc 1 balance": 0,
        "usdc-usdt 2 balance": 0,
        "metis-usdc 2 balance": 0,
        "mim-usdc 2 balance": 0
    })

    def update_merged_data(file, balance_key):
        with open(file, 'r') as f:
            data = json.load(f)
            for entry in data:
                address = entry["address"]
                merged_data[address]["bHermes"] += entry.get("bHermes", 0)
                if "balance" in entry:
                    merged_data[address][balance_key] = entry.get("balance", 0)
                if "value" in entry:
                    merged_data[address][balance_key] = entry.get("value", 0)
                if "usdc-usdt" in entry:
                    merged_data[address]["usdc-usdt 1 balance" if "LP 1" in balance_key else "usdc-usdt 2 balance"] = entry.get("usdc-usdt", 0)
                if "metis-usdc" in entry:
                    merged_data[address]["metis-usdc 1 balance" if "LP 1" in balance_key else "metis-usdc 2 balance"] = entry.get("metis-usdc", 0)
                if "mim-usdc" in entry:
                    merged_data[address]["mim-usdc 2 balance"] = entry.get("mim-usdc", 0)

    update_merged_data(staking_1_file, "staking 1 balance")
    update_merged_data(staking_2_file, "staking 2 balance")
    update_merged_data(lp_1_file, "LP 1 value")
    update_merged_data(lp_2_file, "LP 2 value")

    # Remove fields with zero values from each entry, except for the bHermes field
    cleaned_data = {}
    for address, details in merged_data.items():
        cleaned_data[address] = {k: v for k, v in details.items() if v != 0 or k == "bHermes"}


    # Sort cleaned data by bHermes in descending order
    sorted_data = dict(sorted(cleaned_data.items(), key=lambda item: item[1]["bHermes"], reverse=True))

    with open(output_file, 'w') as out_file:
        json.dump(sorted_data, out_file, indent=4)

    print(f'Merged and sorted JSON saved to {output_file}')


staking_1_file = 'stakers1.json'
staking_2_file = 'staking2.json'
lp_1_file = 'lp1.json'
lp_2_file = 'lp2.json'
output_file = 'airdrop.json'

merge_json_files(staking_1_file, staking_2_file, lp_1_file, lp_2_file, output_file)
