from pydantic import BaseModel


class LoginResponse(BaseModel):
    def __init__(self, token):
        self.token = token
    token: str
