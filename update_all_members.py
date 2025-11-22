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

def generate_unique_key(attack):
    """Generate a unique key for each attack to prevent duplicates."""
    if "attack_id" in attack:
        return attack["attack_id"]
    if "id" in attack:
        return attack["id"]
    if "timestamp" in attack:
        return attack["timestamp"]
    return json.dumps(attack, sort_keys=True)

def load_existing_attacks(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as f:
            return json.load(f)
    return []

if __name__ == "__main__":
    members = load_members()
    os.makedirs("attacks", exist_ok=True)

    for name, api_key in members.items():
        print(f"Fetching attacks for {name}...")
        latest_attacks = fetch_attacks(api_key)
        filename = f"attacks/{name}_attacks.json"

        existing_attacks = load_existing_attacks(filename)

        # Build a set of existing attack keys
        existing_keys = {generate_unique_key(a) for a in existing_attacks}

        # Filter only new attacks
        new_attacks = []
        for atk in latest_attacks:
            key = generate_unique_key(atk)
            if key not in existing_keys:
                new_attacks.append(atk)
                existing_keys.add(key)

        if not new_attacks:
            print(f"[{name}] No new attacks.")
            continue

        # Prepend new attacks to maintain newest-first order
        merged_attacks = new_attacks + existing_attacks

        # Save updated attacks JSON
        with open(filename, "w") as f:
            json.dump(merged_attacks, f, indent=2)

        print(f"[{name}] Added {len(new_attacks)} new attacks. Total now: {len(merged_attacks)}")
