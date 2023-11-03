from fastapi import FastAPI, UploadFile, File ,Request, HTTPException, Depends,status
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import pyrebase
from  models import * 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index(request: Request):
    
    return {"message": "Hello"}

# const firebaseConfig = {
#   apiKey: "AIzaSyBtQKU950eUqsgAVtQw5aubRKXcmyc5g2E",
#   authDomain: "hashtogether.firebaseapp.com",
#   databaseURL: "https://hashtogether-default-rtdb.firebaseio.com",
#   projectId: "hashtogether",
#   storageBucket: "hashtogether.appspot.com",
#   messagingSenderId: "1079333558091",
#   appId: "1:1079333558091:web:6670b36cb755b756b4bace",
#   measurementId: "G-Z13R905TEE"
# };
config = {
    "apiKey":"AIzaSyBtQKU950eUqsgAVtQw5aubRKXcmyc5g2E",
    "authDomain":"hashtogether.firebaseapp.com",
    "projectId":"hashtogether",
    "storageBucket": "hashtogether.appspot.com",
    "messagingSenderId": "1079333558091",
    "appId": "1:1079333558091:web:6670b36cb755b756b4bace",
    "measurementId": "G-Z13R905TEE",
    "databaseURL": "https://hashtogether-default-rtdb.firebaseio.com"
}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.post("/signup")
def signup(request: SignupRequest):
    try:
        user = auth.create_user_with_email_and_password(request.email, request.password)
        return {"message": "Signup successful", "user": f"{user['email']}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Signup failed")

def authenticate_user(username: str, password: str):
    try:
        response=auth.sign_in_with_email_and_password(username,password)

        access_token = response['idToken']
        
        return {"access_token": access_token, "token_type": "bearer"}
    # except client.exceptions.NotAuthorizedException:
    #     raise Exception("Invalid credentials")
    # except client.exceptions.UserNotFoundException:
    #     raise Exception("User not found")
    except Exception as e:
        raise Exception(str(e))


@app.post("/login", response_model=Token,tags=['Auth'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return authenticate_user(form_data.username, form_data.password)

@app.get("/get_userid",tags=['Auth'])
async def get_userid(token : str= Depends(oauth2_scheme)):
    info=auth.get_account_info(token)
    #print(info['users'][0]['email'])
    email=info['users'][0]['email']
    return {"userid": email} 
