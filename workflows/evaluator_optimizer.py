"""Evaluator-optimizer pattern for agent collaboration."""

from agents import HousingAgent, NeighborhoodAgent


class EvaluatorOptimizerWorkflow:
    """Ask one agent to propose, another to critique, then revise."""

    def __init__(self, llm):
        self.housing_agent = HousingAgent(llm)
        self.neighborhood_agent = NeighborhoodAgent(llm)

    @staticmethod
    def _show_step(number, title, content):
        print(f"\n{'=' * 60}")
        print(f"STEP {number}: {title}")
        print("=" * 60)
        print(content)

    @staticmethod
    def _message(sender, recipient, purpose, content):
        return {
            "from": sender,
            "to": recipient,
            "purpose": purpose,
            "content": content,
        }

    def run(self, request):
        self._show_step(1, "USER -> HOUSING AGENT", request)

        proposal = self.housing_agent.run(request)
        self._show_step(2, "HOUSING AGENT PROPOSAL", proposal)
        print(f"\n[HousingAgent memory after proposal]\n{self.housing_agent.memory}")

        review_request = self._message(
            "HousingAgent",
            "NeighborhoodAgent",
            "Evaluate this proposal against known neighborhood facts",
            proposal,
        )
        self._show_step(3, "PROPOSAL -> NEIGHBORHOOD EVALUATOR", review_request)

        critique = self.neighborhood_agent.review(proposal)
        self._show_step(4, "NEIGHBORHOOD AGENT CRITIQUE", critique)

        feedback = self._message(
            "NeighborhoodAgent",
            "HousingAgent",
            "Revise the proposal using this critique",
            critique,
        )
        self._show_step(5, "CRITIQUE -> HOUSING OPTIMIZER", feedback)
        print(
            "\n[Memory available to HousingAgent before revision]\n"
            f"{self.housing_agent.memory}"
        )

        revision_request = (
            "Use your short-term memory to recall the original user goal and your "
            "first proposal. Revise that proposal using this evaluator feedback:\n\n"
            f"{critique}\n\n"
            "Correct unsupported claims and choose one option."
        )
        final_answer = self.housing_agent.run(revision_request, trace=True)
        self._show_step(6, "REVISED RECOMMENDATION -> USER", final_answer)
        print(f"\n[HousingAgent memory after revision]\n{self.housing_agent.memory}")
        return final_answer
