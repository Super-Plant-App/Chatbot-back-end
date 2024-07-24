from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
import dotenv

dotenv.load_dotenv()
class AuthModel():
    def __init__(self):
        self.__init_mongo()

    def __init_mongo(self) -> MongoClient | None:
        connection_str = os.getenv('MONGO_CONNECTION_STR')
        self.client = MongoClient(connection_str)
        
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            
            db_name = os.getenv('MONGO_CONNECTION_DB')
            self.db = self.client[db_name]

            # Create an index for the ChatHistory collection to delete after some time
            # print(self.db['ChatHistory'].create_index( { "expireAt": 1 }, { "expireAfterSeconds": 0 }))
            self.db['Users'].create_index('expire', expireAfterSeconds=0)

        except Exception as e:
            print(f"Error init mongo: {e}")
    
    def login(self, email: str, password: str) -> str | None:
        collection = self.db['Users']

        query = {"email": email.strip(), "password": password.strip()}
        user = collection.find_one(query)

        if user:
            return user._id
        else:
            return None

    def signup(self, email: str, password: str) -> str | None:
        collection = self.db['Users']

        query = {"email": email.strip(), "password": password.strip()}
        user = collection.find_one(query)

        if user:
            return "User Already Exists"
        else:
            query = {"email": email.strip(), "password": password.strip()}
            user = collection.create_index(query)

            if user:
                return user._id
            else:
                return None