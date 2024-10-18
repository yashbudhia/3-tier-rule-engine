import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from backend.ast_node import Node  # Adjust the path as needed based on your project structure


# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv('DATABASE_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['rule_engine']

rules_collection = db['rules']

def save_rule(rule_id, rule_string, ast):
    rule_data = {
        "_id": rule_id,
        "rule_string": rule_string,
        "ast": ast,  # ast should already be a dictionary when passed in
        "created_at": datetime.now(),
        "modified_at": datetime.now()
    }
    rules_collection.insert_one(rule_data)


def load_rule(rule_id):
    rule_data = db.rules.find_one({'_id': rule_id})  # Adjust based on your MongoDB setup
    if rule_data:
        # Ensure that Node is defined in this scope
        rule_data['ast'] = Node.from_dict(rule_data['ast'])
        return rule_data
    return None

