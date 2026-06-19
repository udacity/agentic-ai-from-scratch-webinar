"""Demo 4: let the model choose a tool in a bounded agent loop."""

from agents import HousingAgent
from services.azure_llm import AzureLLMClient
from workflows.agent_loop import AgentLoop


def main():
    agent = HousingAgent(AzureLLMClient())
    runtime = AgentLoop(agent)
    goal = "Find an Austin-area rental for my family under $2,400 per month."

    print(f"\n{'=' * 60}")
    print("STEP 1: USER GOAL")
    print("=" * 60)
    print(goal)

    answer = runtime.run(goal)

    print(f"\n{'=' * 60}")
    print("STEP 2: FINAL ANSWER")
    print("=" * 60)
    print(answer)


if __name__ == "__main__":
    main()
