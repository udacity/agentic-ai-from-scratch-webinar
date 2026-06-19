"""Demo 6: an LLM router coordinates a complete agentic workflow."""

from services.azure_llm import AzureLLMClient

from workflows.home_finding import HomeFindingWorkflow


def main():
    workflow = HomeFindingWorkflow(AzureLLMClient())
    workflow.run("Help my family choose an Austin-area rental under $2,500.")


if __name__ == "__main__":
    main()
