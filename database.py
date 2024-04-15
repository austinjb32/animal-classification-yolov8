
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://austinjb32:123Gmail@cluster0.6j6xq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["class", "timestamp"],
        "properties": {
            "class": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "timestamp": {
                "bsonType": "date",
                "description": "must be a date and is required"
            }
        }
    }
}

client['main'].command('create', 'animal_log',
                     validator=schema,
                     validationLevel='moderate')

