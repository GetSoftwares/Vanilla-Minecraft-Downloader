__lazy__ = ["os"]
import os
from util import *

def change_downloader_setting_page(config_data):
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
                    return change_downloader_setting_page(config_data)
                case False:
                    config_data["check_hash"] = True
                    save_config(config_data)
                    print("已成功将“检查文件哈希”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case _:
                    config_data["check_hash"] = True
                    save_config(config_data)
                    print("未知的设置，已将“检查文件哈希”重置为默认值：开", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
        case "2":
            match config_data["auto_retry"]:
                case True:
                    config_data["auto_retry"] = False
                    save_config(config_data)
                    print("已成功将“自动重试”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case False:
                    config_data["auto_retry"] = True
                    save_config(config_data)
                    print("已成功将“自动重试”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case _:
                    config_data["auto_retry"] = True
                    save_config(config_data)
                    print("未知的设置，已将“自动重试”重置为默认值：开", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
        case "3":
            match config_data["show_log"]:
                case True:
                    config_data["show_log"] = False
                    save_config(config_data)
                    print("已成功将“显示下载日志”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case False:
                    config_data["show_log"] = True
                    save_config(config_data)
                    print("已成功将“显示下载日志”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case _:
                    config_data["show_log"] = True
                    save_config(config_data)
                    print("未知的设置，已将“显示下载日志”重置为默认值：开", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
        case "4":
            match config_data["debug"]:
                case True:
                    config_data["debug"] = False
                    save_config(config_data)
                    print("已成功将“调试”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case False:
                    config_data["debug"] = True
                    save_config(config_data)
                    print("已成功将“调试”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case _:
                    config_data["debug"] = False
                    save_config(config_data)
                    print("未知的设置，已将“调试”重置为默认值：关", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
        case "5":
            answer = input("你确定要恢复默认设置吗？（y/yes/是=确认，其他=取消）：")
            if answer.casefold() in YES_LIST:
                config_data = reset_default_setting(config_data)
                print("恢复默认设置成功！")
                os.system("pause")
            return change_downloader_setting_page(config_data)
        case "6":
            return config_data
        case _:
            print("你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return change_downloader_setting_page(config_data)