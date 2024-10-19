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
    base_id = rule_id  # Keep the original rule ID for appending suffixes
    suffix_counter = 1
    
    while True:
        try:
            rule_data = {
                "_id": rule_id,
                "rule_string": rule_string,
                "ast": ast,  # Ensure ast is a dictionary when passed in
                "created_at": datetime.now(),
                "modified_at": datetime.now()
            }

            rules_collection.insert_one(rule_data)
            break  # If the insertion is successful, exit the loop

        except Exception as e:
            # Check for duplicate key error and update the rule_id
            if "E11000" in str(e):
                rule_id = f"{base_id}_{suffix_counter}"
                suffix_counter += 1
            else:
                # If it's a different error, raise it
                raise e



def load_rule(rule_id):
    rule_data = rules_collection.find_one({'_id': rule_id})  # Adjust based on your MongoDB setup
    if rule_data:
        # Deserialize the AST back into a Node object
        rule_data['ast'] = Node.from_dict(rule_data['ast'])  # Convert back to Node
        return rule_data
    return None
