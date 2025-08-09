import rich
import asyncio
from connection import config
from pydantic import BaseModel
from agents import (
    Agent, OutputGuardrailTripwireTriggered, Runner, 
    input_guardrail, GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered, output_guardrail
)

# 🎯 Exercise #1 
# Objective: Create an agent with an input guardrail that blocks admin-related tasks.
# Test Prompt: "I want to change my class timings 😭😭"
# Expected: InputGuardrailTripwireTriggered should be called and logged.

class AdminTask(BaseModel):
    response: str
    isAdminTask: bool

# 👨‍🏫 Teacher Agent
teacher_agent = Agent(
    name="Teacher Agent",
    instructions="""
   📚👨‍🏫 You are a dedicated Teacher Agent.  
Your job is to assist students with **study-related questions** only.  

- If a student makes an **admin-related request** (e.g., class timings ⏰, fee details 💰, schedule changes 📅):  
    * isAdminTask: true  
    * response: ⚠️ This is an administrative matter. Please reach out to the admin office 🏢 for assistance.  

- If the request is **study-related**:  
    * isAdminTask: false  
    * response: ✅ Here’s the academic help you requested 📖.  
    """,
    output_type=AdminTask
)

# 🛡️ INPUT GUARDRAIL
@input_guardrail
async def teacher_input_guardrail(context, agent: Agent, input: str) -> GuardrailFunctionOutput:
    result = await Runner.run(
        teacher_agent, 
        input, 
        run_config=config
    )
    rich.print("[bold cyan]🔍 Input Check:[/bold cyan]", result.final_output)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isAdminTask
    )

# 🛡️ OUTPUT GUARDRAIL
@output_guardrail
async def teacher_output_guardrail(context, agent: Agent, output: str) -> GuardrailFunctionOutput:
    result = await Runner.run(
        teacher_agent,
        output,
        run_config=config
    )
    rich.print("[bold magenta]📤 Output Check:[/bold magenta]", result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isAdminTask
    )

# 🎓 Student Agent
student_agent = Agent(
    name="Student Agent",
    instructions="You are a student 🧑‍🎓 politely requesting to change class timings 😥.",
    input_guardrails=[teacher_input_guardrail],
    output_guardrails=[teacher_output_guardrail]
)

# 🚀 Main Execution
async def main():
    try:
        result = await Runner.run(
            student_agent, 
            'I want to change my class timings 😭😭', 
            run_config=config
        )
        rich.print(result.final_output)
        rich.print("[bold green]📚 Study-related task accepted![/bold green]")

    except InputGuardrailTripwireTriggered:
        rich.print("[bold red]⛔ Input Blocked:[/bold red] This is an Admin Task! 🏢")

    except OutputGuardrailTripwireTriggered:
        rich.print("[bold yellow]⚠️ Output Blocked:[/bold yellow] Response contains Admin Task! 🏢")    

if __name__ == "__main__":
    asyncio.run(main())
