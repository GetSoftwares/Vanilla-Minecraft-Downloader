__lazy__ = ["os", "os.path", "json"]
import os, os.path, json
from util import *

def import_folders_from_hmcl(config_data, launcher_path, /):
    """从 HMCL 启动器导入 Minecraft 文件夹。

    参数：

    config_data: 配置数据

    launcher_path: 启动器路径"""
    success_imported_count = 0
    show_log = config_data["show_log"]
    match config_data["set_default_folder_when_import"]:
        case "auto":
            if not config_data["default_folder_uuid"] or config_data["minecraft_folders"].get(config_data["default_folder_uuid"]) is None:
                set_default = True
            else:
                set_default = False
        case "on":
            set_default = True
        case "off":
            set_default = False
        case _:
            raise ValueError(f"“导入时设置默认文件夹”的值非法：{config_data['set_default_folder_when_import']}！")
    if os.path.exists(f"{launcher_path}{os.sep}.hmcl"):
        folder_list = json.load(open(f"{launcher_path}{os.sep}.hmcl{os.sep}config{os.sep}game-directories.json", encoding = "utf-8"))
        launcher_config = json.load(open(f"{launcher_path}{os.sep}.hmcl{os.sep}config{os.sep}launcher-settings.json", encoding = "utf-8"))
        default_folder = launcher_config["selectedGameDirectory"]
        for folder in folder_list["directories"]:
            if os.path.isabs(folder["path"]):
                folder_path = folder["path"]
            else:
                folder_path = f"{launcher_path}{os.sep}{folder['path']}"
            if check_folder_exists(config_data, folder_path):
                if show_log:
                    print(f"文件夹 {folder_path} 已存在，跳过")
                continue
            folder_uuid = folder["id"].split(':')[1]
            if show_log:
                print(f"正在导入文件夹 {folder_path}……")
            if folder["id"] == default_folder:
                config_data = add_minecraft_folder(config_data, folder_path, folder_uuid, set_default)
            else:
                config_data = add_minecraft_folder(config_data, folder_path, folder_uuid)
            success_imported_count += 1
    elif os.path.exists(f"{launcher_path}{os.sep}config.json"):
        launcher_config = json.load(open(f"{launcher_path}{os.sep}config.json", encoding = "utf-8"))
        default_folder = launcher_config["last"]
        for folder in launcher_config["configurations"]:
            if launcher_config["configurations"][folder]["useRelativePath"]:
                folder_path = os.path.normpath(f"{launcher_path}{os.sep}{launcher_config['configurations'][folder]['gameDir']}")
            else:
                folder_path = launcher_config["configurations"][folder]["gameDir"]
            if check_folder_exists(config_data, folder_path):
                if show_log:
                    print(f"文件夹 {folder_path} 已存在，跳过")
                continue
            if show_log:
                print(f"正在导入文件夹 {folder_path}……")
            if folder_path == default_folder:
                config_data = add_minecraft_folder(config_data, minecraft_folder = folder_path, _set_default = set_default)
            else:
                config_data = add_minecraft_folder(config_data, folder_path)
            success_imported_count += 1
    else:
        print(f"{launcher_path} 未发现 HMCL 启动器的配置文件！", file = sys.stderr)
        os.system("pause")
        return config_data
    if success_imported_count:
        print("从 HMCL 导入 Minecraft 文件夹成功！")
    else:
        print("没有从 HMCL 中导入任何文件夹！", file = sys.stderr)
    os.system("pause")
    return config_data