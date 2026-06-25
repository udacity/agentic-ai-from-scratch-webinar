"""Demo 1: make a basic LLM call without an agent persona."""

from services.azure_llm import AzureLLMClient


def main():
    llm = AzureLLMClient()
    austin_messages = [
        {
            "role": "user",
            "content": "I accepted a job in Austin, Texas. Where should I live?",
        }
    ]

    print(f"\n{'=' * 60}")
    print("STEP 1: ASK ABOUT OUR AUSTIN RELOCATION USE CASE")
    print("=" * 60)
    print(austin_messages)

    austin_answer = llm.chat(austin_messages)
    print(f"\nLLM: {austin_answer}")

    cake_messages = [
        {
            "role": "user",
            "content": "How do I bake a cake?",
        }
    ]

    print(f"\n{'=' * 60}")
    print("STEP 2: ASK SOMETHING OUTSIDE OUR USE CASE")
    print("=" * 60)
    print(cake_messages)

    cake_answer = llm.chat(cake_messages)
    print(f"\nLLM: {cake_answer}")

    print(f"\n{'=' * 60}")
    print("STEP 3: OBSERVE THE LACK OF SCOPE")
    print("=" * 60)
    print(
        "The LLM answered both questions because we have not given it a persona, "
        "domain boundary, or trusted application knowledge."
    )


if __name__ == "__main__":
    main()
