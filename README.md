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
│   ├── test_rule_engine.py   # Unit tests for rule creation, combination, evaluation
|   ├── __init__.py    
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


# Installation Steps

- Clone the repository:

- Create Virtual Environment:
```
python -m venv myenv
source myenv/bin/activate  # For Linux/Mac
myenv\Scripts\activate  # For Windows

```
- Install Dependencies:
```
pip install -r requirements.txt
```

- MongoDB Configuration:

    Provide details about setting up MongoDB if not running locally.
    Sample connection string in .env file:

```
DATABASE_URI=mongodb://localhost:27017

```

- Run the Flask server:
in the terminal cd to api from the root directory and run the command
```
flask run
```

- API Endpoints (Use Either Curl or Postman for api testing)

1. Create Rule:
        Endpoint: POST /create_rule
        Description: Creates a rule from the provided rule string and stores it in the database.
        Sample Request:

bash
```
curl -X POST http://127.0.0.1:5000/create_rule -H "Content-Type: application/json" -d '{"rule_string": "age > 30 AND income < 50000"}'
```

Sample Response:

json

```

    {
      "rule_id": "rule1",
      "AST": {...}
    }


```

2. Combine Rules:

    Endpoint: POST /combine_rules
    Description: Combines multiple rules into a single AST.
    Sample Request:



bash

```
curl -X POST http://127.0.0.1:5000/combine_rules -H "Content-Type: application/json" -d '{"rule_ids": ["rule1", "rule2"]}'
```

Sample Response:

json
```
    {
      "combined_AST": {...}
    }
```
3. Evaluate Rule:

    Endpoint: POST /evaluate_rule
    Description: Evaluates a given rule’s AST against user attributes (JSON data).
    Sample Request:

bash
```
curl -X POST http://127.0.0.1:5000/evaluate_rule -H "Content-Type: application/json" -d '{"data": {"age": 35, "income": 40000}}'
```

Sample Response:

json
```
{
  "result": true
}
```
- There is also a frontend - to open cd frontend and run index.html


# Error Handling

- Added checks if same rule is added twice or more - duplicates rules are created as -
  - for each rule with rule_id rule1
  - duplicates will be created as -> rule1_1 -> rule1_2

- for tests use while in root directory and having activated the virtual enviroment 

```
python -m unittest tests/test_rule_engine.py

```