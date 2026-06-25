"""Agent that reasons about homes matching a user's goal."""

import json

from knowledge import HOUSING_RECOMMENDATION_KNOWLEDGE
from tools.housing_search import search_listings


class HousingAgent:
    """A small agent made from persona, knowledge, tools, and memory."""

    PERSONA = (
        "You are Becky, a practical and encouraging Austin housing agent. "
        "You recommend homes that match the user's needs, explain tradeoffs, "
        "and clearly identify facts the user should verify."
    )

    # Shared knowledge can be reused by agents with different roles.
    KNOWLEDGE = HOUSING_RECOMMENDATION_KNOWLEDGE

    MEMORY_POLICY = (
        "When the current request refers to information shared earlier, inspect "
        "Prior memory. If Prior memory is empty, do not guess or recommend a home. "
        'Respond exactly: "I don\'t have the earlier context in this conversation. '
        'Please tell me about your household needs first."'
    )

    def __init__(self, llm):
        self.llm = llm

        # Memory: conversation facts retained while this object is running.
        self.memory = []

        # Tools: Python functions the agent is allowed to call.
        self.tools = {
            "search_listings": search_listings,
        }

    def describe_components(self):
        """Expose the building blocks so they are easy to show in the webinar."""
        return {
            "persona": self.PERSONA,
            "knowledge": self.KNOWLEDGE,
            "tools": list(self.tools),
            "memory": self.memory,
        }

    def decide(self, request, observations):
        """Choose the next action; the external runtime executes it."""
        # Decide: the model chooses the next step, but does not execute it.
        # With no observations, it should ask for a tool. With observations, it
        # should finish with an answer grounded in the tool result.
        if observations:
            guidance = "The search is complete. Choose finish using the observation."
        else:
            guidance = "You have no listing facts yet. Choose search_listings first."

        response = self.llm.chat(
            [
                {
                    "role": "system",
                    "content": (
                        f"# Persona\n{self.PERSONA}\n\n"
                        f"# Knowledge\n- " + "\n- ".join(self.KNOWLEDGE) + "\n\n"
                        "# Available actions\n"
                        '1. {"action":"search_listings","arguments":{"max_rent":2500}}\n'
                        '2. {"action":"finish","answer":"your recommendation"}\n\n'
                        "When the goal includes a maximum rent, use that exact value "
                        "for search_listings. "
                        "Return exactly one JSON object and no Markdown. "
                        "Never invent a tool name or listing fact."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Goal: {request}\n"
                        f"Memory: {json.dumps(self.memory)}\n"
                        f"Observations: {json.dumps(observations)}\n"
                        f"Next-step guidance: {guidance}"
                    ),
                },
            ],
            temperature=0,
            max_tokens=250,
        )

        start = response.find("{")
        end = response.rfind("}") + 1
        if start < 0 or end <= start:
            raise ValueError(f"The agent did not return JSON: {response}")
        return json.loads(response[start:end])

    def run(self, request, max_rent=2500, trace=False):
        # Take a snapshot before storing the current request. This is the context
        # that was genuinely available from earlier turns.
        prior_memory = list(self.memory)

        if trace:
            print(f"\n[Goal] {request}")
            print(f"[Memory read] Prior memory before this request: {prior_memory}")

        # Goal: remember the user's current request.
        user_event = {
            "role": "user",
            "content": request,
            "max_rent": max_rent,
        }
        self.remember(user_event)
        if trace:
            print(f"[Memory write] Stored user event: {user_event}")

        # Act: use a tool to obtain facts the model does not already know.
        if trace:
            print(f"[Tool call] search_listings(max_rent={max_rent})")
        matches = self.tools["search_listings"](max_rent)
        if trace:
            print(f"[Tool observation] {matches}")

        # Observe -> Finish: give the model the tool results so it can answer.
        if trace:
            print(f"[Memory read] Sending prior memory to the model: {prior_memory}")
            print("[Model call] Sending persona, knowledge, memory, and tool results")
        answer = self.llm.chat(
            [
                {
                    "role": "system",
                    "content": (
                        f"# Persona\n{self.PERSONA}\n\n"
                        f"# Knowledge\n- " + "\n- ".join(self.KNOWLEDGE) + "\n\n"
                        f"# Memory policy\n{self.MEMORY_POLICY}\n\n"
                        "Use only facts from the Current request, Knowledge, Prior "
                        "memory, and Tool results. "
                        "Do not "
                        "invent neighborhood qualities, schools, amenities, contact "
                        "details, or actions you cannot perform."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"# Current request\n{request}\n\n"
                        f"# Prior memory\n{prior_memory}\n\n"
                        f"# Tool used\nsearch_listings(max_rent={max_rent})\n\n"
                        f"# Tool results\n{matches}"
                    ),
                },
            ],
            temperature=0,
        )
        assistant_event = {
            "role": "assistant",
            "content": answer,
        }
        self.remember(assistant_event)
        if trace:
            print(f"[Agent answer] {answer}")
            print(f"[Memory write] Stored agent answer: {assistant_event}")
            print(f"[Memory state] Memory now contains {len(self.memory)} events")
        return answer

    def remember(self, event):
        """Store one event in the agent's short-term memory."""
        self.memory.append(event)
