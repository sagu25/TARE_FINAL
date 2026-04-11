"""
BlueVerse Foundry — Agent API Client

Handles OAuth2 token acquisition and agent invocation.
All credentials and agent IDs are loaded from .env

Usage:
    from blueverse_client import BlueverseClient
    client = BlueverseClient()
    response = client.invoke("KORAL", "What telemetry have you observed?")
"""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# ─── Agent ID map (fill values in .env) ───────────────────────────────────────
AGENT_IDS = {
    # Zone 3 — Reef
    "KORAL":    os.getenv("BV_AGENT_KORAL", ""),
    "MAREA":    os.getenv("BV_AGENT_MAREA", ""),
    "TASYA":    os.getenv("BV_AGENT_TASYA", ""),
    "NEREUS":   os.getenv("BV_AGENT_NEREUS", ""),
    # Zone 2 — Shelf
    "ECHO":     os.getenv("BV_AGENT_ECHO", ""),
    "SIMAR":    os.getenv("BV_AGENT_SIMAR", ""),
    "NAVIS":    os.getenv("BV_AGENT_NAVIS", ""),
    "RISKADOR": os.getenv("BV_AGENT_RISKADOR", ""),
    # Zone 1 — Trench
    "TRITON":   os.getenv("BV_AGENT_TRITON", ""),
    "AEGIS":    os.getenv("BV_AGENT_AEGIS", ""),
    "TEMPEST":  os.getenv("BV_AGENT_TEMPEST", ""),
    "LEVIER":   os.getenv("BV_AGENT_LEVIER", ""),
    # Zone 4
    "BARRIER":  os.getenv("BV_AGENT_BARRIER", ""),
}


class BlueverseClient:
    """
    OAuth2 client for BlueVerse Foundry agent API.
    Token is cached and refreshed automatically on expiry.
    """

    def __init__(self):
        self._token_url     = os.getenv("BLUEVERSE_TOKEN_URL", "")
        self._chat_url      = os.getenv("BLUEVERSE_CHAT_URL", "")
        self._client_id     = os.getenv("BLUEVERSE_CLIENT_ID", "")
        self._client_secret = os.getenv("BLUEVERSE_CLIENT_SECRET", "")
        self._verify_ssl    = os.getenv("BLUEVERSE_VERIFY_SSL", "true").lower() == "true"

        self._access_token  = None
        self._token_expiry  = 0

    # ── Token Management ──────────────────────────────────────────────────────

    def _get_token(self) -> str:
        """Return cached token or fetch a new one if expired."""
        if self._access_token and time.time() < self._token_expiry - 30:
            return self._access_token

        resp = requests.post(
            self._token_url,
            data={
                "grant_type":    "client_credentials",
                "client_id":     self._client_id,
                "client_secret": self._client_secret,
            },
            verify=self._verify_ssl,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        self._access_token = data["access_token"]
        self._token_expiry = time.time() + data.get("expires_in", 3600)
        return self._access_token

    # ── Agent Invocation ──────────────────────────────────────────────────────

    def invoke(self, agent_name: str, message: str) -> str:
        """
        Send a message to a BlueVerse agent and return its response.

        agent_name : one of the 13 TARE agent names (e.g. "KORAL", "MAREA")
        message    : the prompt/question to send to the agent
        Returns    : agent response as string
        """
        agent_id = AGENT_IDS.get(agent_name, "")
        if not agent_id:
            raise ValueError(f"No BlueVerse agent ID configured for {agent_name}. "
                             f"Set BV_AGENT_{agent_name} in .env")

        token = self._get_token()

        url = self._chat_url.rstrip("/")
        if "{agent_id}" in url:
            url = url.replace("{agent_id}", agent_id)
        else:
            url = f"{url}/{agent_id}"

        resp = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type":  "application/json",
            },
            json={"message": message},
            verify=self._verify_ssl,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        # Handle common response formats
        return (
            data.get("response")
            or data.get("content")
            or data.get("message")
            or data.get("answer")
            or data.get("output")
            or str(data)
        )

    def invoke_safe(self, agent_name: str, message: str, fallback: str = "") -> str:
        """
        Same as invoke() but returns fallback string on any error.
        Use this in agent classes so a BlueVerse outage doesn't crash TARE.
        """
        try:
            return self.invoke(agent_name, message)
        except Exception as e:
            print(f"[BlueverseClient] {agent_name} invoke failed: {e}")
            return fallback


# ─── Singleton ────────────────────────────────────────────────────────────────
_client = None

def get_client() -> BlueverseClient:
    """Return shared BlueverseClient instance."""
    global _client
    if _client is None:
        _client = BlueverseClient()
    return _client
