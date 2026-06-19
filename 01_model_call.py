"""Demo 1: make a basic LLM call without an agent persona."""

from services.azure_llm import AzureLLMClient


def main():
    llm = AzureLLMClient()
    messages = [
        {
            "role": "user",
            "content": "I accepted a job in Austin, Texas. Where should I live?",
        }
    ]

    print(f"\n{'=' * 60}")
    print("STEP 1: BUILD THE MESSAGE")
    print("=" * 60)
    print(messages)

    print(f"\n{'=' * 60}")
    print("STEP 2: SEND MESSAGE TO THE LLM")
    print("=" * 60)
    answer = llm.chat(messages)

    print(f"\n{'=' * 60}")
    print("STEP 3: LLM RESPONSE")
    print("=" * 60)
    print(answer)


if __name__ == "__main__":
    main()
