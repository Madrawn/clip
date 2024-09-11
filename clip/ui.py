""" This module contains the ui for the tagger tab. """

from typing import Dict, Tuple, List, Optional
import gradio as gr
import re
from PIL import Image
from packaging import version

try:
    from tensorflow import __version__ as tf_version
except ImportError:
    tf_version = "0.0.0"

from html import escape as html_esc

from modules import shared, sd_models, sd_clip  # pylint: disable=import-error
from modules import (
    infotext_utils as parameters_copypaste,
)  # pylint: disable=import-error # noqa

try:
    from modules.call_queue import wrap_gradio_gpu_call
except ImportError:
    from webui import wrap_gradio_gpu_call  # pylint: disable=import-error
from clip import utils  # pylint: disable=import-error
from clip.uiset import IOData, QData  # pylint: disable=import-error

TAG_INPUTS = ["add", "keep", "exclude", "search", "replace"]


def unload_interrogators() -> Tuple[str]:
    unloaded_models = 0
    remaining_models = ""

    for i in utils.interrogators.values():
        if i.unload():
            unloaded_models = unloaded_models + 1
        elif i.model is not None:
            if remaining_models == "":
                remaining_models = f", remaining models:<ul><li>{i.name}</li>"
            else:
                remaining_models = remaining_models + f"<li>{i.name}</li>"
    if remaining_models != "":
        remaining_models = (
            remaining_models + "Some tensorflow models could "
            "not be unloaded, a known issue."
        )
    QData.clear(1)

    return (f"{unloaded_models} model(s) unloaded{remaining_models}",)


def on_interrogate(input_text: str, add_text: str) -> str:
    return input_text + add_text


def on_ui_tabs():
    """configures the ui on the Clip tab"""
    # If checkboxes misbehave you have to adapt the default.json preset
    tag_input = {}

    with gr.Blocks(analytics_enabled=False) as clip_interface:
        with gr.Row():
            with gr.Column(variant="panel"):

                # input components
                go_button = gr.Button(label="Go", name="go_button")
                input_text = gr.Textbox(label="Prompt", lines=3, placeholder="Enter a prompt here", default="A photo of a cute puppy", name="input_text")
                add_text = gr.Textbox(label="Additional prompt", lines=3, placeholder="Enter a prompt here", default="A photo of a cute puppy", name="input_add_text")
                output = gr.Textbox(label="Output", lines=3, placeholder="Output will appear here", default="A photo of a cute puppy", name="output")
        # register events

        go_button.on_click(wrap_gradio_gpu_call(on_interrogate), inputs=[input_text, add_text], outputs=[output])
    return [(clip_interface, "Clip", "clip")]


def set_threshold_values(target):
    def func(input):
        list([QData.set(key)(input) for key in target])

    return func
