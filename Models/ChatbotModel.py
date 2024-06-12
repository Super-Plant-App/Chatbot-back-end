from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
import dotenv

dotenv.load_dotenv()

class ChatbotModel:
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
            print(e)

    def load_history(self, user_id: str) -> list | None:
        history = []
        
        collection = self.db['ChatHistory']

        query = {"userId": ObjectId(user_id)}
        document = collection.find_one(query)

        if document:
            history = document['history']
            return history
        else:
            return None

    def update_history(self, history: list, user_id: str):
        collection = self.db['ChatHistory']

        # check first is there is a history or not
        query = {"userId": ObjectId(user_id)}
        document = collection.find_one(query)

        if document: # if there is a history, update it
            # Calculate new expiration time (1 hour from now)
            new_expiration_time = datetime.utcnow() + timedelta(minutes=1)
            
            update = {
                "$set": {
                    "history": history,
                    "expiration_time": new_expiration_time
                }
            }
            
            result = collection.update_one({"userId": ObjectId(user_id)}, update)

            if result.matched_count > 0:
                print("Document updated successfully.")   
                     
        else: # if there is no history, create new history and add it to the DB
            new_document = {
                "userId": ObjectId(user_id),
                "history": history,
                "expiration_time": datetime.utcnow() + timedelta(minutes=1)
            }

            insert_result = collection.insert_one(new_document)

            if insert_result.inserted_id:
                print("Document inserted successfully with _id:", insert_result.inserted_id)
            else:
                print("Failed to insert document.")
    

    def clear_history(self, user_id: str):
        collection = self.db['ChatHistory']

        filter_criteria = {"userId": user_id}
        res = collection.delete_one(filter_criteria)

        if res.deleted_count == 1:
            print("Document deleted successfully.")
        else:
            print("No matching document found.")
        

