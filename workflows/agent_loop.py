"""Runtime that coordinates an agent's decide-act-observe loop."""


class AgentLoop:
    """Execute only validated actions proposed by an agent."""

    def __init__(self, agent, max_steps=3):
        self.agent = agent
        self.max_steps = max_steps

    @staticmethod
    def _validate_max_rent(arguments):
        max_rent = arguments.get("max_rent")
        if not isinstance(max_rent, (int, float)) or not 500 <= max_rent <= 10_000:
            raise ValueError("max_rent must be a number between 500 and 10,000")
        return max_rent

    def run(self, request):
        # Decide-Act-Observe pattern:
        # 1. Decide: ask the agent what should happen next.
        # 2. Act: if the agent chose a tool, run that allowed tool in Python.
        # 3. Observe: store the tool result so the agent can use it next time.
        # The loop repeats until the agent decides to finish with an answer.

        # Goal: store the user's objective so the agent can see the task.
        user_event = {"role": "user", "content": request}
        self.agent.remember(user_event)
        print(f"[Memory write] Stored goal: {user_event}")
        observations = []

        for step in range(1, self.max_steps + 1):
            print(f"[Memory read] Agent sees: {self.agent.memory}")

            # Decide: ask the agent whether to use a tool or finish.
            decision = self.agent.decide(request, observations)
            action = decision.get("action")
            print(f"\n[Step {step} - Decision] {decision}")

            if action == "finish":
                if not observations:
                    raise ValueError("The agent must use a tool before finishing")

                # Finish: the agent has enough observations to answer the user.
                answer = decision.get("answer", "No answer was provided.")
                assistant_event = {"role": "assistant", "content": answer}
                self.agent.remember(assistant_event)
                print(f"[Memory write] Stored final answer: {assistant_event}")
                return answer

            if action not in self.agent.tools:
                raise ValueError(f"Tool is not allowed: {action}")

            max_rent = self._validate_max_rent(decision.get("arguments", {}))
            print(f"[Step {step} - Action] {action}(max_rent={max_rent})")

            # Act: run the allowed tool chosen by the agent.
            result = self.agent.tools[action](max_rent)

            # Observe: save the tool result so the next decision can use it.
            observation = {"tool": action, "result": result}
            observations.append(observation)
            self.agent.remember(observation)
            print(f"[Step {step} - Observation] {result}")
            print(f"[Memory write] Stored observation: {observation}")

        raise RuntimeError("The agent reached its step limit without finishing")
