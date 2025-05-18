import requests, csv  # Importing required modules for API requests and CSV writing

# Setting my kiln API key for authentication 🔑
api_key = "kiln_Ocn7..."  # Replace with your actual API key

# API headers for authentication
headers = { "Authorization": f"Bearer {api_key}" }

# 🔗 Non-Kiln validator wallet address (used to query their validators)
non_kiln_url = "https://api.testnet.kiln.fi/v1/eth/stakes?wallets=0x195104dD1d3648141f42B85Fa4Fef6F9879825aa"

# 🔗 Kiln-managed validators query using scope=kiln
kiln_url = "https://api.testnet.kiln.fi/v1/eth/stakes?scope=kiln"

# Helper function to validate if all reward fields are non-zero
def has_valid_rewards(v):
    return all([
        v.get("gross_apy") not in (None, 0),
        float(v.get("consensus_rewards", 0)) != 0,
        float(v.get("execution_rewards", 0)) != 0,
        float(v.get("rewards", 0)) != 0
    ])

# Generic function to fetch and optionally filter validators from any Kiln API endpoint
def fetch_validators(url, source, limit=None, strict_rewards=False):
    resp = requests.get(url, headers=headers).json().get("data", [])
    filtered = [
        {
            "source": source,
            "validator_address": v["validator_address"],
            "gross_apy": v["gross_apy"],
            "consensus_rewards": v.get("consensus_rewards", "0"),
            "execution_rewards": v.get("execution_rewards", "0"),
            "rewards": v.get("rewards", "0")
        }
        for v in resp
        if v.get("gross_apy") not in (None, 0)
        and (not strict_rewards or has_valid_rewards(v))
    ]
    return filtered[:limit] if limit else filtered

# Get up to 50 non-Kiln validators with all non-zero rewards
non_kiln = fetch_validators(non_kiln_url, "Non-Kiln", limit=50, strict_rewards=True)

# Get all Kiln validators with non-zero gross APY
kiln = fetch_validators(kiln_url, "Kiln")

# 🖨️ Print how many valid validators were found
print(f" Non-Kiln (filtered): {len(non_kiln)}")
print(f" Kiln (filtered): {len(kiln)}")

# 💾 Export the data into a CSV file
with open("validator_comparison.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "source", "validator_address", "gross_apy",
        "consensus_rewards", "execution_rewards", "rewards"
    ])
    writer.writeheader()
    writer.writerows(kiln + non_kiln)

print("\n Comparison file saved: 'validator_comparison.csv'")

"""
Summary of What This Script Does:

1. Connects to the Kiln API using your API key.
2. Pulls validator data for:
   - Kiln-managed validators using `scope=kiln`
   - Non-Kiln validators from a known wallet address
3. Filters results to only include validators with valid gross_apy.
4. For Non-Kiln validators, it further checks all reward fields are non-zero.
5. Limits the non-Kiln validator list to 50 entries as per assignment.
6. Combines both sets of data (Kiln + Non-Kiln).
7. Saves the result into a CSV file called 'validator_comparison.csv' 
   with columns like Source, Validator Address, APY, and rewards.

Useful for: Comparing APY performance between Kiln and non-Kiln validators on Holesky.
"""
