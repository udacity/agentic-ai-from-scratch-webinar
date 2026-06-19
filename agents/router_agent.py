"""Agent that chooses a bounded workflow route."""


class RouterAgent:
    ROUTES = {"housing", "neighborhood", "full-search"}

    def __init__(self, llm):
        self.llm = llm

    def route(self, request):
        route = self.llm.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "Route the request to exactly one label: housing, neighborhood, "
                        "or full-search. Use full-search when the user wants a complete "
                        "recommendation. Return only the label."
                    ),
                },
                {"role": "user", "content": request},
            ],
            temperature=0,
            max_tokens=20,
        ).lower()
        return route if route in self.ROUTES else "full-search"
