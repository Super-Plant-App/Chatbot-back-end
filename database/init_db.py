from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
import urllib.parse as parser
import os

dotenv.load_dotenv()

def init_mongo() -> MongoClient | None:
    username = os.getenv('MONGO_CONNECTION_USER')
    password = os.getenv('MONGO_CONNECTION_PASS')
    host = os.getenv('MONGO_CONNECTION_HOST')

    username = parser.quote_plus(username)
    password = parser.quote_plus(password)
    host = parser.quote_plus(host)

    client = MongoClient('mongodb+srv://%s:%s@%s' % (username, password, host))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        return client
    except Exception as e:
        print(e)