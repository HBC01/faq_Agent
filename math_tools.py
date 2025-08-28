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
def add_nums(num1:int , num2:int) -> int:
    add=num1+num2
    return f"Called Add nums Tool\n num1 {num1} + num2 {num2}\n Total {add}"

@function_tool
def multiple_nums(num1:int , num2:int) -> int:
    multiples = num1 * num2
    return f"Called Multiple  Tool\n num1 {num1} * num2 {num2}\n Total {multiples}"


# Agent definition
adding_agent = Agent(
    name="Adding Agent",
    instructions="""
    You are a helpful Adding Agent.use add_nums tool for adding numbers then give total sum  to user
    also can use multiple tool if users says for multiply numbers
    """,
    tools=[add_nums,multiple_nums]
)

# Run configuration
my_config = RunConfig(
    model=gemini_model,
    model_provider=extra_client,
    tracing_disabled=True
)

# Main loop
async def main():
    print("Maths Tools are called! write 2 nums  (type 'exit' to quit)\n")
    while True:
        user_input = input("write : ")
        if user_input.lower() == "exit":
            print("Math Tool Finished!")
            break
        result = await Runner.run(adding_agent, input=user_input, run_config=my_config)
        print("Answer is:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
2