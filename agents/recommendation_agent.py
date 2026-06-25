"""Agent that combines specialist research into a final recommendation."""

from knowledge import HOUSING_RECOMMENDATION_KNOWLEDGE


class RecommendationAgent:
    # The recommendation agent and housing agent share domain facts and rules.
    KNOWLEDGE = HOUSING_RECOMMENDATION_KNOWLEDGE

    def __init__(self, llm):
        self.llm = llm

    def run(self, request, housing_result, neighborhood_result):
        return self.llm.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "Shared housing knowledge:\n- "
                        + "\n- ".join(self.KNOWLEDGE)
                        + "\n\n"
                        "Choose exactly one option, explain why, and state one thing "
                        "the user should verify before signing a lease. Use only facts "
                        "in the supplied request and agent research. Never add facts "
                        "about schools, safety, amenities, or property features."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Original request: {request}\nHousing research: {housing_result}"
                        f"\nNeighborhood research: {neighborhood_result}"
                    ),
                },
            ]
        )
