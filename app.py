"""Create entry."""
# pylint: disbale=invalid-name
import os
import time
from pathlib import Path

import gradio as gr
import logzero
import pandas as pd
from about_time import about_time
from icecream import install as ic_install, ic
from logzero import logger
from set_loglevel import set_loglevel

from radio_embed import __version__, radio_embed

os.environ["LOGLEVEL"] = "10"  # turn debug on
os.environ["LOGLEVEL"] = "20"  # turn debug off
logzero.loglevel(set_loglevel())
if set_loglevel() <= 10:
    logger.info(" debug is on ")
else:
    logger.info(" debug is off ")

ic_install()
ic.configureOutput(
    includeContext=True,
    outputFunction=logger.info,
)
# ic.enable()
ic.disable()  # to turn off

os.environ["TZ"] = "Asia/Shanghai"
try:
    time.tzset()  # type: ignore
except Exception as _:
    logger.warning("time.tzset() error: %s. Probably running Windows, we let it pass.", _)


iface = gr.Interface(
    fn=radio_embed,
    inputs="textarea",
    outputs="dataframe",
    title=f"radio-embed {__version__}",
    description="embed rest api via gradio",
    examples=[
        ["test\n测试"]
    ],
    allow_flagging="never",
)

debug = False
if set_loglevel() <= 10:
    debug = True

iface.launch(
    show_error=debug,
    enable_queue=True,
    debug=debug,
)
