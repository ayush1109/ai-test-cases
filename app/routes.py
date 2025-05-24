# app/routes.py
from app import app
from flask import jsonify
import asyncio
import signal
# from .demo import main
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
load_dotenv()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# def shutdown_handler(signum, frame):
#     print("Shutdown signal received, closing browser...")
#     loop.run_until_complete(browser.close())
#     print("Browser closed.")
#     exit(0)

# # Register signal handlers
# signal.signal(signal.SIGINT, shutdown_handler)
# signal.signal(signal.SIGTERM, shutdown_handler)


@app.route('/testcases', methods=['GET'])
def testCases():
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main())
    return result

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Welcome to the API'})


@app.teardown_appcontext
def close_browser_on_teardown(exception):
    # Not called on SIGINT, only on context teardown.
    pass
#Add more routes as needed




async def main():
    # Optional: Use your own Chrome instance by uncommenting:
    browser = Browser(
        config=BrowserConfig(
            headless=True
        )
    )
    try:
        agent = Agent(
            task="Go to https://www.saucedemo.com/ and generate functional test cases for the website. Please give output in simple english sentences.",
            llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
            browser=browser  # Uncomment to use your own Chrome browser
        )
        result = await agent.run()
        # print(str(result.final_result).split('done\': {\'text\':')[1].split(',')[0])
        print(result.has_errors)
        # with open('output.txt', 'w', encoding="utf-8") as file:
        #     file.write(str(result.final_result).split('done\': {\'text\':')[1].split('}')[0].replace(', \'success\': True', ''))
        return str(result.final_result).split('done\': {\'text\':')[1].split('}')[0].replace(', \'success\': True', '')
    finally:
        await browser.close()