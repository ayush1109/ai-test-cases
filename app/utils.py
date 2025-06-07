import requests
from urllib.parse import urlparse
from app.creds import USERS
from flask import jsonify

def is_valid_url(url):
    try:
        # Parse the URL to check format
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False

        # Optional: Check if the URL is reachable
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except Exception:
        return False
    

def extract_json_from_string(s):
    start = s.find('{')
    while start != -1:
        if '"test_cases"' in s[start:start+50]:  # crude check for start of block
            brace_count = 0
            for i in range(start, len(s)):
                if s[i] == '{':
                    brace_count += 1
                elif s[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_str = s[start:i+1]
                        return json_str
        start = s.find('{', start + 1)
    return None


def check_auth(username, password):
    return USERS.get(username) == password

def authenticate():
    return jsonify({"error": "Unauthorized"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}


def reorder_test_cases(parsed_result):
    reordered_test_cases = []
    for test_case in parsed_result["test_cases"]:
        reordered_test_cases.append({
        "title": test_case.get("title"),
        "steps": test_case.get("steps"),
        "expected_result": test_case.get("expected_result"),
        "tags": test_case.get("tags")
    })
    return reordered_test_cases