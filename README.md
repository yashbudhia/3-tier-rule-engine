# 3-tier-rule-engine
a simple 3-tier rule engine application(Simple UI, API and Backend, Data) to determine user eligibility based on attributes like age, department, income, spend


# Project Structure

```
rule-engine-app/
│
├── backend/
│   ├── __init__.py           # Marks the directory as a Python package
│   ├── ast_node.py           # Contains the AST Node class
│   ├── rule_parser.py        # Contains rule parsing (create_rule function)
│   ├── rule_combiner.py      # Contains rule combination logic (combine_rules function)
│   ├── rule_evaluator.py     # Contains rule evaluation logic (evaluate_rule function)
│
├── api/
│   ├── __init__.py           # Marks the directory as a Python package
│   ├── app.py                # Flask API code
│
├── database/
│   ├── __init__.py           # Marks the directory as a Python package
│   ├── schema.py             # Database schema and connection
│
├── tests/
│   ├── test_rule_engine.py    # Unit tests for rule creation, combination, evaluation
│
├── frontend/
│   ├── index.html            # Simple UI to create and evaluate rules
│   ├── script.js             # Frontend logic (e.g., sending requests to API)
│   ├── styles.css            # CSS for the UI
│
├── README.md                 # Documentation for the project
├── requirements.txt          # Python dependencies (Flask, pymongo, etc.)
└── config.py                 # Configuration for API and database connection

```


# Error Handling

- Added checks if same rule is added twice or more

- for tests use while in root directory and having activated the virtual enviroment 

```
python -m unittest tests/test_rule_engine.py

```