# src/database/upload_data.py

from src.db.db_connection import MongoDBConnection

def upload_user_data(data: dict):
    """
    Upload user data to MongoDB.
    Ensures database and collection are created if they don't exist.
    """
    mongo = MongoDBConnection()
    mongo.connect()

    collection = mongo.get_collection()

    result = collection.insert_one(data)
    print(f"Data inserted with ID: {result.inserted_id}")

    mongo.close()


if __name__ == "__main__":
    # Example usage: new user data
    user_input = {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 22
    }
    upload_user_data(user_input)
