__lazy__ = ["winreg", "sys", "os", "os.path", "configparser"]
import winreg, sys, os, os.path, configparser
from util import *

def import_folders_from_pcl2(config_data, launcher_path):
    """从 PCL2 导入 Minecraft 文件夹。"""
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
    if os.path.exists(f"{launcher_path}{os.sep}PCL"):
        try:
            pcl_setup = configparser.ConfigParser(allow_unnamed_section = True)
            pcl_setup.read(f"{launcher_path}{os.sep}PCL{os.sep}Setup.ini")
            default_folder = pcl_setup.get(configparser.UNNAMED_SECTION, "LaunchFolderSelect")
            if default_folder[-1] == '\\':
                default_folder = default_folder[:-1]
        except:
            default_folder = ""
            print("尝试获取 LaunchFolderSelect 的值失败，将跳过设置默认文件夹", file = sys.stderr)
        try:
            launch_folders = winreg.QueryValueEx(winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"SOFTWARE\PCL"), "LaunchFolders")[0]
        except OSError:
            print("查找 LaunchFolders 的值失败！", file = sys.stderr)
            os.system("pause")
            return config_data
        folder_list = []
        for folder in launch_folders.split('|'):
            folder_path = folder.split('>')
            if len(folder_path) == 2 and folder_path[1]:
                folder_list.append(folder_path[1])
        if len(folder_list) == 0:
            print("PCL2 没有任何合法的 Minecraft 文件夹！", file = sys.stderr)
            os.system("pause")
            return config_data
        if config_data["debug"]:
            print(f"{folder_list=}", file = sys.stderr)
        for folder in folder_list:
            if folder[-1] == '\\':
                folder_path = folder[:-1]
            else:
                folder_path = folder
            if check_folder_exists(config_data, folder_path):
                if show_log:
                    print(f"文件夹 {folder_path} 已存在，跳过")
                continue
            if show_log:
                print(f"正在导入文件夹 {folder_path}……")
            if folder_path.casefold() == default_folder.casefold():
                config_data = add_minecraft_folder(config_data, minecraft_folder = folder_path, _set_default = set_default)
                if set_default:
                    print(f"已将 {folder_path} 设为默认文件夹。")
            else:
                config_data = add_minecraft_folder(config_data, folder_path)
            success_imported_count += 1
    else:
        print(f"{launcher_path} 未发现 PCL2 启动器的配置文件！", file = sys.stderr)
        os.system("pause")
        return config_data
    if success_imported_count:
        print("从 PCL2 导入 Minecraft 文件夹成功！")
    else:
        print("没有从 PCL2 中导入任何文件夹！", file = sys.stderr)
    os.system("pause")
    return config_data