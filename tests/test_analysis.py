import pytest

from Gurshant.database_analysis import analyze_response


SCORE_FIELDS = ("relevance", "clarity", "conciseness", "completeness", "structure")


def test_analysis_returns_five_bounded_scores_and_explanations():
    result = analyze_response(
        "Explain photosynthesis and name its inputs",
        "Photosynthesis uses sunlight, water, and carbon dioxide.\n"
        "1. Plants produce glucose.\n2. Oxygen is released.",
    )

    assert all(isinstance(result[field], int) for field in SCORE_FIELDS)
    assert all(0 <= result[field] <= 100 for field in SCORE_FIELDS)
    assert result["explanations"]
    assert result["structure"] == 100


@pytest.mark.parametrize(
    ("prompt", "response"),
    [("", "answer"), ("   ", "answer"), ("question", ""), ("question", "  ")],
)
def test_analysis_rejects_empty_inputs(prompt, response):
    with pytest.raises(ValueError):
        analyze_response(prompt, response)


def test_long_unstructured_response_remains_in_score_range_and_explains_weaknesses():
    response = " ".join(["unrelatedword"] * 500)
    result = analyze_response("Explain photosynthesis", response)

    assert all(0 <= result[field] <= 100 for field in SCORE_FIELDS)
    assert result["conciseness"] < 100
    assert result["structure"] == 50
    assert any("long" in explanation.lower() for explanation in result["explanations"])


def test_short_relevant_response_includes_positive_explanation():
    result = analyze_response(
        "Explain photosynthesis", "Photosynthesis converts sunlight into energy."
    )
    assert result["explanations"]
