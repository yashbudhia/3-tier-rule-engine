import unittest
import json
from api.app import app, rule_counter, rules_cache, create_rule  # Ensure create_rule is imported

class CreateRuleEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Initialize the Flask test client
        self.app.testing = True
        global rule_counter
        rule_counter = 0  # Reset rule counter before each test
        rules_cache.clear()  # Clear the in-memory cache before each test

    def test_create_rule_success(self):
        # Test valid rule creation with different rule strings
        rule_strings = [
            "age > 25",
            "income < 50000",
            "spend >= 1000"
        ]

        for rule_string in rule_strings:
            response = self.app.post('/create_rule', 
                                     data=json.dumps({"rule_string": rule_string}), 
                                     content_type='application/json')
            
            # Debug prints
            print(f"Testing rule: '{rule_string}'")
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data.decode('utf-8')}")  # Decode to string for better readability
            
            self.assertEqual(response.status_code, 200)  # Expecting 200 for success
            data = json.loads(response.data)
            self.assertIn('rule_id', data)
            self.assertIn('ast', data)

    def test_create_rule_missing_rule_string(self):
        # Test missing rule_string in the request
        response = self.app.post('/create_rule', 
                                 data=json.dumps({}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Rule string is required")


    def test_create_rule_invalid_input(self):
        # Test invalid input that raises ValueError
        def mock_create_rule(rule_string):
            raise ValueError("Failed to parse rule, remaining items in stack: []")

        # Replace the original create_rule function with the mock
        original_create_rule = create_rule
        globals()['create_rule'] = mock_create_rule

        response = self.app.post('/create_rule', 
                                 data=json.dumps({"rule_string": "invalid_rule"}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Failed to parse rule, remaining items in stack: []")  # Match the actual error message

        # Restore the original function
        globals()['create_rule'] = original_create_rule

if __name__ == '__main__':
    unittest.main()