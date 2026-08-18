"""
Unit tests for scripts/eval_false_positive_rate.py (issue #3).

Pure-logic tests against synthetic scores -- no trained model or
legit-vessel holdout dataset required.
"""

import pytest

from scripts.eval_false_positive_rate import compute_false_positive_rate


class TestComputeFalsePositiveRate:
    def test_computes_correct_rate_on_mixed_scores(self):
        y_true_legit = [0, 0, 0, 0, 0]
        y_pred_scores = [0.9, 0.2, 0.6, 0.1, 0.8]  # 3 of 5 >= 0.5
        result = compute_false_positive_rate(y_true_legit, y_pred_scores, threshold=0.5)

        assert result["total_legit_vessels_checked"] == 5
        assert result["false_positives"] == 3
        assert result["false_positive_rate"] == pytest.approx(0.6)
        assert result["threshold"] == 0.5

    def test_boundary_score_equal_to_threshold_counts_as_flag(self):
        y_true_legit = [0]
        y_pred_scores = [0.5]
        result = compute_false_positive_rate(y_true_legit, y_pred_scores, threshold=0.5)
        assert result["false_positives"] == 1
        assert result["false_positive_rate"] == 1.0

    def test_all_below_threshold_gives_zero_rate(self):
        y_true_legit = [0, 0, 0]
        y_pred_scores = [0.1, 0.2, 0.3]
        result = compute_false_positive_rate(y_true_legit, y_pred_scores, threshold=0.5)
        assert result["false_positive_rate"] == 0.0

    def test_all_at_or_above_threshold_gives_full_rate(self):
        y_true_legit = [0, 0, 0]
        y_pred_scores = [0.5, 0.7, 0.99]
        result = compute_false_positive_rate(y_true_legit, y_pred_scores, threshold=0.5)
        assert result["false_positive_rate"] == 1.0

    def test_default_threshold_is_half(self):
        y_true_legit = [0, 0]
        y_pred_scores = [0.51, 0.49]
        result = compute_false_positive_rate(y_true_legit, y_pred_scores)
        assert result["threshold"] == 0.5
        assert result["false_positives"] == 1

    def test_raises_on_mismatched_lengths(self):
        with pytest.raises(ValueError):
            compute_false_positive_rate([0, 0, 0], [0.1, 0.2])

    def test_raises_on_empty_scores(self):
        with pytest.raises(ValueError):
            compute_false_positive_rate([], [])
