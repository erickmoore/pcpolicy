from modules.api import apply_policies
import json

def apply_policy(policy_details, new_severity, new_label, remove_label, enable, disable, url, token, timestamp):
    actions = []
    if enable or disable:
        actions.append({'type': "enable" if enable else "disable", 'payload': None})
    if new_severity:
        actions.append({'type': "severity", 'payload': json.dumps(policy_details)})
    if new_label or remove_label:
        actions.append({'type': "label", 'payload': json.dumps(policy_details)})

    for action in actions:
        status_code = apply_policies(url, token, action['type'], policy_details['id'], action['payload'])
        handle_action_result(status_code, action['type'], policy_details, timestamp)
        