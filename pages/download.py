__lazy__ = ["requests", "urllib3"]

import requests, urllib3

from module import *
from util import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_version_page(config_data):
    os.system("cls")
    if len(config_data["minecraft_folders"]) == 0:
        print("\n你还没有任何文件夹。请添加一个文件夹然后再进行下载。")
        os.system("pause")
        return
    elif config_data["minecraft_folders"].get(config_data["default_folder_uuid"]) is None:
        print("\n所使用的文件夹不存在！请重新设置一个默认文件夹，然后再进行下载。")
        os.system("pause")
        return
    default = config_data["default_folder_uuid"]
    if not os.path.exists(f"{config_data['minecraft_folders'][default]['path']}{os.sep}version_manifest.json"):
        try:
            response = requests.get(VERSION_LIST_DOWNLOAD_URL, verify = config_data["ssl_verify"])
        except:
            print("当前暂时无法下载版本列表，请稍后再试。", file = sys.stderr)
            os.system("pause")
            return config_data
        config_data["minecraft_folders"][default]["version_list_last_modified_time"] = response.headers.get("Last-Modified")
        save_config(config_data)
        version_list = response.json()
        dump_version_list(version_list, config_data["minecraft_folders"][default]["path"])
    else:
        try:
            response = requests.head(VERSION_LIST_DOWNLOAD_URL, verify = config_data["ssl_verify"])
        except:
            print("当前暂时无法获取版本列表的最后修改时间，请稍后再试。", file = sys.stderr)
            os.system("pause")
            return config_data
        if response.headers.get("Last-Modified") != config_data["minecraft_folders"][default]["version_list_last_modified_time"]:
            try:
                version_list = requests.get(VERSION_LIST_DOWNLOAD_URL, verify = config_data["ssl_verify"]).json()
            except:
                print("当前暂时无法下载版本列表，请稍后再试。", file = sys.stderr)
                os.system("pause")
                return config_data
            config_data["minecraft_folders"][default]["version_list_last_modified_time"] = response.headers.get("Last-Modified")
            save_config(config_data)
            dump_version_list(version_list, config_data["minecraft_folders"][default]["path"])
        else:
            version_list = load_version_list(config_data["minecraft_folders"][default]["path"])
    option = input(f"""
你想要下载哪个版本？

    [1] 最新正式版（当前最新正式版：{version_list['latest']['release']}）
    [2] 最新快照版（当前最新快照版：{version_list['latest']['snapshot']}）
    [3] 指定版本
    [4] 强制刷新版本列表
    [5] 退出下载

请输入：""")
    match option:
        case "1":
            download_special_version(
                get_client_manifest(version_list, version_list["latest"]["release"], config_data["ssl_verify"]),
                minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                check_hash = config_data["check_hash"],
                auto_retry = config_data["auto_retry"],
                show_log = config_data["show_log"],
                debug = config_data["debug"]
            )
            return download_version_page(config_data)
        case "2":
            match config_data["minecraft_folders"][default]["april_fool_control"]:
                case "auto":
                    if config_data["minecraft_folders"][default]["multi_version"]:
                        download_special_version(
                            get_client_manifest(version_list, version_list["latest"]["snapshot"], config_data["ssl_verify"]),
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
                    return download_version_page(config_data)
                case "on":
                    download_special_version(
                        get_client_manifest(version_list, version_list["latest"]["snapshot"], config_data["ssl_verify"]),
                        minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                        has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                        check_hash = config_data["check_hash"],
                        auto_retry = config_data["auto_retry"],
                        show_log = config_data["show_log"],
                        debug = config_data["debug"]
                    )
                    return download_version_page(config_data)
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
                    return download_version_page(config_data)
                case _:
                    config_data["minecraft_folders"][default]["april_fool_control"] = "auto"
                    print(f"“下载愚人节版本”的设置内容不正确。已重置为“自动”。", file = sys.stderr)
                    os.system("pause")
                    return download_version_page(config_data)
        case "3":
            version = input("请输入要下载的版本：")
            for i in version_list["versions"]:
                if i["id"].casefold() == version.casefold():
                    try:
                        client_manifest = requests.get(i["url"], verify = config_data["ssl_verify"]).json()
                    except:
                        print(f"当前暂时无法下载 {i['id']} 版本的客户端清单，请稍后再试。")
                        os.system("pause")
                        return config_data
                    download_special_version(
                        client_manifest,
                        minecraft_folder = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["path"],
                        has_multi_version = config_data["minecraft_folders"][config_data["default_folder_uuid"]]["multi_version"],
                        check_hash = config_data["check_hash"],
                        auto_retry = config_data["auto_retry"],
                        show_log = config_data["show_log"],
                        debug = config_data["debug"]
                    )
                    return download_version_page(config_data)
            else:
                print(f"你输入的版本 {version} 不存在！", file = sys.stderr)
                os.system("pause")
                return download_version_page(config_data)
        case "4":
            print("正在刷新版本列表……")
            try:
                response = requests.get(VERSION_LIST_DOWNLOAD_URL, verify = config_data["ssl_verify"])
            except:
                print(f"当前暂时无法刷新版本列表，请稍后再试。")
                os.system("pause")
                return config_data
            dump_version_list(response.json(), config_data["minecraft_folders"][default]["path"])
            config_data["minecraft_folders"][default]["version_list_last_modified_time"] = response.headers.get("Last-Modified")
            save_config(config_data)
            print("刷新版本列表成功！")
            os.system("pause")
            return download_version_page(config_data)
        case "5":
            return config_data
        case _:
            print(f"你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return download_version_page(config_data)