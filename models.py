from pydantic import BaseModel

class SignupRequest(BaseModel):
    email: str
    password: str
    name:str
    last_name :str
    gender : str
    age : str

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RoomCreate(BaseModel):
    OwnerName: str
    RoomPurpose: str
    Latitude: float
    Longitude: float
    DistanceAllowed: float
    
class RoomResponseModel(BaseModel):
    RoomID: str
    UserID: int
    OwnerName: str
    RoomPurpose: str
    Latitude: float
    Longitude: float
    DistanceAllowed: float