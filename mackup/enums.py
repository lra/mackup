from enum import Enum


class SyncMode(Enum):
    HARDLINK = "hardlink"
    SOFTLINK = "softlink"


def parse_sync_mode(mode):
    if mode == "hardlink":
        return SyncMode.HARDLINK

    return SyncMode.SOFTLINK
