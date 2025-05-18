import requests
import csv

# Your Kiln API Key
api_key = "kiln_Ocn7hmm..."

# Add the API key to headers
headers = { "Authorization": f"Bearer {api_key}" }

# URLs to get validator data
non_kiln_url = "https://api.testnet.kiln.fi/v1/eth/stakes?wallets=0x195104dD1d3648141f42B85Fa4Fef6F9879825aa"
kiln_url = "https://api.testnet.kiln.fi/v1/eth/stakes?scope=kiln"
#------------------------------------------------------------------
# Function to get data from Kiln API
def get_validators(url):
    response = requests.get(url, headers=headers)
    data = response.json().get("data", [])
    return [
        {
            "source": "Kiln" if "scope=kiln" in url else "Non-Kiln",
            "validator_address": v["validator_address"],
            "gross_apy": v["gross_apy"],
            "consensus_rewards": v.get("consensus_rewards", 0),
            "execution_rewards": v.get("execution_rewards", 0),
            "rewards": v.get("rewards", 0)
        }
        for v in data
        if v.get("gross_apy") not in (None, 0)
    ]
#---------------------------------------------------------------------
# Get validators from both sources
kiln_validators = get_validators(kiln_url)
non_kiln_validators = get_validators(non_kiln_url)[:50]  # Limit to 50

# Combine both lists
all_validators = kiln_validators + non_kiln_validators

# Save to CSV
with open("validator_comparison2.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["source", "validator_address", "gross_apy", "consensus_rewards", "execution_rewards", "rewards"])
    writer.writeheader()
    writer.writerows(all_validators)

print("CSV saved as 'validator_comparison2.csv'")