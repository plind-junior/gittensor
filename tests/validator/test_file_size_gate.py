"""The file-size gate brackets UTF-8 size by char count to skip a redundant encode."""

from gittensor.constants import MAX_FILE_SIZE_BYTES
from gittensor.validator.utils.tree_sitter_scoring import exceeds_max_file_bytes


def test_small_ascii_is_under_limit():
    assert exceeds_max_file_bytes('def foo():\n    return 1\n') is False


def test_empty_is_under_limit():
    assert exceeds_max_file_bytes('') is False


def test_char_count_over_limit_short_circuits_true():
    # More characters than the byte budget => definitely over (no encode needed).
    assert exceeds_max_file_bytes('x' * (MAX_FILE_SIZE_BYTES + 1)) is True


def test_ambiguous_band_multibyte_over_limit():
    # '€' is 3 UTF-8 bytes. char_count <= MAX < char_count*4 forces the exact
    # encode; 500k chars => 1.5MB bytes => over.
    content = '€' * (MAX_FILE_SIZE_BYTES // 2)
    assert len(content) <= MAX_FILE_SIZE_BYTES  # in the ambiguous band
    assert exceeds_max_file_bytes(content) is True


def test_ambiguous_band_multibyte_under_limit():
    # 300k '€' chars => 900KB bytes => under, even though char_count*4 > MAX.
    content = '€' * 300_000
    assert len(content) * 4 > MAX_FILE_SIZE_BYTES  # in the ambiguous band
    assert exceeds_max_file_bytes(content) is False
