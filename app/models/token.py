from dataclasses import dataclass


@dataclass
class Token:
    access_token: str
    expires_in: float
    token_type: str

    @staticmethod
    def from_json(json: dict) -> "Token":
        return Token(
            json["access_token"],
            float(json["expires_in"]),
            json["token_type"],
        )
