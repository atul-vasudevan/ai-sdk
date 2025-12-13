from ai_lib import AIClient

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase
from deepeval import assert_test


def test_summarise_text_quality():
    client = AIClient(app_name="deepeval-test")

    original_text = (
        "Bella is a 3-year-old indoor cat. This policy covers her for accidental "
        "injuries and some specified illnesses, subject to annual limits and an excess. "
        "Routine check-ups are not covered under this policy."
    )

    summary = client.summarise_text(original_text)

    metric = GEval(
        name="policy-summary-quality",
        criteria=(
            "The summary should capture the key points: "
            "1) pet type and basic context, "
            "2) that the policy covers accidental injuries and some illnesses, "
            "3) that there are limits/excesses, "
            "4) that routine check-ups are not covered."
        ),
        evaluation_params=["input", "actual_output"],
    )

    test_case = LLMTestCase(
        input=original_text,
        actual_output=summary,
        expected_output=None,
    )

    assert_test(test_case, [metric])
