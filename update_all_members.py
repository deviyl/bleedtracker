import json
import os

def load_members():
    members_json = os.getenv("MEMBERS_API")
    if not members_json:
        raise ValueError("MEMBERS_API secret not found.")
    return json.loads(members_json)

if __name__ == "__main__":
    members = load_members()
    print("Loaded members:", list(members.keys()))
