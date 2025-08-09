import rich
import asyncio
from connection import config
from pydantic import BaseModel
from agents import (
    Agent, OutputGuardrailTripwireTriggered, Runner, 
    input_guardrail, GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered, output_guardrail
)

# 🎯 Exercise #2 
# Objective: Create a father agent & guardrail to stop the child from running if the temperature is below 26°C.

class WeatherCheck(BaseModel):
    response: str
    tooCold: bool

# 👨‍👦 Father Agent
father_agent = Agent(
    name="Father Agent",
    instructions="""
    👨‍👦 You are a caring and protective father ❤️.  
Your cheerful child 🧒 is asking to go for a run 🏃‍♂️ outside.  

- If the temperature is **below 26°C** 🌡️:  
    * tooCold: true  
    * response: ❄️ It's too chilly outside! Please wait until the weather warms up 🌞.  

- If the temperature is **26°C or above** 🌤️:  
    * tooCold: false  
    * response: ✅ You may go for a run! Stay safe, have fun, and drink plenty of water 💧.  
    """,
    output_type=WeatherCheck
)


# 🛡️ INPUT GUARDRAIL
@input_guardrail
async def father_input_guardrail(context, agent: Agent, input: str) -> GuardrailFunctionOutput:
    result = await Runner.run(
        father_agent,
        input,
        run_config=config
    )
    rich.print("[bold cyan]🔍 Temperature Check:[/bold cyan]", result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.tooCold
    )

# 🧒 Child Agent
child_agent = Agent(
    name="Child Agent",
    instructions="You are an excited child 🏃‍♂️ asking your father to go running outside.",
    input_guardrails=[father_input_guardrail]
)

# 🚀 Main Execution
async def main():
    try:
        temperature_info = "The outside temperature is 24°C."
        result = await Runner.run(
            child_agent,
            temperature_info,
            run_config=config
        )
        rich.print("[bold green]🌞 Run Approved:[/bold green]", result.final_output)

    except InputGuardrailTripwireTriggered:
        rich.print("[bold red]❌ Run Blocked:[/bold red] Too cold to go outside! ❄️")


if __name__ == "__main__":
    asyncio.run(main())
