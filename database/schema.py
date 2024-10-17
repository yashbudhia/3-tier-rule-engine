from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['rule_engine']

rules_collection = db['rules']

def save_rule(rule_id, rule_string, ast):
    rule_data = {
        "_id": rule_id,
        "rule_string": rule_string,
        "ast": ast,
        "created_at": datetime.now(),
        "modified_at": datetime.now()
    }
    rules_collection.insert_one(rule_data)

def load_rule(rule_id):
    return rules_collection.find_one({"_id": rule_id})
