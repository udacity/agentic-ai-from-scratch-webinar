"""Demo 5: agents improve an answer with evaluator-optimizer feedback."""

from services.azure_llm import AzureLLMClient
from workflows.evaluator_optimizer import EvaluatorOptimizerWorkflow


def main():
    team = EvaluatorOptimizerWorkflow(AzureLLMClient())
    team.run("Find a family-friendly Austin-area rental under $2,500.")


if __name__ == "__main__":
    main()
