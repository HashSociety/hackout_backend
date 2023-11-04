# HeadTogether

Our project, HeadTogether is a travel companion app tailored for travelers. With our app, users can input their personal information and specify their travel intentions, whether it's exploring a new destination, sharing a cab ride, or enjoying a movie with someone. With HeadTogether, you can create and join exclusive "rooms" for specific purposes within a a specified radius, making your immediate location your password. Upon submission, our app will generate a virtual "room" based on these details, allowing users to define the room's size and set the range for visibility to others. This unique room concept is then made accessible to fellow app users within the specified range. They can explore these rooms, join discussions, and collaborate on travel plans, fostering connections and making solo adventures more engaging and social.  It's all about local synergy, where your neighbors, fellow commuters, or enthusiasts in your area can easily connect, share rides, play sports, or embark on shared activities, all by being in the right place at the right time. Whether you're seeking companionship, ride-sharing, or cultural exploration, our travel app has you covered. 

## Getting Started

Before running the application, you need to install the required dependencies. You can do this using `pip`.

```bash
pip install fastapi[all] aiomysql pyrebase4
```

## Running the Application

You can run the FastAPI application using the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

This command starts the application on `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs` or `http://localhost:8000/redoc`.

## Endpoints

### Authentication

#### Signup (POST `/signup`)

- Creates a new user account.
- Requires providing an email and password.
- Inserts user information into the MySQL database.

#### Login (POST `/login`)

- Authenticates a user and returns an access token.
- Requires providing a valid email and password.

#### Get User Info (GET `/get_user_info`)

- Retrieves user information based on the provided access token.
- Requires a valid access token obtained during login.

### Rooms

#### Create Room (POST `/create_room`)

- Creates a new room.
- Requires providing room details like `OwnerName`, `RoomPurpose`, `Latitude`, `Longitude`, and `DistanceAllowed`.
- The user who creates the room is automatically added as an admin of the room.

#### Get Room (GET `/get_room/{room_id}`)

- Retrieves room details based on the provided room ID.
- Requires a valid room ID.
- Accessible to authenticated users.

#### Search Nearby Rooms (GET `/search_nearby_rooms`)

- Searches for nearby rooms based on user's latitude and longitude.
- Requires providing the user's location (`user_latitude` and `user_longitude`).
- Returns a list of nearby rooms.

#### Join Room (POST `/join_room/{room_id}`)

- Allows a user to join an existing room.
- Requires providing a valid room ID.
- The user is added as a participant in the room.

## Database Configuration

The application uses MySQL for user and room data storage. Make sure to configure the MySQL database connection parameters in the `create_connection_pool` function.

## Firebase Configuration

Firebase is used for user authentication. You need to provide your Firebase configuration in the `config` dictionary. Update the `config` dictionary with your Firebase project credentials.

```python
config = {
    "apiKey": "your_api_key",
    "authDomain": "your_auth_domain",
    "projectId": "your_project_id",
    "storageBucket": "your_storage_bucket",
    "messagingSenderId": "your_messaging_sender_id",
    "appId": "your_app_id",
    "measurementId": "your_measurement_id",
    "databaseURL": "your_database_url"
}
```

## Dependencies

- FastAPI: A modern, fast web framework for building APIs with Python.
- pyrebase: A Python wrapper for the Firebase API.
- aiomysql: An asynchronous MySQL client for Python.

## Notes

- This is a sample application and should be customized and secured for production use.
- Error handling and validation have not been thoroughly implemented in this example and should be enhanced for production use.

Enjoy exploring and extending this FastAPI application for your specific needs!
```

You can copy and paste this Markdown content into your README.md file.