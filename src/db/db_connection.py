# src/database/db_connection.py

from pymongo import MongoClient
from config.config import DataBaseConfig
from config.logger import logging
from config.exception import CustomException
from dataclasses import dataclass
import sys


@dataclass
class MongoConfig:
    uri = DataBaseConfig.DATABASE_URL
    db_name = DataBaseConfig.DATABASE_NAME
    collection_name = DataBaseConfig.DB_COLLECTION_NAME


class MongoDBConnection:
    def __init__(self, uri = None):
        self.uri = uri if uri is not None else MongoConfig.uri
        self.db_name = MongoConfig.db_name
        self.collection_name = MongoConfig.collection_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            # Explicitly create DB (Mongo will create if it doesn’t exist)
            self.db = self.client[self.db_name]
            print(f"Connected to MongoDB, database: {self.db_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e

    def get_collection(self,):
        """Get collection; if it doesn't exist, create it."""
        if self.collection_name not in self.db.list_collection_names():
            self.db.create_collection(self.collection_name)
            print(f"Created new collection: {self.collection_name}")
        return self.db[self.collection_name]

    def close(self):
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")
