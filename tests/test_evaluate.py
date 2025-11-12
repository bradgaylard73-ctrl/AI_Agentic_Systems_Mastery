from avatar_assistant.evaluate import basic_quality_score
def test_basic_quality_score():
    s = "# Summary\n\n- Point A\n- Point B\n\nAction: Do X"
    assert 0.5 <= basic_quality_score(s) <= 1.0
