import unittest
import json
from api.app import app, rule_counter, rules_cache

class RuleEngineEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Initialize the Flask test client
        self.app.testing = True
        global rule_counter
        rule_counter = 1  # Reset rule counter before each test
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
            self.assertEqual(response.status_code, 200)  # Expecting 200 for success
            data = json.loads(response.data)
            self.assertIn('rule_id', data)
            self.assertIn('ast', data)

    def test_combine_rules_success(self):
        # First, create two rules to combine
        response1 = self.app.post('/create_rule', 
                                  data=json.dumps({"rule_string": "age > 25"}), 
                                  content_type='application/json')
        data1 = json.loads(response1.data)
        rule_id1 = data1['rule_id']  # Dynamically retrieve rule ID from response

        response2 = self.app.post('/create_rule', 
                                  data=json.dumps({"rule_string": "income < 50000"}), 
                                  content_type='application/json')
        data2 = json.loads(response2.data)
        rule_id2 = data2['rule_id']  # Dynamically retrieve rule ID from response

        # Now, attempt to combine them
        response = self.app.post('/combine_rules', 
                                 data=json.dumps({"rule_ids": [rule_id1, rule_id2]}), 
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('combined_rule_id', data)
        self.assertIn('ast', data)

    def test_combine_rules_rule_not_found(self):
        # Test combining rules with a non-existent rule ID
        response = self.app.post('/combine_rules', 
                                 data=json.dumps({"rule_ids": ["non_existent_rule"]}), 
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Rule with ID 'non_existent_rule' not found.")

    def test_evaluate_rule_success(self):
        # First, create a rule to evaluate
        response = self.app.post('/create_rule', 
                                 data=json.dumps({"rule_string": "age > 25"}), 
                                 content_type='application/json')
        data = json.loads(response.data)
        rule_id = data['rule_id']  # Dynamically retrieve rule ID

        # Now, evaluate the rule
        response = self.app.post('/evaluate_rule', 
                                 data=json.dumps({"rule_id": rule_id, "user_data": {"age": 30}}), 
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)

if __name__ == '__main__':
    unittest.main()
