"""Tests for the shared spam-penalty ramp helper (#1370)."""

import pytest

from gittensor.utils.utils import spam_penalty_multiplier


class TestSpamPenaltyMultiplier:
    def test_full_score_at_or_under_threshold(self):
        assert spam_penalty_multiplier(0, 2, 3) == 1.0
        assert spam_penalty_multiplier(2, 2, 3) == 1.0

    def test_linear_ramp_over_threshold(self):
        assert spam_penalty_multiplier(3, 2, 3) == pytest.approx(2 / 3)
        assert spam_penalty_multiplier(4, 2, 3) == pytest.approx(1 / 3)

    def test_reaches_zero_at_full_overage(self):
        assert spam_penalty_multiplier(5, 2, 3) == 0.0

    def test_clamps_to_zero_past_full_overage(self):
        assert spam_penalty_multiplier(50, 2, 3) == 0.0

    def test_zero_width_reproduces_hard_cliff(self):
        # zero_at_overage=0 is the old binary behavior: 1.0 at/under, 0.0 over.
        assert spam_penalty_multiplier(2, 2, 0) == 1.0
        assert spam_penalty_multiplier(3, 2, 0) == 0.0
