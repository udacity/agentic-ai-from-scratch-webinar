"""Demo 6: an LLM router coordinates a complete agentic workflow."""

from services.azure_llm import AzureLLMClient

from workflows.home_finding import HomeFindingWorkflow


def main():
    # Routed multi-agent flow:
    # Request -> Route -> Delegate -> Handoff -> Synthesize -> Final answer
    # A router chooses which specialist agent or workflow path should handle the
    # request, then specialist outputs are handed off and combined.
    workflow = HomeFindingWorkflow(AzureLLMClient())
    workflow.run("Help my family choose an Austin-area rental under $2,500.")


if __name__ == "__main__":
    main()
