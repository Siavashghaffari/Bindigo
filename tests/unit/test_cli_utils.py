"""
Test CLI output formatting helpers.
"""

from bindigo.cli.utils import _wrap_text


class TestWrapText:
    """Test the text wrapper used by the error box."""

    def test_wraps_long_paragraph(self):
        """Long paragraphs are split to fit the box."""
        lines = _wrap_text("word " * 40, 20)
        assert all(len(line) <= 20 for line in lines)
        assert len(lines) > 1

    def test_preserves_explicit_line_breaks(self):
        """Installation instructions keep their own line structure."""
        text = "First line\n\n  indented line\nLast line"
        assert _wrap_text(text, 64) == [
            "First line",
            "",
            "  indented line",
            "Last line",
        ]

    def test_hard_splits_overlong_word(self):
        """A URL longer than the box cannot overflow the border."""
        lines = _wrap_text("https://example.com/" + "a" * 100, 30)
        assert all(len(line) <= 30 for line in lines)

    def test_empty_text(self):
        """Empty input produces no lines."""
        assert _wrap_text("", 64) == []
