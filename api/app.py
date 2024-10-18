from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from backend.rule_parser import create_rule
from backend.rule_evaluator import evaluate_rule
from backend.rule_combiner import combine_rules
from database.schema import db,save_rule, load_rule  # Import save_rule and load_rule functions
from backend.ast_node import Node  # Import the Node class

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

rules = {}  # In-memory storage for rules (optional, used in parallel with MongoDB)

# Create Rule Endpoint
@app.route("/create_rule", methods=["POST"])
def create_rule_endpoint():
    try:
        rule_string = request.json.get("rule_string")
        if not rule_string:
            return jsonify({"error": "Rule string is required"}), 400

        # Create AST from the rule string
        ast = create_rule(rule_string)

        # Generate a unique rule ID
        rule_id = f"rule{len(rules) + 1}"

        # Check if the rule already exists in MongoDB
        existing_rule = db.rules.find_one({'_id': rule_id})  # Ensure you have db configured
        if existing_rule:
            return jsonify({"error": "Rule with this ID already exists."}), 400

        # Save the rule to MongoDB, serializing the Node to a dictionary
        save_rule(rule_id, rule_string, ast.to_dict())

        # Store the rule temporarily if needed
        rules[rule_id] = ast

        return jsonify({"rule_id": rule_id, "ast": ast.to_dict()})  # Return the AST representation as a dictionary

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the error to the console
        return jsonify({"error": str(e)}), 400


# Combine Rules Endpoint
@app.route("/combine_rules", methods=["POST"])
def combine_rules_endpoint():
    try:
        rule_ids = request.json.get("rule_ids")  # Expecting a list of rule IDs
        if not rule_ids:
            return jsonify({"error": "Rule IDs are required."}), 400

        rules = []
        for rule_id in rule_ids:
            rule = load_rule(rule_id)
            if rule is None:
                return jsonify({"error": f"Rule with ID {rule_id} not found."}), 404
            rules.append(rule['ast'])  # Assuming `ast` is the correct field to use

        # Use the combine_rules function to combine the ASTs
        combined_ast = combine_rules(rules, operator="AND")  # Or "OR" based on your requirement

        # Optionally, save the combined rule back to MongoDB or return the AST
        combined_rule_id = f"combined_rule{len(rules) + 1}"  # Generate a new ID
        save_rule(combined_rule_id, ' AND '.join(rule_ids), combined_ast.to_dict())

        return jsonify({"combined_rule_id": combined_rule_id, "ast": combined_ast.to_dict()}), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the error to the console
        return jsonify({"error": str(e)}), 400




# Evaluate Rule Endpoint
@app.route("/evaluate_rule", methods=["POST"])
def evaluate_rule_endpoint():
    try:
        rule_id = request.json.get("rule_id")
        user_data = request.json.get("user_data")
        
        # Load rule from MongoDB
        rule = load_rule(rule_id)
        
        if not rule:
            return jsonify({"error": "Rule not found"}), 404
        
        # Evaluate the rule's AST with the user data
        result = evaluate_rule(rule['ast'], user_data)
        
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
