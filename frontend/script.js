const baseUrl = 'http://localhost:5000'; // Define the base URL for your API

// Handle the creation of a rule
document.getElementById('rule-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const ruleInput = document.getElementById('rule-input').value;

    const response = await fetch(`${baseUrl}/create_rule`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_string: ruleInput })
    });

    const result = await response.json();
    if (!response.ok) {
        document.getElementById('rule-message').innerText = `Error: ${result.error || 'Unknown error'}`;
    } else {
        document.getElementById('rule-message').innerText = `Rule created: ${result.rule_id}`;
        document.getElementById('ast-representation').innerText = `AST: ${JSON.stringify(result.ast, null, 2)}`; // Display the AST
    }
});

// Handle combining of rules
document.getElementById('combine-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const combineInput = document.getElementById('combine-input').value;
    const ruleIds = combineInput.split(',').map(id => id.trim());

    const response = await fetch(`${baseUrl}/combine_rules`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_ids: ruleIds })
    });

    const result = await response.json();
    if (!response.ok) {
        document.getElementById('combine-message').innerText = `Error: ${result.error || 'Unknown error'}`;
    } else {
        document.getElementById('combine-message').innerText = `Combined Rule created: ${result.combined_rule_id}`;
    }
});

// Handle evaluation of a rule
document.getElementById('evaluate-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const ruleId = document.getElementById('evaluate-rule-id').value;
    const dataInput = document.getElementById('evaluate-data').value;

    // Safely parse JSON user data
    let userData;
    try {
        userData = JSON.parse(dataInput);
    } catch (error) {
        document.getElementById('evaluate-message').innerText = 'Error: Invalid JSON data';
        return;
    }

    const response = await fetch(`${baseUrl}/evaluate_rule`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_id: ruleId, user_data: userData })
    });

    const result = await response.json();
    if (!response.ok) {
        document.getElementById('evaluate-message').innerText = `Error: ${result.error || 'Unknown error'}`;
    } else {
        document.getElementById('evaluate-message').innerText = `Evaluation result: ${result.result}`;
    }
});

// Handle modifying a rule
document.getElementById('modify-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const ruleId = document.getElementById('modify-rule-id').value;
    const newRuleString = document.getElementById('modify-rule-string').value;

    const response = await fetch(`${baseUrl}/modify_rule/${ruleId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ modifications: { rule_string: newRuleString } })
    });

    const result = await response.json();
    if (!response.ok) {
        document.getElementById('modify-message').innerText = `Error: ${result.error || 'Unknown error'}`;
    } else {
        document.getElementById('modify-message').innerText = `Rule modified successfully.`;
    }
});
