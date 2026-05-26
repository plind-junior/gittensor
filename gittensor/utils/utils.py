"""
GitTensor Utilities
"""

import os


def backoff_seconds(attempt: int, base: int = 5, cap: int = 30) -> int:
    return min(base * (2**attempt), cap)


def spam_penalty_multiplier(total_open: int, threshold: int, zero_at_overage: int) -> float:
    """Ramp the open-item spam multiplier down instead of snapping to zero (#1370).

    At or under ``threshold`` the multiplier is 1.0. Each item over fades it
    linearly, reaching 0.0 once ``zero_at_overage`` items past the threshold.
    A ``zero_at_overage`` of 0 reproduces the old hard 1.0/0.0 cliff.
    """
    overage = total_open - threshold
    if overage <= 0:
        return 1.0
    if zero_at_overage <= 0:
        return 0.0
    return max(0.0, 1.0 - overage / zero_at_overage)


def get_contract_address() -> str:
    """Get contract address. Override via CONTRACT_ADDRESS env var for dev/testing.

    Returns:
        Contract address string (env var override or constants.py default)
    """
    from gittensor.constants import CONTRACT_ADDRESS

    return os.environ.get('CONTRACT_ADDRESS') or CONTRACT_ADDRESS
