__lazy__ = ['requests', 'json', 'os', 'os.path', 'sys', 'time']
import requests, os, os.path, sys, time
from config import *
from download import *

def download_version_main():
    global config_data
    os.system("cls")
    if len(config_data["minecraft_folders"]) == 0:
        print("\n你还没有任何文件夹。请添加一个文件夹然后再进行下载。")
        os.system("pause")
        return
    elif config_data["minecraft_folders"].get(config_data["default_folder_uuid"]) is None:
        print("\n所使用的文件夹不存在！请重新设置一个默认文件夹，然后再进行下载。")
        os.system("pause")
        return
    respong = requests.head(VERSION_LIST_DOWNLOAD_URL)
    default = config_data["default_folder_uuid"]
    if respong.headers.get("Last-Modified") != config_data["minecraft_folders"][default]["version_list_last_modified_time"]:
        version_list = requests.get(VERSION_LIST_DOWNLOAD_URL).json()
        config_data["minecraft_folders"][default]["version_list_last_modified_time"] = respong.headers.get("Last-Modified")
        save_config(config_data)
        dump_version_list(version_list, config_data["minecraft_folders"][default]["path"])
    else:
        version_list = load_version_list(config_data["minecraft_folders"][default]["path"])
    option = input(r"""
你想要下载哪个版本？

    [1] 最新正式版
    [2] 最新快照版
    [3] 指定版本
    [4] 退出下载

请输入：""")
    match option:
        case "1":
            download_special_version(
                get_client_manifest(version_list,version_list["latest"]["release"]),
                minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                check_hash = config_data["check_hash"],
                auto_retry = config_data["auto_retry"],
                show_log = config_data["show_log"],
                debug = config_data["debug"]
            )
            return download_version_main()
        case "2":
            match config_data["minecraft_folders"][default]["april_fool_control"]:
                case "auto":
                    if config_data["minecraft_folders"][default]["multi_version"]:
                        download_special_version(
                            get_client_manifest(version_list, version_list["latest"]["snapshot"]),
                            minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                            has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                            check_hash = config_data["check_hash"],
                            auto_retry = config_data["auto_retry"],
                            show_log = config_data["show_log"],
                            debug = config_data["debug"]
                        )
                    else:
                        download_latest_none_april_fool_version(
                            version_list,
                            minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                            has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                            check_hash = config_data["check_hash"],
                            auto_retry = config_data["auto_retry"],
                            show_log = config_data["show_log"],
                            debug = config_data["debug"]
                        )
                    return download_version_main()
                case "on":
                    download_special_version(
                        get_client_manifest(version_list, version_list["latest"]["snapshot"]),
                        minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                        has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                        check_hash = config_data["check_hash"],
                        auto_retry = config_data["auto_retry"],
                        show_log = config_data["show_log"],
                        debug = config_data["debug"]
                    )
                    return download_version_main()
                case "off":
                    download_latest_none_april_fool_version(
                        version_list,
                        minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                        has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                        check_hash = config_data["check_hash"],
                        auto_retry = config_data["auto_retry"],
                        show_log = config_data["show_log"],
                        debug = config_data["debug"]
                    )
                    return download_version_main()
                case _:
                    config_data["minecraft_folders"][default]["april_fool_control"] = "auto"
                    print(f"“下载愚人节版本”的设置内容不正确。已重置为“自动”。", file = sys.stderr)
                    os.system("pause")
                    return download_version_main()
        case "3":
            version = input("请输入要下载的版本：")
            for i in version_list["versions"]:
                if i["id"].casefold() == version.casefold():
                    download_special_version(
                        requests.get(i["url"]).json(),
                        minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                        has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                        check_hash = config_data["check_hash"],
                        auto_retry = config_data["auto_retry"],
                        show_log = config_data["show_log"],
                        debug = config_data["debug"]
                    )
                    return download_version_main()
            else:
                print(f"你输入的版本 {version} 不存在！", file = sys.stderr)
                os.system("pause")
                return download_version_main()
        case "4":
            return
        case _:
            print(f"你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return download_version_main()

def change_folder_setting_main():
    global config_data
    os.system("cls")
    if len(config_data["minecraft_folders"]) == 0:
        print("\n这里没有可以设置的文件夹。请添加一个文件夹然后再进行设置。", file = sys.stderr)
        os.system("pause")
        return
    elif config_data["minecraft_folders"].get(config_data["default_folder_uuid"]) == None:
        print("\n所使用的文件夹不存在！请重新设置一个默认文件夹，然后再进行设置。")
        os.system("pause")
        return
    print(f"""
更改 {config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"]} 的设置

    1. [{'开' if config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"] else '关'}] 多版本隔离""")
    match config_data["minecraft_folders"][config_data["default_folder_uuid"]]["april_fool_control"]:
        case "auto":
            print("    2. [自动] 下载愚人节版本")
        case "on":
            print("    2. [开] 下载愚人节版本")
        case "off":
            print("    2. [关] 下载愚人节版本")
    print(r"""    3. 退出更改

设置说明：
多版本隔离：是否为每个版本单独设立一个文件夹。
- 开：开启多版本隔离，每个版本将被放置到 versions\<版本名> 的文件夹下
- 关：关闭多版本隔离，版本被直接放在 Minecraft 文件夹根目录下
- 会根据文件夹中是否有 versions 文件夹来自动设定默认值。
下载愚人节版本：是否下载愚人节版本。仅用于“下载最新快照”。
- 自动：根据版本隔离情况自动选择，开启版本隔离则下载愚人节版本，关闭则不下载（默认）
- 开：无论如何都下载愚人节版本
- 关：无论如何都不下载愚人节版本。这种情况下将下载最新的非愚人节快照（按时间排序）。
""")
    setting = input("请输入要修改的设置项：")
    match setting:
        case "1":
            match config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"]:
                case True:
                    config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"] = False
                    save_config(config_data)
                    print("已将多版本隔离设置为：关！")
                case False:
                    config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"] = True
                    save_config(config_data)
                    print("已将多版本隔离设置为：开！")
                case _:
                    config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"] = os.path.exists(f"{config_data['minecraft_folders'][config_data['default_folder_uuid']]}{os.sep}versions")
                    save_config(config_data)
                    print(f"未知的设置，已将“多版本隔离”重置为默认值：{'开' if config_data['minecraft_folders'][config_data['default_folder_uuid']]['multi_version'] else '关'}！")
            os.system("pause")
            return change_folder_setting_main()
        case "2":
            setting_value = input("你想要将“下载愚人节版本”更新为什么设置：（auto=自动，on=开，off=关）")
            match setting_value:
                case "auto" | "on" | "off":
                    config_data["minecraft_folders"][config_data["default_folder_uuid"]]["april_fool_control"] = setting_value
                    print(f"已成功将“下载愚人节版本”设为：{setting_value}")
                    os.system("pause")
                    return change_folder_setting_main()
                case _:
                    print(f"未知的设置：{setting_value}", file = sys.stderr)
                    os.system("pause")
                    return change_folder_setting_main()
        case "3":
            return
        case _:
            print(f"你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return change_folder_setting_main()

def change_downloader_setting_main():
    global config_data
    os.system("cls")
    print(f"""
更改 {PROJECT_NAME} 设置

    1. [{'开' if config_data['check_hash'] else '关'}] 检查文件哈希
    2. [{'开' if config_data['auto_retry'] else '关'}] 自动重试
    3. [{'开' if config_data['show_log'] else '关'}] 显示下载日志
    4. [{'开' if config_data['debug'] else '关'}] 调试
    5. 恢复默认设置
    6. 退出

设置说明：
检查文件哈希：检查下载的文件的 SHA-1 哈希是否匹配。
- 开：将检查下载的文件的 SHA-1 值是否与官方给出的 SHA-1 值匹配。这有助于确保下载到正确的文件。（默认值）
- 关：将不检查下载的文件的 SHA-1 值是否与官方给出的 SHA-1 值匹配。
自动重试：下载失败时自动重新下载文件，最多重新尝试五次（含第一次下载）。
- 开：失败时自动重新下载。（默认值）
- 关：失败时立即停止下载。
显示下载日志：在下载版本是是否显示下载日志。
- 开：将显示下载日志，有助于排查问题。（默认值）
- 关：将不显示下载日志。
调试：输出下载器的调试信息。
- 开：输出调试信息，有助于排查问题
- 关：不输出调试信息（默认）
""")
    setting = input("请输入要修改的设置项：")
    match setting:
        case "1":
            match config_data["check_hash"]:
                case True:
                    config_data["check_hash"] = False
                    save_config(config_data)
                    print("已成功将“检查文件哈希”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_main()
                case False:
                    config_data["check_hash"] = True
                    save_config(config_data)
                    print("已成功将“检查文件哈希”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_main()
                case _:
                    config_data["check_hash"] = True
                    save_config(config_data)
                    print("未知的设置，已将“检查文件哈希”重置为默认值：开", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_main()
        case "2":
            match config_data["auto_retry"]:
                case True:
                    config_data["auto_retry"] = False
                    save_config(config_data)
                    print("已成功将“自动重试”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_main()
                case False:
                    config_data["auto_retry"] = True
                    save_config(config_data)
                    print("已成功将“自动重试”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_main()
                case _:
                    config_data["auto_retry"] = True
                    save_config(config_data)
                    print("未知的设置，已将“自动重试”重置为默认值：开", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_main()
        case "3":
            match config_data["show_log"]:
                case True:
                    config_data["show_log"] = False
                    save_config(config_data)
                    print("已成功将“显示下载日志”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_main()
                case False:
                    config_data["show_log"] = True
                    save_config(config_data)
                    print("已成功将“显示下载日志”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_main()
                case _:
                    config_data["show_log"] = True
                    save_config(config_data)
                    print("未知的设置，已将“显示下载日志”重置为默认值：开", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_main()
        case "4":
            match config_data["debug"]:
                case True:
                    config_data["debug"] = False
                    save_config(config_data)
                    print("已成功将“调试”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_main()
                case False:
                    config_data["debug"] = True
                    save_config(config_data)
                    print("已成功将“调试”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_main()
                case _:
                    config_data["debug"] = False
                    save_config(config_data)
                    print("未知的设置，已将“调试”重置为默认值：关", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_main()
        case "5":
            answer = input("你确定要恢复默认设置吗？（y/yes/是=确认，其他=取消）：")
            if answer.casefold() in YES_LIST:
                config_data = reset_default_setting(config_data)
                print("恢复默认设置成功！")
                os.system("pause")
            return change_downloader_setting_main()
        case "6":
            return
        case _:
            print("你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return change_downloader_setting_main()

def minecraft_folder_management_main():
    global config_data
    os.system("cls")
    print(r"""
Minecraft 文件夹管理

以下是你当前可用的 Minecraft 文件夹：
""")
    if len(config_data["minecraft_folders"]) == 0:
        print("\n这里没有任何文件夹。请先添加一个文件夹。", file = sys.stderr)
        os.system("pause")
        return
    folder_index = 0
    for entry in config_data["minecraft_folders"]:
        folder_index += 1
        print(f"    [{folder_index}] {config_data['minecraft_folders'][entry]['path']}{'（默认）' if entry == config_data['default_folder_uuid'] else ''}")
    print()
    folder_index = input("你想要操作哪个文件夹：")
    try:
        folder_index = int(folder_index)
    except ValueError:
        print("你输入了非数字序号，请重新输入。", file = sys.stderr)
        os.system("pause")
        return minecraft_folder_management_main()
    if folder_index < 1 or folder_index > len(config_data["minecraft_folders"]):
        print("你指定了不在列表中的序号，请重新输入。", file = sys.stderr)
        os.system("pause")
        return minecraft_folder_management_main()
    folder_uuid = list(config_data["minecraft_folders"].keys())[folder_index - 1]
    print(r"""
你想要执行什么操作？

    [1] 更改文件夹的路径
    [2] 设为默认文件夹
    [3] 删除文件夹
    [4] 退出操作
""")
    option = input("请选择：")
    match option:
        case "1":
            new_path = input(f"请输入你想要更改的路径：")
            if not new_path:
                print("你没有输入任何路径。请重新输入。")
                os.system("pause")
                return minecraft_folder_management_main()
            else:
                config_data = change_minecraft_folder_path(config_data, folder_uuid = folder_uuid, new_path = new_path)
                print("更改文件夹路径成功！")
                os.system("pause")
                return minecraft_folder_management_main()
        case "2":
            config_data = change_default_minecraft_folder(config_data, folder_uuid)
            print(f"已成功更改默认文件夹为 {config_data['minecraft_folders'][folder_uuid]['path']}。")
            os.system("pause")
            return minecraft_folder_management_main()
        case "3":
            answer = input(f"你确定要删除 {config_data['minecraft_folders'][folder_uuid]['path']} 吗？（y/yes/是=删除，其他=保留）：")
            if answer.casefold() in YES_LIST:
                config_data = remove_minecraft_folder(config_data, folder_uuid)
                print("删除成功！")
                os.system("pause")
            return minecraft_folder_management_main()
        case "4":
            return
        case _:
            print(f"你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return minecraft_folder_management_main()

def about_main():
    print(f"""
{PROJECT_NAME}
版本：{PROJECT_VERSION}
作者：GetSoftwares

一个纯粹的原版 Minecraft Java 版下载器。
你知道吗？下载器的程序只花了三天时间就写完了。
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
    [3] 添加 Minecraft 文件夹
    [4] 更改文件夹设置
    [5] 下载器设置
    [6] 关于
    [7] 退出
""")
    option = input("请输入选项：")
    match option:
        case "1":
            download_version_main()
            return title_main()
        case "2":
            minecraft_folder_management_main()
            return title_main()
        case "3":
            new_folder = input("你想要添加哪个文件夹：")
            if not os.path.isdir(new_folder):
                print(f"{new_folder} 不是一个文件夹或不存在。请检查你的输入，然后再试一次。", file = sys.stderr)
            else:
                config_data = add_minecraft_folder(config_data, new_folder)
                print("已成功添加文件夹。")
            os.system("pause")
            return title_main()
        case "4":
            change_folder_setting_main()
            return title_main()
        case "5":
            change_downloader_setting_main()
            return title_main()
        case "6":
            about_main()
            return title_main()
        case "7":
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
    if config_data["minecraft_folders"] == {}:
        answer = input(r"当前没有任何 Minecraft 文件夹。你需要使用默认的 Minecraft 文件夹（%APPDATA%\.minecraft）吗？（Y/Yes/是=使用，其他=不使用）：")
        if answer.casefold() in YES_LIST:
            config_data = add_minecraft_folder(config_data, minecraft_folder = os.path.expandvars(r"%APPDATA%\.minecraft"))
    if config_data["minecraft_folders"].get(config_data["default_folder_uuid"]) == None:
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
