"""Embed input."""
import numpy
from hf_model_s_cpu import model_s
from logzero import logger

try:
    model = model_s()
except Exception as _:
    logger.exception(_)
    raise SystemExit(1) from _


def radio_embed(
    text: str,
) -> numpy.ndarray:
    """Embed input."""
    try:
        _ = model.encode(text.strip().splitlines())
    except Exception as _:
        logger.exception(_)
        raise

    return _
