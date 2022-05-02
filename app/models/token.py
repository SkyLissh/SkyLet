from dataclasses import dataclass


@dataclass
class Token:
    access_token: str
    expires_in: float
    token_type: str
