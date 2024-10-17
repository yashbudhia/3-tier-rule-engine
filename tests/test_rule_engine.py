import unittest
from backend.rule_parser import create_rule
from backend.rule_combiner import combine_rules
from backend.rule_evaluator import evaluate_rule

class TestRuleEngine(unittest.TestCase):
    
    def test_create_rule(self):
        rule = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule)
        self.assertIsNotNone(ast)

    def test_combine_rules(self):
        rule1 = create_rule("age > 30")
        rule2 = create_rule("salary > 50000")
        combined_ast = combine_rules([rule1, rule2], "AND")
        self.assertEqual(combined_ast.value, "AND")
    
    def test_evaluate_rule(self):
        rule = create_rule("age > 30 AND salary > 50000")
        data = {"age": 35, "salary": 60000}
        result = evaluate_rule(rule, data)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
