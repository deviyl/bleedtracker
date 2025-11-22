import json
import os
import urllib.request

def load_members():
    members_json = os.getenv("MEMBERS_API")
    if not members_json:
        raise ValueError("MEMBERS_API secret not found.")
    return json.loads(members_json)

def fetch_attacks(api_key):
    url = f"https://api.torn.com/v2/user/self/attacks?selections=attacks&key={api_key}"
    req = urllib.request.Request(url, headers={"User-Agent": "BleedTracker/1.0"})
    with urllib.request.urlopen(req) as response:
        data = json.load(response)
    return data.get("attacks", [])

if __name__ == "__main__":
    members = load_members()

    # Ensure the attacks folder exists
    os.makedirs("attacks", exist_ok=True)

    for name, api_key in members.items():
        print(f"Fetching attacks for {name}...")
        attacks = fetch_attacks(api_key)
        filename = f"attacks/{name}_attacks.json"
        with open(filename, "w") as f:
            json.dump(attacks, f, indent=2)
        print(f"Saved {len(attacks)} attacks to {filename}")
