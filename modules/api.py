import json
import requests

# // Get Login Token
#
def login(url, username, password):
    loginURL = url + "/login"
    payload = json.dumps({
        'username': username,
        'password': password
    })
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
    }
    login = requests.request("POST", loginURL, headers=headers, data=payload)
    response_json = login.json()
    token = response_json["token"]
    
    return token

# // Get Policies
#
def get_policies(url, token, severity=None, policy_status=None, policy_subtype=None, cloud=None, policy_label=None):
    
    params = []
    
    if cloud:
        params.append(f"cloud.type={cloud}")
        
    if policy_status:
        params.append(f"policy.enabled={policy_status}")
        
    if policy_subtype:
        params.append(f"policy.subtype={policy_subtype}")
        
    if severity:
        params.append(f"policy.severity={severity}")
        
    if policy_label:
        params.append(f"policy.label={policy_label}")        
        
    if params:
        policy_url = f"{url}/v2/policy?" + "&".join(params)
    else:
        policy_url = f"{url}/v2/policy"
    
    api_headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    }
    body = {}
    policies = (requests.request("GET", policy_url, headers=api_headers, data=body)).json()
    
    return policies

def apply_policies(url, token, policy_action, policy_id, payload=None):
    api_headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    }
    
    if policy_action == 'enable':
        policy_url = f"{url}/policy/{policy_id}/status/true"
        results = requests.request("PATCH", policy_url, headers=api_headers, data={})
        return results.status_code
    
    if policy_action == 'disable':
        policy_url = f"{url}/policy/{policy_id}/status/false"
        results = requests.request("PATCH", policy_url, headers=api_headers, data={})
        return results.status_code 
    
    if policy_action == 'update':
        policy_url = f"{url}/policy/{policy_id}"
        payload = json.dumps({
            'severity': payload.get('severity'),
            'labels': payload.get('labels', [])
        })
        results = requests.request("PUT", policy_url, headers=api_headers, data=payload)
        return results.status_code
    
    return None

# // Get Policies
#
def get_compliance(url, token):
    
    policy_url = f"{url}/compliance"
    
    api_headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    }
    body = {}
    compliance = (requests.request("GET", policy_url, headers=api_headers, data=body)).json()
    
    return compliance