"""clip module entry point."""

from modules import script_callbacks  # pylint: disable=import-error
from clip.ui import on_ui_tabs  # pylint: disable=import-error
from clip.settings import on_ui_settings  # pylint: disable=import-error



script_callbacks.on_ui_tabs(on_ui_tabs)
script_callbacks.on_ui_settings(on_ui_settings)
