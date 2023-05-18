"""Module Database"""
from pymongo import MongoClient


# MongoDB Connection Manager
class MongoDB:
    """Class for connect and close MongoDB"""

    def __init__(self, dri, mydatabase):
        self.client = MongoClient(dri)
        self.db = self.client[mydatabase]

    def close_connection(self):
        """Method to close connection"""
        self.client.close()
