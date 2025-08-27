import os
import asyncio
from dotenv import load_dotenv


from openai import AsyncOpenAI
from agents import Agent, Runner, RunConfig, function_tool,OpenAIChatCompletionsModel

load_dotenv()

Gemini_Key = os.getenv("Gemini_Api_Key")
if not Gemini_Key:
    raise ValueError("Gemini key not found in .env")

# Gemini client
extra_client = AsyncOpenAI(
    api_key=Gemini_Key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model
gemini_model = OpenAIChatCompletionsModel(
    openai_client=extra_client,
    model="gemini-2.0-flash"
)

# Tool definition
@function_tool
def faq_return(ques: str) -> str:
    Q = ques.lower().strip()
    return f"Sorry, your question '{Q}' is not in the FAQs."

# Agent definition
Faq_Agent = Agent(
    name="FAQ Agent",
    instructions="""
    You are a helpful FAQ bot. 
    If questions are not similar to the predefined FAQs, then use the tool faq_return.

    Predefined FAQs:
    - Q: What is your name?
      A: My name is FAQ Bot.
    - Q: What can you do?
      A: I can answer simple frequently asked questions.
    - Q: Who created you?
      A: I was created using the OpenAI Agent SDK by Hazoor Ahmed.
    - Q: How smart are you?
      A: I am just smart enough to answer basic FAQs!
    - Q: Can you help me with coding?
      A: Yes, but only in a very basic way.
    """,
    tools=[faq_return]
)

# Run configuration
my_config = RunConfig(
    model=gemini_model,
    model_provider=extra_client,
    tracing_disabled=True
)

# Main loop
async def main():
    print("FAQ Bot is running! Ask me something (type 'exit' to quit)\n")
    while True:
        user_input = input("write : ")
        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break
        result = await Runner.run(Faq_Agent, input=user_input, run_config=my_config)
        print("Answer is:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
2