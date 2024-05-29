from pydantic import BaseModel

class UserRequest(BaseModel):
    email : str
    username : str
    password : str

class UserResponse(BaseModel):
    email : str
    username : str
    # password : str

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None