"""Demo 3: combine persona, knowledge, tools, and memory in one agent."""

from services.azure_llm import AzureLLMClient

from agents import HousingAgent


def main():
    llm = AzureLLMClient()
    agent_with_memory = HousingAgent(llm)

    components = agent_with_memory.describe_components()
    print(f"\n{'=' * 60}")
    print("STEP 1: THE FOUR COMPONENTS OF THIS AGENT")
    print("=" * 60)
    print(f"\n1. Persona\n{components['persona']}")
    print(f"\n2. Knowledge\n{components['knowledge']}")
    print(f"\n3. Tools\n{components['tools']}")
    print(f"\n4. Memory (before the request)\n{components['memory']}")

    print(f"\n{'=' * 60}")
    print("STEP 2: FIRST REQUEST")
    print("=" * 60)
    agent_with_memory.run(
        "Find a home near Austin for a family with two children.",
        trace=True,
    )
    print(f"\nMemory after the first request:\n{agent_with_memory.memory}")

    follow_up = (
        "Based on what I shared earlier, which home would best fit my family "
        "while keeping the rent under $2,400 per month?"
    )

    print(f"\n{'=' * 60}")
    print("STEP 3: SAME FOLLOW-UP WITHOUT PRIOR MEMORY")
    print("=" * 60)
    fresh_agent = HousingAgent(llm)
    answer_without_memory = fresh_agent.run(
        follow_up,
        max_rent=2400,
        trace=True,
    )

    print(f"\n{'=' * 60}")
    print("STEP 4: SAME FOLLOW-UP WITH PRIOR MEMORY")
    print("=" * 60)
    answer_with_memory = agent_with_memory.run(
        follow_up,
        max_rent=2400,
        trace=True,
    )

    print(f"\n{'=' * 60}")
    print("STEP 5: COMPARE THE RESPONSES")
    print("=" * 60)
    print(f"\nWithout prior memory:\n{answer_without_memory}")
    print(f"\nWith prior memory:\n{answer_with_memory}")
    print(
        "\nThe fresh agent should ask for the missing household context instead of "
        "guessing. The agent with memory can use the earlier detail that the family "
        "includes two children to make a recommendation."
    )


if __name__ == "__main__":
    main()
