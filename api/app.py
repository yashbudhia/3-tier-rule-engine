from flask import Flask, request, jsonify
from backend.rule_parser import create_rule
from backend.rule_evaluator import evaluate_rule
from backend.rule_combiner import combine_rules

app = Flask(__name__)

rules = {}  # In-memory storage for rules

@app.route("/create_rule", methods=["POST"])
def create_rule_endpoint():
    rule_string = request.json.get("rule_string")
    ast = create_rule(rule_string)
    rule_id = f"rule{len(rules)+1}"
    rules[rule_id] = ast
    return jsonify({"rule_id": rule_id, "ast": str(ast)})

@app.route("/combine_rules", methods=["POST"])
def combine_rules_endpoint():
    rule_ids = request.json.get("rule_ids")
    selected_rules = [rules[rule_id] for rule_id in rule_ids]
    combined_rule = combine_rules(selected_rules)
    combined_rule_id = f"rule{len(rules)+1}"
    rules[combined_rule_id] = combined_rule
    return jsonify({"combined_rule_id": combined_rule_id, "ast": str(combined_rule)})

@app.route("/evaluate_rule", methods=["POST"])
def evaluate_rule_endpoint():
    rule_id = request.json.get("rule_id")
    user_data = request.json.get("user_data")
    rule = rules.get(rule_id)
    if not rule:
        return jsonify({"error": "Rule not found"}), 404
    result = evaluate_rule(rule, user_data)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
