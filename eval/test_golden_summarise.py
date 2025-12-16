import json
import os
import pytest
from ai_lib.client import AIClient
from deepeval.scorer import Scorer

CASES_PATH = os.path.join(os.path.dirname(__file__), "golden_cases_summarise.json")

with open(CASES_PATH, "r") as f:
    CASES = json.load(f)


@pytest.mark.parametrize("case", CASES)
def test_summarise_golden_case(case):
    client = AIClient(app_name="golden-eval")
    generated = client.summarise_text(case["input"])
    expected = case["expected"]

    scorer = Scorer()
    score = scorer.rouge_score(
        prediction=generated,
        target=expected,
        score_type="rougeL"
    )
    print(f"\nCase: {case['id']}")
    print("Generated:", generated)
    print("Expected:", expected)
    print("ROUGE-L F1:", score)
    if os.getenv("AI_LIB_SUMMARISATION_BACKEND") == "hf":
        assert score >= 0.50, f"ROUGE score {score} below threshold"
    else:
        assert score >= 0.05, f"ROUGE score {score} below threshold"