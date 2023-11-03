# hackout_backend

install dependencies:
pip install fastapi[all] sqlalchemy databases[mysql]

To run server:
uvicorn main:app --reload <ip_address> --port <port_number>

eg: uvicorn main:app --reload 0.0.0.0 --port 8000
