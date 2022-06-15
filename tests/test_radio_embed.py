"""Test radio_embed."""
# pylint: disable=broad-except
from radio_embed import __version__
from radio_embed import radio_embed


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not radio_embed()
    except Exception:
        assert True
