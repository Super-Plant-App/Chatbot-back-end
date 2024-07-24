from pymongo.mongo_client import MongoClient
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

        except Exception as e:
            print(f"Error init mongo: {e}")
    
    def login(self, email: str, password: str) -> str | None:
        collection = self.db['Users']

        query = {"email": email.strip(), "password": password.strip()}
        user = collection.find_one(query)

        if user:
            return str(user['_id'])
        else:
            return "Wrong Credentials"

    def signup(self, email: str, password: str) -> str | None:
        collection = self.db['Users']

        query = {"email": email.strip(), "password": password.strip()}
        user = collection.find_one(query)

        if user:
            return "User Already Exists"
        else:
            query = {"email": email.strip(), "password": password.strip()}
            user = collection.insert_one(query)

            if user:
                return str(user.inserted_id)
            else:
                return "User Already Exists"