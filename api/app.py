from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.rule_parser import create_rule
from backend.rule_evaluator import evaluate_rule
from backend.rule_combiner import combine_rules
from database.schema import db, rules_collection, save_rule, load_rule
from backend.ast_node import Node
import re

app = Flask(__name__)
CORS(app)

# In-memory cache of rules (optional, for quick access)
rules_cache = {}
rule_counter = 1  # Initialize a counter for rule IDs

# Attribute Catalog
VALID_ATTRIBUTES = {
    "age",
    "department",
    "salary",
    "experience",
    "performance_score",
    "location",
    "job_title",
    "tenure",
    "education_level",
    "skills"
}

def validate_rule_string(rule_string):
    """Validate the rule string for proper syntax."""
    if not re.search(r'(AND|OR)', rule_string):
        raise ValueError("Rule must contain at least one operator (AND/OR).")

def validate_attributes(condition):
    """Validate attributes against a predefined catalog."""
    key = list(condition.keys())[0]
    if key not in VALID_ATTRIBUTES:
        raise ValueError(f"Invalid attribute: {key}. Allowed attributes: {VALID_ATTRIBUTES}")

# Create Rule Endpoint
@app.route("/create_rule", methods=["POST"])
def create_rule_endpoint():
    global rule_counter  # Declare as global to modify the counter
    try:
        rule_string = request.json.get("rule_string")
        if not rule_string:
            return jsonify({"error": "Rule string is required"}), 400

        # Validate rule string
        validate_rule_string(rule_string)

        # Create AST from the rule string
        ast = create_rule(rule_string)

        # Validate attributes in the AST (pseudo-code, implement based on your AST structure)
        for operand in ast.get_operands():  # Assume get_operands() fetches operands
            validate_attributes(operand.value)

        # Generate a simple rule ID
        rule_id = f"rule{rule_counter}"
        rule_counter += 1  # Increment the counter for the next rule ID

        # Save the rule to MongoDB with unique rule_id logic
        save_rule(rule_id, rule_string, ast.to_dict())

        # Add to in-memory cache
        rules_cache[rule_id] = ast

        return jsonify({"rule_id": rule_id, "ast": ast.to_dict()}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Combine Rules Endpoint
@app.route("/combine_rules", methods=["POST"])
def combine_rules_endpoint():
    try:
        rule_ids = request.json.get("rule_ids")
        if not rule_ids:
            return jsonify({"error": "Rule IDs are required."}), 400

        rule_asts = []
        for rule_id in rule_ids:
            rule_data = load_rule(rule_id)
            if not rule_data:
                return jsonify({"error": f"Rule with ID '{rule_id}' not found."}), 404
            rule_asts.append(rule_data['ast'])

        # Combine the ASTs using AND (you can change the operator as needed)
        combined_ast = combine_rules(rule_asts, operator="AND")

        # Save the combined rule to MongoDB
        combined_rule_id = f"combined_rule{len(rules_cache) + 1}"
        save_rule(combined_rule_id, ' AND '.join(rule_ids), combined_ast.to_dict())

        return jsonify({"combined_rule_id": combined_rule_id, "ast": combined_ast.to_dict()}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Evaluate Rule Endpoint
@app.route("/evaluate_rule", methods=["POST"])
def evaluate_rule_endpoint():
    try:
        rule_id = request.json.get("rule_id")
        user_data = request.json.get("user_data")

        if not rule_id or not user_data:
            return jsonify({"error": "Rule ID and user data are required"}), 400

        # Load the rule from MongoDB
        rule_data = load_rule(rule_id)
        if not rule_data:
            return jsonify({"error": f"Rule with ID '{rule_id}' not found."}), 404

        # Evaluate the rule with the given user data
        result = evaluate_rule(rule_data['ast'], user_data)

        return jsonify({"result": result}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Modify Rule Endpoint
@app.route("/modify_rule/<rule_id>", methods=["PATCH"])
def modify_rule_endpoint(rule_id):
    try:
        modifications = request.json.get("modifications")
        if not modifications:
            return jsonify({"error": "Modifications are required."}), 400

        rule_data = load_rule(rule_id)
        if not rule_data:
            return jsonify({"error": f"Rule with ID '{rule_id}' not found."}), 404

        # Here you would implement logic to modify the AST based on the modifications provided
        # For simplicity, assuming modifications include new rule_string
        new_rule_string = modifications.get("rule_string")
        if new_rule_string:
            validate_rule_string(new_rule_string)
            new_ast = create_rule(new_rule_string)
            # Validate attributes in the new AST
            for operand in new_ast.get_operands():
                validate_attributes(operand.value)

            # Save the modified rule
            save_rule(rule_id, new_rule_string, new_ast.to_dict())

        return jsonify({"message": "Rule modified successfully."}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
