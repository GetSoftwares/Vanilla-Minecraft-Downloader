__lazy__ = ["os", "sys"]
import os, sys
from launcher_provider import *

def import_folders_page(config_data):
    os.system("cls")
    print(r"""
从其他启动器导入文件夹

Vanilla Minecraft Downloader 可以从其他启动器导入文件夹。当前 VMD 下载器支持以下启动器：

    [1] HMCL
    [2] PCL2（含 PCL2-CE）（暂未实现）
    [3] 退出导入
""")
    launcher = input("你想要从哪个启动器导入 Minecraft 文件夹？请输入启动器前面的数字序号：")
    match launcher:
        case "1":
            launcher_path = os.path.normpath(os.path.expandvars(f"{input('请输入 HMCL 启动器所在的位置或其所在的文件夹：').replace('"', '')}"))
            if not launcher_path:
                print("你没有输入路径不存在！请重新输入。", file = sys.stderr)
                os.system("pause")
                return import_folders_page(config_data)
            elif os.path.isfile(launcher_path):
                launcher_path = os.path.dirname(launcher_path)
            elif os.path.isdir(launcher_path):
                pass
            else:
                print("你输入的路径不存在！请检查你的输入，然后再试一次。", file = sys.stderr)
                os.system("pause")
                return import_folders_page(config_data)
            print("开始导入……")
            config_data = import_folders_from_hmcl(config_data, launcher_path)
            return import_folders_page(config_data)
        case "2":
            print("从 PCL2（含 PCL2-CE）导入 Minecraft 文件夹尚未实现。")
            os.system("pause")
            return import_folders_page(config_data)
        case "3":
            return config_data
        case _:
            print("你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return import_folders_page(config_data)