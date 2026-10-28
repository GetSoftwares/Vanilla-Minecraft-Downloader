__lazy__ = ['json', 'os', 'os.path', 'sys', 'time']
import os, os.path, sys, time
from util import *
from module import *
from pages import *

def about_main():
    print(f"""
{PROJECT_NAME}
版本：{PROJECT_VERSION}
作者：GetSoftwares

一个纯粹的原版 Minecraft Java 版下载器。
你知道吗？下载器的第一个版本只花了三天时间就写完了。
""")
    os.system("pause")
    return

def title_main():
    global config_data
    os.system("cls")
    print(f"""
欢迎来到 {PROJECT_NAME}！以下是你可以选定的操作：

    [1] 下载一个版本
    [2] Minecraft 文件夹管理
    [3] 下载器设置
    [4] 从其他启动器导入 Minecraft 文件夹
    [5] 关于
    [6] 退出
""")
    option = input("请输入选项：")
    match option:
        case "1":
            config_data = download_version_page(config_data)
            return title_main()
        case "2":
            config_data = minecraft_folder_management_page(config_data)
            return title_main()
        case "3":
            config_data = change_downloader_setting_page(config_data)
            return title_main()
        case "4":
            config_data = import_folders_page(config_data)
            return title_main()
        case "5":
            about_main()
            return title_main()
        case "6":
            print("保存配置……")
            save_config(config_data)
            print("退出！")
            return 0
        case _:
            print("你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return title_main()

def main():
    global config_data
    if not os.path.exists(os.path.expandvars(CONFIG_SAVE_PATH)):
        generate_default_config()
    config_data = load_config()
    if not config_data.get("minecraft_folders"):
        answer = input(r"当前没有任何 Minecraft 文件夹。你需要使用默认的 Minecraft 文件夹（%APPDATA%\.minecraft）吗？（Y/Yes/是=使用，其他=不使用）：")
        if answer.casefold() in YES_LIST:
            config_data = add_minecraft_folder(config_data, minecraft_folder = os.path.expandvars(r"%APPDATA%\.minecraft"))
    elif config_data["minecraft_folders"].get(config_data["default_folder_uuid"]) == None:
        answer = input(r"当前使用的文件夹条目不存在。是否要设置新的默认文件夹？（默认选中第一个条目，如果没有任何条目则添加默认 Minecraft 文件夹（%APPDATA%\.minecraft）：")
        if answer.casefold() in YES_LIST:
            if len(config_data["minecraft_folders"]):
                config_data = change_default_minecraft_folder(config_data)
            else:
                config_data = add_minecraft_folder(config_data, minecraft_folder = os.path.expandvars(r"%APPDATA%\.minecraft"))
    # 添加 aria2c 到 PATH，以便于将本程序打包后还能找到正确的 aria2c
    match get_machine():
        case "AMD64":
            os.environ["PATH"] = f"{os.path.join(os.path.dirname(sys.argv[0]), f'aria2{os.sep}x64')}{os.pathsep}{os.environ['PATH']}"
        case "X86":
            os.environ["PATH"] = f"{os.path.join(os.path.dirname(sys.argv[0]), f'aria2{os.sep}x86')}{os.pathsep}{os.environ['PATH']}"
        case "ARM":
            os.environ["PATH"] = f"{os.path.join(os.path.dirname(sys.argv[0]), f'aria2{os.sep}x86')}{os.pathsep}{os.environ['PATH']}"
        case "ARM64":
            if platform.version().split('.')[2] < 22000:
                os.environ["PATH"] = f"{os.path.join(os.path.dirname(sys.argv[0]), f'aria2{os.sep}x86')}{os.pathsep}{os.environ['PATH']}"
            else:
                os.environ["PATH"] = f"{os.path.join(os.path.dirname(sys.argv[0]), f'aria2{os.sep}x64')}{os.pathsep}{os.environ['PATH']}"
        case _:
            print(f"未知的架构，{PROJECT_NAME} 将退出……", file = sys.stderr)
    if config_data["debug"]:
        print(f"当前环境变量 PATH 的值：{os.environ['PATH']}", file = sys.stderr)
        print(f"当前配置：{config_data}", file = sys.stderr)
        time.sleep(5)
    return title_main()

if __name__ == '__main__':
    sys.exit(main())
