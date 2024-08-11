import dspy
from dspy.mocks.dummies import DummyLM


def test_basic_example():
    class BasicQA(dspy.Signature):
        """Answer questions with short factoid answers."""

        question = dspy.InputField()
        answer = dspy.OutputField(desc="often between 1 and 5 words")

    # Example completions generated by a model for reference
    completions = [
        dspy.Prediction(
            rationale="I recall that during clear days, the sky often appears this color.",
            answer="blue",
        ),
        dspy.Prediction(
            rationale="Based on common knowledge, I believe the sky is typically seen as this color.",
            answer="green",
        ),
        dspy.Prediction(
            rationale="From images and depictions in media, the sky is frequently represented with this hue.",
            answer="blue",
        ),
    ]

    # Pass signature to MultiChainComparison module
    compare_answers = dspy.MultiChainComparison(BasicQA)

    # Call the MultiChainComparison on the completions
    question = "What is the color of the sky?"
    lm = DummyLM(["my rationale", "blue"])
    dspy.settings.configure(lm=lm)
    final_pred = compare_answers(completions, question=question)

    assert final_pred.rationale == "my rationale"
    assert final_pred.answer == "blue"
