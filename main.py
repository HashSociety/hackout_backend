from fastapi import FastAPI, UploadFile, File ,Request, HTTPException, Depends,status
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import pyrebase
from  models import * 
import aiomysql
from aiomysql import Pool
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







async def create_connection_pool():
    pool = await aiomysql.create_pool(
        host='sql.freedb.tech',
        user='freedb_hashsociety',
        password='PjbkVhfvM6U*rcp',
        db='freedb_hashsociety',
        autocommit=True
    )
    return pool

async def get_connection():
    return await app.state.pool.acquire()

async def release_connection(conn):
    await app.state.pool.release(conn)


@app.on_event("startup")
async def startup_event():
    app.state.pool = await create_connection_pool()
    
    
@app.on_event("shutdown")
async def shutdown_event():
    await app.state.pool.close()







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
async def signup(request: SignupRequest):
    try:
        # Create a user with email and password (this part remains the same)
        user = auth.create_user_with_email_and_password(request.email, request.password)
        
        # Insert the user's information into the MySQL table
        async with await get_connection() as conn:
            async with conn.cursor() as cursor:
                # Define the SQL INSERT statement
                sql = "INSERT INTO User (EmailId, Name, LastName, Gender, Age) VALUES (%s, %s, %s, %s, %s)"
                
                # Specify the values to insert (you can adjust this part as needed)
                values = (request.email, request.name, request.last_name, request.gender, request.age)
                
                # Execute the INSERT statement
                await cursor.execute(sql, values)
            
        return {"message": "Signup successful", "user": f"{user['email']}"}
    except Exception as e:
        print(e)
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

@app.get("/get_user_info", tags=['Auth'])
async def get_user_info(token: str = Depends(oauth2_scheme)):
    info = auth.get_account_info(token)
    email = info['users'][0]['email']

    # Use the email to fetch user information from the User table
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            # Define the SQL query to retrieve user information based on the email
            sql = "SELECT * FROM User WHERE EmailId = %s"
            
            # Execute the SQL query with the email as a parameter
            await cursor.execute(sql, (email,))
            
            # Fetch the result
            user_info = await cursor.fetchone()

    # Check if user information was found
    if user_info:
        # Convert the result to a dictionary for response
        user_info_dict = {
            "Userid": user_info[0],
            "EmailId": user_info[1],
            "Name": user_info[2],
            "LastName": user_info[3],
            "Gender": user_info[4],
            "Age": user_info[5]
        }
        return user_info_dict
    else:
        raise HTTPException(status_code=404, detail="User not found")


