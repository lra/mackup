import os
from .mackup import Mackup

mckp = Mackup()

colors = mckp._config._cli_colors

colorize = True

if "CLICOLOR" in os.environ:
    if os.environ["CLICOLOR"] == "0":
        colorize = False

colorize = False if "NO_COLOR" in os.environ else colorize


def colorize_text(text):
    if colorize:
        return colors["text"] + text + colors["reset"]
    return text


def colorize_filename(text):
    if colorize:
        return (colors["filename"] + text + colors["reset"]).replace(
            "/", colors["filename_path_separator"] + "/" + colors["filename"]
        )
    return text


def colorize_name(text):
    if colorize:
        return colors["name"] + text + colors["reset"]
    return text


def colorize_item_bullet(text):
    if colorize:
        return colors["item_bullet"] + text + colors["reset"]
    return text


def colorize_header(text):
    if colorize:
        return colors["header"] + text + colors["reset"]
    return text


def colorize_header_app_name(text):
    if colorize:
        return colors["header_app_name"] + text + colors["reset"]
    return text
