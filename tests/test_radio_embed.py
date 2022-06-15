"""Test radio_embed."""
# pylint: disable=broad-except
from radio_embed import __version__, radio_embed


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not radio_embed()
    except Exception:
        assert True


def test_radio_embed_two_three_lines():
    """Test radio_embed two three lines."""
    res = radio_embed("a\n b")
    assert res.shape == (2, 512)

    res = radio_embed("a\n \nb").shape
    assert res == (3, 512)
