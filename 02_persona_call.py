"""Demo 2: give an LLM a persona, knowledge, and a clear scope."""

from services.azure_llm import AzureLLMClient


PERSONA_PROMPT = """
# Persona
You are Becky, a friendly and practical Austin relocation advisor.
You answer questions only about choosing a home or neighborhood in the Austin area.
If a question is outside that scope, respond exactly:
"I can only help with Austin-area housing and neighborhoods."

# Knowledge
- Cedar Park is suburban and quiet. A typical commute in this example is 35 minutes.
- Lakeway is walkable and family-friendly. But the commute downtown might be close to an hour.
- Downtown Austin is urban and lively with many parks, hiking trails, and outdoor activities nearby. A typical commute in this example is 8 minutes.
- Shorter commutes often involve tradeoffs in space, price, or neighborhood character.
- Housing details can change, so users should verify prices and availability.
""".strip()


def ask(llm, question):
    return llm.chat(
        [
            {"role": "system", "content": PERSONA_PROMPT},
            {"role": "user", "content": question},
        ]
    )


def main():
    llm = AzureLLMClient()

    print(f"\n{'=' * 60}")
    print("STEP 1: DEFINE PERSONA, KNOWLEDGE, AND SCOPE")
    print("=" * 60)
    print(PERSONA_PROMPT)

    in_scope = "Which neighborhood might suit a family that values walkability?"
    print(f"\n{'=' * 60}")
    print("STEP 2: ASK AN IN-PERSONA QUESTION")
    print("=" * 60)
    print(f"User: {in_scope}")
    in_scope_answer = ask(llm, in_scope)
    print(f"Becky: {in_scope_answer}")

    in_scope = "Why not downtown?"
    print(f"\n{'=' * 60}")
    print("STEP 3: ASK AN IN-PERSONA QUESTION")
    print("=" * 60)
    print(f"User: {in_scope}")
    in_scope_answer = ask(llm, in_scope)
    print(f"Becky: {in_scope_answer}")

    in_scope = "Is downtown better than the options you suggested"
    print(f"\n{'=' * 60}")
    print("STEP 4: ASK AN IN-PERSONA QUESTION")
    print("=" * 60)
    print(f"User: {in_scope}")
    in_scope_answer = ask(llm, in_scope)
    print(f"Becky: {in_scope_answer}")

    in_scope = "Suggest other neighborhoods"
    print(f"\n{'=' * 60}")
    print("STEP 5: ASK AN IN-PERSONA QUESTION")
    print("=" * 60)
    print(f"User: {in_scope}")
    in_scope_answer = ask(llm, in_scope)
    print(f"Becky: {in_scope_answer}")

    in_scope = "Now which one is best?"
    print(f"\n{'=' * 60}")
    print("STEP 6: ASK AN IN-PERSONA QUESTION")
    print("=" * 60)
    print(f"User: {in_scope}")
    in_scope_answer = ask(llm, in_scope)
    print(f"Becky: {in_scope_answer}")

    in_scope = "Which is best for the value I told you?"
    print(f"\n{'=' * 60}")
    print("STEP 7: ASK AN IN-PERSONA QUESTION")
    print("=" * 60)
    print(f"User: {in_scope}")
    in_scope_answer = ask(llm, in_scope)
    print(f"Becky: {in_scope_answer}")

    out_of_scope = "How do I bake sourdough bread?"
    print(f"\n{'=' * 60}")
    print("STEP 8: TEST THE PERSONA BOUNDARY")
    print("=" * 60)
    print(f"User: {out_of_scope}")
    out_of_scope_answer = ask(llm, out_of_scope)
    print(f"Becky: {out_of_scope_answer}")

    print(f"\n{'=' * 60}")
    print("STEP 9: OBSERVE THE DIFFERENCE")
    print("=" * 60)
    print("The same model answered inside its role and declined outside its role.")


if __name__ == "__main__":
    main()
