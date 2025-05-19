from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv

load_dotenv()
# Optional: Use your own Chrome instance by uncommenting:
browser = Browser(
    config=BrowserConfig(
        headless=True
    )
)
async def main():
    agent = Agent(
        task="Go to https://www.saucedemo.com/ and generate functional test cases for the website. Please give output in simple english sentences.",
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
        # browser=browser  # Uncomment to use your own Chrome browser
    )
    result = await agent.run()
    # print(str(result.final_result).split('done\': {\'text\':')[1].split(',')[0])
    print(result.has_errors)
    # with open('output.txt', 'w', encoding="utf-8") as file:
    #     file.write(str(result.final_result).split('done\': {\'text\':')[1].split('}')[0].replace(', \'success\': True', ''))
    return str(result.final_result).split('done\': {\'text\':')[1].split('}')[0].replace(', \'success\': True', '')