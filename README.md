# Overview

- In this assignment, I designed and implemented a rule engine API that allows users to create, modify, combine, and evaluate rules based on user attributes. The core functionality includes:

    - Creating Rules: Users can define rules in a specific format, which are then parsed and stored in a database.
    - Modifying Rules: Users can update existing rules by providing new conditions, enhancing flexibility.
    - Combining Rules: Users can combine multiple rules into a single rule using logical operators.
    - Evaluating Rules: The engine evaluates rules against user-provided data to determine eligibility or validity based on specified criteria.
    - Error Handling and Validation: The API includes validation for rule syntax and attribute catalog, ensuring robust input handling.

Technology Choices :

- Flask

   - Simplicity and Flexibility: Flask is a micro web framework that allows for quick development and prototyping of APIs. Its lightweight    nature provides flexibility in structuring the application.

- MongoDB

   - Schema Flexibility: MongoDB is a NoSQL database that allows for dynamic schema design. This is beneficial for the rule engine, where the structure of rules may evolve over time.
   - Document-Based Storage: The document-oriented nature of MongoDB makes it easy to store complex data structures like rules and their AST representations in a natural format.
   - JSON-like Structure: MongoDB’s BSON format is inherently compatible with the JSON format used in our API, simplifying data interchange between the application and the database.

By combining Flask and MongoDB, the project leverages the strengths of both technologies to create a flexible, scalable, and easy-to-maintain rule engine API.


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
    - Endpoint: POST /create_rule
    - Description: Creates a rule from the provided rule string and stores it in the database.
    - Sample Request:

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

    - Endpoint: POST /combine_rules
    - Description: Combines multiple rules into a single AST.
    - Sample Request:



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

    - Endpoint: POST /evaluate_rule
    - Description: Evaluates a given rule’s AST against user attributes (JSON data).
    - Sample Request:

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

4. Modify a Rule (Bonus) 

    - Endpoint: PATCH /modify_rule/:ruleId
    - Sample Request:


bash
```
curl -X PATCH http://127.0.0.1:5000/modify_rule/rule1 \
-H "Content-Type: application/json" \
-d '{
    "modifications": {
        "rule_string": "age < 40 AND department = '\''Sales'\''"
    }
}'
```

Sample Response

json
```
{
  "message": "Rule modified successfully."
}
```



- There is also a frontend - to open cd frontend and run index.html


# Error Handling

- The API will return meaningful error messages in case of any issues, which can include invalid inputs, rule IDs that don’t exist, or server errors. (Bonus)

- Implement validations for attributes to be part of a catalog. (Bonus)

- Added checks if same rule is added twice or more - duplicates rules are created as -
  - for each rule with rule_id rule1
  - duplicates will be created as -> rule1_1 -> rule1_2

- for tests use while in root directory and having activated the virtual enviroment 

```
python -m unittest tests/test_rule_engine.py

```

# Sample Acceptable Rules:

1. rule1:
    This rule checks if the user is either in Sales and over 30 or in Marketing and under 25, with additional conditions on salary or experience.

    plaintext
```
((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
```
2. rule2:
This rule applies to users in the Marketing department who are over 30, with conditions on salary or experience.

plaintext
```
(age > 30 AND department = 'Marketing') AND (salary > 20000 OR experience > 5)
```

3. rule3:
This rule checks if the user is younger than 40 or works in the HR department, with additional conditions on salary.

plaintext
```
(age < 40 OR department = 'HR') AND salary > 30000
```

4. rule4:
This rule checks if the user’s experience is greater than 10 years or their income is less than 60000.

plaintext
```
(experience > 10 OR income < 60000)
```


You can instruct users to enter these rules through the frontend's rule input field, and these samples demonstrate the flexibility of combining conditions using AND, OR, and comparison operators (>, <, >=, <=, etc.).

- Evaluating rules

Input Field:
Enter user attributes to evaluate against the combined rule as a JSON object.

Example:

json
```
{
  "age": 35,
  "department": "Sales",
  "salary": 60000,
  "experience": 4
}
```
