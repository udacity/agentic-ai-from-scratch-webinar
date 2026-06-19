"""Agent that evaluates neighborhoods."""

from tools.housing_search import get_neighborhoods


class NeighborhoodAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, research_input):
        return self.llm.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "You evaluate neighborhoods mentioned in the supplied research. "
                        "Use only the supplied area data and identify tradeoffs. "
                        "Ignore unsupported claims in the other agent's research. "
                        "Do not make claims about schools, safety, amenities, or distance "
                        "unless those facts appear in the area data."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Research request or agent message:\n{research_input}"
                        f"\nArea data: {get_neighborhoods()}"
                    ),
                },
            ]
        )

    def review(self, proposal):
        """Evaluate another agent's proposal instead of answering the user."""
        return self.llm.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "You are a strict neighborhood evaluator. Review another "
                        "agent's housing proposal using only the supplied area data. "
                        "Return three short sections: Supported, Unsupported, and "
                        "Suggested Revision. Flag every claim that is absent from the "
                        "area data; do not add your own facts."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Proposal to review:\n{proposal}\n\n"
                        f"Area data:\n{get_neighborhoods()}"
                    ),
                },
            ]
        )
