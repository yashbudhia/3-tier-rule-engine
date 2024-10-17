document.getElementById('rule-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const ruleInput = document.getElementById('rule-input').value;
    const response = await fetch('/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_string: ruleInput })
    });
    const result = await response.json();
    document.getElementById('rule-message').innerText = `Rule created: ${result.rule_id}`;
});

document.getElementById('combine-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const combineInput = document.getElementById('combine-input').value;
    const ruleIds = combineInput.split(',').map(id => id.trim());
    const response = await fetch('/combine_rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_ids: ruleIds })
    });
    const result = await response.json();
    document.getElementById('combine-message').innerText = `Combined Rule created: ${result.combined_rule_id}`;
});

document.getElementById('evaluate-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const ruleId = document.getElementById('evaluate-rule-id').value;
    const dataInput = document.getElementById('evaluate-data').value;
    const userData = JSON.parse(dataInput);
    const response = await fetch('/evaluate_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_id: ruleId, user_data: userData })
    });
    const result = await response.json();
    document.getElementById('evaluate-message').innerText = `Evaluation result: ${result.result}`;
});
