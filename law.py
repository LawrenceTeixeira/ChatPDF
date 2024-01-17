import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

# Load the variables from .env
load_dotenv(".env")

## MongoDB vector database settings
# initialize MongoDB python client
MONGODB_ATLAS_CLUSTER_URI = os.getenv("MONGODB_ATLAS_CLUSTER_URI")

uri = "mongodb+srv://lawrence:766587La@inpi.gijwroc.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri )

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)