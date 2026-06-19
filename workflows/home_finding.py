"""Deterministic workflow coordinator for the routed demo."""

from agents import HousingAgent, NeighborhoodAgent, RecommendationAgent, RouterAgent


class HomeFindingWorkflow:
    def __init__(self, llm):
        self.router = RouterAgent(llm)
        self.housing = HousingAgent(llm)
        self.neighborhood = NeighborhoodAgent(llm)
        self.recommender = RecommendationAgent(llm)

    @staticmethod
    def _show_stage(number, name, content):
        print(f"\n{'=' * 60}")
        print(f"STEP {number}: {name}")
        print(f"{'=' * 60}")
        print(content)

    @staticmethod
    def _handoff(sender, recipient, content):
        """Create and display a simple agent-to-agent message."""
        message = {
            "from": sender,
            "to": recipient,
            "content": content,
        }
        print(f"\n--- HANDOFF: {sender} -> {recipient} ---")
        print(message)
        return message

    def run(self, request):
        self._show_stage(0, "USER GOAL", request)

        route = self.router.route(request)
        self._show_stage(1, "ROUTER AGENT", f"Selected route: {route}")

        if route == "housing":
            result = self.housing.run(request)
            self._show_stage(2, "HOUSING AGENT", result)
            return result
        if route == "neighborhood":
            result = self.neighborhood.run(request)
            self._show_stage(2, "NEIGHBORHOOD AGENT", result)
            return result

        housing_result = self.housing.run(request)
        self._show_stage(2, "HOUSING AGENT", housing_result)
        print(f"\n[HousingAgent private memory]\n{self.housing.memory}")
        print(
            "[Workflow note] Other agents cannot see this memory automatically; "
            "the workflow must send them a message."
        )

        housing_message = self._handoff(
            "HousingAgent", "NeighborhoodAgent", housing_result
        )
        neighborhood_result = self.neighborhood.run(housing_message["content"])
        self._show_stage(3, "NEIGHBORHOOD AGENT", neighborhood_result)

        housing_research = self._handoff(
            "HousingAgent", "RecommendationAgent", housing_result
        )
        neighborhood_research = self._handoff(
            "NeighborhoodAgent", "RecommendationAgent", neighborhood_result
        )

        final_result = self.recommender.run(
            request,
            housing_research["content"],
            neighborhood_research["content"],
        )
        self._show_stage(4, "RECOMMENDATION AGENT", final_result)
        return final_result
