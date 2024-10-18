from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from backend.rule_parser import create_rule
from backend.rule_evaluator import evaluate_rule
from backend.rule_combiner import combine_rules

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

rules = {}  # In-memory storage for rules

@app.route("/create_rule", methods=["POST"])
def create_rule_endpoint():
    try:
        rule_string = request.json.get("rule_string")
        if not rule_string:
            return jsonify({"error": "Rule string is required"}), 400
        ast = create_rule(rule_string)
        rule_id = f"rule{len(rules) + 1}"
        rules[rule_id] = ast
        return jsonify({"rule_id": rule_id, "ast": str(ast)})  # Return the AST representation
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the error to the console
        return jsonify({"error": str(e)}), 400

@app.route("/combine_rules", methods=["POST"])
def combine_rules_endpoint():
    try:
        rule_ids = request.json.get("rule_ids")
        selected_rules = [rules[rule_id] for rule_id in rule_ids if rule_id in rules]
        combined_rule = combine_rules(selected_rules)
        combined_rule_id = f"rule{len(rules) + 1}"
        rules[combined_rule_id] = combined_rule
        return jsonify({"combined_rule_id": combined_rule_id, "ast": str(combined_rule)})  # Return the combined rule's AST
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/evaluate_rule", methods=["POST"])
def evaluate_rule_endpoint():
    try:
        rule_id = request.json.get("rule_id")
        user_data = request.json.get("user_data")
        rule = rules.get(rule_id)
        if not rule:
            return jsonify({"error": "Rule not found"}), 404
        result = evaluate_rule(rule, user_data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
