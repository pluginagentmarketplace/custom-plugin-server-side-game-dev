#!/usr/bin/env python3
"""Secure token generation for game authentication."""
import hashlib
import hmac
import secrets
import time
import base64
import json

SECRET_KEY = secrets.token_bytes(32)

def generate_session_token(player_id: str) -> str:
    """Generate a secure session token."""
    payload = {
        "player_id": player_id,
        "created_at": int(time.time()),
        "nonce": secrets.token_hex(16)
    }
    payload_bytes = json.dumps(payload).encode()
    signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(payload_bytes + signature).decode()
    return token

def verify_token(token: str) -> dict:
    """Verify and decode a session token."""
    try:
        decoded = base64.urlsafe_b64decode(token)
        payload_bytes = decoded[:-32]
        signature = decoded[-32:]
        expected_sig = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).digest()
        if hmac.compare_digest(signature, expected_sig):
            return json.loads(payload_bytes)
        return None
    except Exception:
        return None

def generate_match_key(match_id: str) -> str:
    """Generate encryption key for match data."""
    return hashlib.sha256(f"{match_id}:{SECRET_KEY.hex()}".encode()).hexdigest()

if __name__ == "__main__":
    token = generate_session_token("player_123")
    print(f"Token: {token[:50]}...")
    verified = verify_token(token)
    print(f"Verified: {verified}")
