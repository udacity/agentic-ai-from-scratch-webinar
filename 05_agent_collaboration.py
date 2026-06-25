"""Demo 5: agents improve an answer with evaluator-optimizer feedback."""

from services.azure_llm import AzureLLMClient
from workflows.evaluator_optimizer import EvaluatorOptimizerWorkflow


def main():
    # Evaluator-optimizer flow:
    # Request -> Proposal -> Evaluation -> Revision -> Final answer
    # One agent drafts an answer, another agent critiques it, and the first
    # agent improves the answer using that feedback.
    team = EvaluatorOptimizerWorkflow(AzureLLMClient())
    team.run("Find a family-friendly Austin-area rental under $2,500.")


if __name__ == "__main__":
    main()
