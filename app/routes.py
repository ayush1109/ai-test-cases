# app/routes.py
from app import app
from flask import jsonify, request
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
from app.utils import extract_json_from_string, is_valid_url, reorder_test_cases
from app.middleware import requires_auth
import json
import codecs
load_dotenv()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.route('/testcases', methods=['POST'])
@requires_auth
def testCases():
    # Create a new event loop for this thread
    data = request.get_json()
    url = data.get('url')
    if(is_valid_url(url)):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(main(url))
        return result
    else:
        return jsonify({'message': 'Please check url', 'status': 'fail'}), 400, {"Content-Type": "application/json"}

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Welcome to the API'})

@app.teardown_appcontext
def close_browser_on_teardown(exception):
    # Not called on SIGINT, only on context teardown.
    pass

async def main(url):
    browser = Browser(
        config=BrowserConfig(
            headless=True
        )
    )
    try:
        agent = Agent(
            task="""
Go to {url}.

Analyze the page's UI and DOM structure carefully.

Your task is to generate a set of **realistic and high-coverage functional test cases** based on the current web page.

⚙️ Requirements:
- Focus only on **functional tests** (not unit or performance).
- Interact with elements on the page like a real user would (e.g., login form, buttons, dropdowns).
- Include both **positive and negative** test scenarios.
- Assume no prior knowledge of the app — rely only on the visible UI and DOM.
- You must generate **at least 10 unique test cases**.

📦 Output Format:
Return the test cases in the following **JSON structure**:

```json
{{
  "test_cases": [
    {{
      "title": "Short summary of the test",
      "steps": [
        "Step-by-step user actions"
      ],
      "expected_result": "What should happen if the test passes",
      "tags": ["positive" or "negative", "login", etc.]
    }}
  ]
}}
""".format(url=url),
            llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
            browser=browser
        )
        result = await agent.run()
        response_str = str(result.final_result)        
        result = extract_json_from_string(response_str)
        unescaped_result = codecs.decode(result, 'unicode_escape')
        parsed_result = json.loads(unescaped_result)
        # reordered_test_cases = reorder_test_cases(parsed_result)
        if result:
            return jsonify({"status": "success", "result" : parsed_result}), 200, {"Content-Type": "application/json"}
        else:
            return jsonify({"status": "fail", "result": "Could not generate test cases!! Please try again. If the issue persists, please contact "
            "raghav.suneja686@gmail.com and gargayush308@gmail.com"}), 500, {"Content-Type": "application/json"}  
    except Exception as e:
        return jsonify({"status": "fail", "result": str(e)}), 500, {"Content-Type": "application/json"}

    finally:
        await browser.close()