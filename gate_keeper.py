import rich
import asyncio
from connection import config
from pydantic import BaseModel
from agents import (Agent, Runner, input_guardrail, GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered
)

# 🎯 Exercise # 3 
# Objective: Make a Gate Keeper agent with an input guardrail to stop students from other schools.

class EntryCheck(BaseModel):
    response: str
    isOtherSchool: bool

# 🚪👮 Gate Keeper Agent (No guardrails here)
gate_keeper_agent = Agent(
    name="Gate Keeper Agent",
    instructions="""
    🚪 You are a strict yet fair gate keeper stationed at the entrance of "Our School".  

    🎯 Your duty:  
    - If a student belongs to any school other than **"Our School"**:  
        _ isOtherSchool: true  
        _ response: ❌ Access denied! This gate is strictly for "Our School" students only 🚷  

    - If a student is from **"Our School"**:  
        _ isOtherSchool: false  
        _ response: ✅ Welcome! Please enter and have a great day at school 🏫
    """,
    output_type=EntryCheck
)

# 🛡️ INPUT GUARDRAIL 
@input_guardrail
async def gate_keeper_input_guardrail(context, agent, input) -> GuardrailFunctionOutput:
    # ✅ Run the dedicated checking agent (not the "agent" param)
    result = await Runner.run(
        gate_keeper_agent,
        input,
        run_config=config
    )
    rich.print("💬 [bold cyan]🔍 Entry Check:[/bold cyan]", result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isOtherSchool
    )

# 🎒🧑‍🎓STUDENT AGENT 
student_agent = Agent(
    name="Student Agent",
    instructions="🎒 I am a student trying to enter the school.",
    input_guardrails=[gate_keeper_input_guardrail]
)

async def main():
    try:
        # ❌ Example: Other school student
        student_info = "I am from City Public School."
        result = await Runner.run(
            student_agent,
            student_info,
            run_config=config
        )
        rich.print("[bold green]✅ Entry Approved:[/bold green]", result.final_output)

    except InputGuardrailTripwireTriggered:
        rich.print("[bold red]🚫 Entry Blocked:[/bold red] You are from another school! 🛑")

if __name__ == "__main__":
    asyncio.run(main())
