__lazy__ = ['json', 'os', 'os.path', 'uuid']

import json, os, os.path, uuid
from .constant import CONFIG_SAVE_PATH

def generate_default_config():
    """生成默认配置文件。"""
    save_config({
        "minecraft_folders": {},
        "default_folder_uuid": "",
        "check_hash": True,
        "auto_retry": True,
        "show_log": True,
        "debug": False
    })

def save_config(config_data):
    """保存配置文件。"""
    os.makedirs(os.path.dirname(CONFIG_SAVE_PATH), exist_ok = True)
    json.dump(config_data, open(CONFIG_SAVE_PATH, "w"), ensure_ascii = False, indent = 4)

def load_config():
    """加载配置文件。"""
    config_data = json.load(open(CONFIG_SAVE_PATH, encoding = "utf-8"))
    config_data.setdefault("check_hash", True)
    config_data.setdefault("auto_retry", True)
    config_data.setdefault("show_log", True)
    config_data.setdefault("debug", False)
    return config_data

def reset_default_setting(config_data):
    modified_config_data = config_data.copy()
    modified_config_data.update({"check_hash": True, "auto_retry": True, "show_log": True})
    save_config(modified_config_data)
    return modified_config_data

def add_minecraft_folder(config_data, /, minecraft_folder: str):
    """添加 Minecraft 文件夹。

    参数：

    config_data: 位置参数，下载器的配置。

    minecraft_folder: 要添加的文件夹。

    当添加前 Minecraft 文件夹列表为空时会同时将 minecraft_folder 设为默认文件夹。"""
    modified_config_data = config_data.copy()
    minecraft_folder = os.path.abspath(os.path.expandvars(minecraft_folder.replace('"', '')))
    if not os.path.exists(minecraft_folder):
        os.makedirs(minecraft_folder, exist_ok = True)
    new_folder_uuid = str(uuid.uuid4())
    if len(modified_config_data["minecraft_folders"]) == 0:
        modified_config_data["default_folder_uuid"] = new_folder_uuid
    modified_config_data["minecraft_folders"][new_folder_uuid] = {
        "path": minecraft_folder,
        "multi_version": os.path.exists(f"{minecraft_folder}{os.sep}versions"),
        "april_fool_control": "auto",
        "version_list_last_modified_time": ""
    }
    save_config(modified_config_data)
    return modified_config_data

def remove_minecraft_folder(config_data, /, folder_uuid: str):
    """删除 Minecraft 文件夹。

    参数：

    config_data: 位置参数，下载器的配置。

    folder_uuid: 要删除的文件夹 UUID。

    当 folder_uuid 与默认文件夹的 UUID 相等时，会自动设置默认文件夹。"""
    modified_config_data = config_data.copy()
    del modified_config_data["minecraft_folders"][folder_uuid]
    if folder_uuid == modified_config_data["default_folder_uuid"]:
        if len(modified_config_data["minecraft_folders"]):
            modified_config_data = change_default_minecraft_folder(modified_config_data)
        else:
            modified_config_data["default"] = ""
            save_config(modified_config_data)
    else:
        save_config(modified_config_data)
    return modified_config_data

def change_default_minecraft_folder(config_data, /, folder_uuid: str | None = None):
    """更改默认的 Minecraft 文件夹。

    参数：

    config_data: 位置参数，下载器的配置。

    folder_uuid: 要设为默认文件夹的文件夹 UUID。可为空。

    当 folder_uuid 为空时，自动设置第一个文件夹为默认文件夹。当 folder_uuid 不存在时会引发 LookupError 异常。"""
    modified_config_data = config_data.copy()
    if modified_config_data["default_folder_uuid"] == {}:
        raise ValueError("Minecraft 文件夹列表是空的！")
    if folder_uuid:
        if modified_config_data["minecraft_folders"].get(folder_uuid):
            modified_config_data["default_folder_uuid"] = folder_uuid
        else:
            raise LookupError(f"Minecraft 文件夹列表中没有 UUID 为 {folder_uuid} 的条目！")
    else:
        modified_config_data["default_folder_uuid"] = list(modified_config_data["minecraft_folders"].keys())[0] # 自动设置第一个文件夹为默认文件夹
    save_config(modified_config_data)
    return modified_config_data

def change_minecraft_folder_path(config_data, /, new_path: str, folder_uuid: str | None = None):
    """更改 Minecraft 文件夹的位置。"""
    modified_config_data = config_data.copy()
    if folder_uuid:
        modified_config_data["minecraft_folders"][folder_uuid]["path"] = new_path
    else:
        modified_config_data["minecraft_folders"][modified_config_data["default_folder_uuid"]]["path"] = new_path
    save_config(modified_config_data)
    return modified_config_data