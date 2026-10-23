__lazy__ = ["platform"]

import platform

def is_target_platform(target_platform):
    current_platform = platform.system()
    match current_platform:
        case "Windows":
            return target_platform == "windows"
        case "Darwin":
            return target_platform == "osx"
        case "Linux":
            return target_platform == "linux"
        case _:
            return False

def get_machine():
    return platform.machine()

def get_platform():
    current_platform = platform.system()
    match current_platform:
        case "Windows":
            return "windows"
        case "Darwin":
            return "osx"
        case "Linux":
            return "linux"
        case _:
            raise ValueError(f"不支持的平台：{current_platform}")