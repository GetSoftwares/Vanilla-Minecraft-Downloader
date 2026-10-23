__lazy__ = ['os.path']

import os.path

CONFIG_SAVE_PATH = os.path.expandvars(r"%APPDATA%\Vanilla Minecraft Downloader\config.json")

YES_LIST = ['y'.casefold(), 'yes'.casefold(), '是'.casefold()]

MAX_RETRY = 5

VERSION_LIST_DOWNLOAD_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
RESOURCES_DOWNLOAD_URL = "https://resources.download.minecraft.net"

PROJECT_NAME = "Vanilla Minecraft Downloader"
PROJECT_VERSION = "1.0.0"