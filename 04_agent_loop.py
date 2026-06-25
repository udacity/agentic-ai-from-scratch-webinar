"""Demo 4: let the model choose a tool in a bounded agent loop."""

from agents import HousingAgent
from services.azure_llm import AzureLLMClient
from workflows.agent_loop import AgentLoop


def main():
    agent = HousingAgent(AzureLLMClient())

    # ReAct means reasoning plus acting: the model chooses actions, the runtime
    # executes them, and the model reasons over the observations.
    # ReAct-style flow:
    # Goal -> Decide -> Act -> Observe -> Decide -> Finish
    # We define an agent, give it to a loop, then run the loop with the user's
    # goal. The loop asks the agent to decide, runs allowed tools, observes the
    # results, and repeats until the agent returns a final answer.
    runtime = AgentLoop(agent)

    # Goal: the user states what they want the agent to accomplish.
    goal = "Find an Austin-area rental for my family under $2,400 per month."

    print(f"\n{'=' * 60}")
    print("STEP 1: USER GOAL")
    print("=" * 60)
    print(goal)

    # The loop handles Decide -> Act -> Observe -> Decide -> Finish.
    answer = runtime.run(goal)

    print(f"\n{'=' * 60}")
    print("STEP 2: FINAL ANSWER")
    print("=" * 60)
    print(answer)


if __name__ == "__main__":
    main()
