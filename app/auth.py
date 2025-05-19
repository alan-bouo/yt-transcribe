# app/auth.py
import json
from datetime import date

TOKENS_FILE = "app/tokens.json"
QUOTA_FILE = "app/quota.json"

def load_tokens():
    with open(TOKENS_FILE) as f:
        return json.load(f)

def load_quota():
    try:
        with open(QUOTA_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_quota(quota):
    with open(QUOTA_FILE, "w") as f:
        json.dump(quota, f)

def is_token_valid(token: str) -> bool:
    tokens = load_tokens()
    return token in tokens

def has_quota(token: str) -> bool:
    quota = load_quota()
    return quota.get(token) != str(date.today())

def update_quota(token: str):
    quota = load_quota()
    quota[token] = str(date.today())
    save_quota(quota)
