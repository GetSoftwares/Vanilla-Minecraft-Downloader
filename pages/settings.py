__lazy__ = ["os"]
import os
from util import *

def change_downloader_setting_page(config_data):
    os.system("cls")
    print(f"""
更改 {PROJECT_NAME} 设置

    下载器
        1. [{'开' if config_data['check_hash'] else '关'}] 检查文件哈希
        2. [{'开' if config_data['auto_retry'] else '关'}] 自动重试
        3. [{'开' if config_data['show_log'] else '关'}] 显示下载日志""")
    match config_data["write_isolation_config"]:
        case "auto":
            print("        4. [自动] 写入版本隔离设置")
        case "on":
            print("        4. [开] 写入版本隔离设置")
        case "off":
            print("        4. [关] 写入版本隔离设置")
    print(f"""    导入文件夹
        5. [{'开' if config_data['show_log'] else '关'}] 导入启动器预设文件夹""")
    match config_data["set_default_folder_when_import"]:
        case "auto":
            print("        6. [自动] 导入时设置默认文件夹")
        case "on":
            print("        6. [开] 导入时设置默认文件夹")
        case "off":
            print("        6. [关] 导入时设置默认文件夹")
    print(f"""    调试性设置
        7. [{'开' if config_data['debug'] else '关'}] 调试
        8. [{'开' if config_data['ssl_verify'] else '关'}] SSL 验证
    其他
        9. 恢复默认设置
        10. 退出

设置说明：
检查文件哈希：检查下载的文件的 SHA-1 哈希是否匹配。
- 开：将检查下载的文件的 SHA-1 值是否与官方给出的 SHA-1 值匹配。这有助于确保下载到正确的文件。（默认值）
- 关：将不检查下载的文件的 SHA-1 值是否与官方给出的 SHA-1 值匹配。
自动重试：下载失败时自动重新下载文件，最多重新尝试五次（含第一次下载）。
- 开：失败时自动重新下载。（默认）
- 关：失败时立即停止下载。
显示下载日志：在下载版本是是否显示下载日志。
- 开：将显示下载日志，有助于排查问题。（默认）
- 关：将不显示下载日志。
写入版本隔离设置：下载完后写入多版本隔离设置。
- 自动：对于多版本隔离则自动写入版本隔离设置，对于单实例则不写入。（默认）
- 开：始终写入版本隔离设置。
- 关：始终不写入版本隔离设置。
导入启动器预设文件夹：导入不在配置文件或文件夹列表文件中的、预设的文件夹（启动器所在目录的 .minecraft 文件夹和 %APPDATA%\\.minecraft）。仅适用于 PCL2。
- 开：导入预设文件夹。（默认）
- 关：不导入预设文件夹。
导入时设置默认文件夹：从其他启动器导入文件夹时，将启动器的默认文件夹设置为下载器的默认文件夹。
- 自动：当设置了下载器的默认文件夹时不设置，否则设为启动器的默认文件夹。（默认）
- 开：始终将默认文件夹设置为启动器的默认文件夹。
- 关：永远不会将启动器的默认文件夹设置为下载器的默认文件夹。
调试：输出下载器的调试信息。
- 开：输出调试信息，有助于排查问题。
- 关：不输出调试信息。（默认）
SSL 验证：（调试性选项）在下载 Minecraft 时是否验证 SSL 证书。
- 开：验证 SSL 证书。（默认）
- 关：不验证 SSL 证书。可在验证 SSL 证书遇到问题时使用。
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
            setting_value = input("你想要将“写入版本隔离设置”更新为什么设置：（auto=自动，on=开，off=关）")
            match setting_value:
                case "auto" | "on" | "off":
                    config_data["write_isolation_config"] = setting_value
                    print(f"已成功将“写入版本隔离设置”设为：{setting_value}")
                case _:
                    print(f"未知的设置：{setting_value}", file = sys.stderr)
            os.system("pause")
            return change_downloader_setting_page(config_data)
        case "5":
            match config_data["import_preset_folder"]:
                case True:
                    config_data["import_preset_folder"] = False
                    save_config(config_data)
                    print("已成功将“导入启动器预设文件夹”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case False:
                    config_data["import_preset_folder"] = True
                    save_config(config_data)
                    print("已成功将“导入启动器预设文件夹”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case _:
                    config_data["import_preset_folder"] = True
                    save_config(config_data)
                    print("未知的设置，已将“导入启动器预设文件夹”重置为默认值：开", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
        case "6":
            setting_value = input("你想要将“导入时设置默认文件夹”更新为什么设置：（auto=自动，on=开，off=关）")
            match setting_value:
                case "auto" | "on" | "off":
                    config_data["set_default_folder_when_import"] = setting_value
                    print(f"已成功将“导入时设置默认文件夹”设为：{setting_value}")
                case _:
                    print(f"未知的设置：{setting_value}", file = sys.stderr)
            os.system("pause")
            return change_downloader_setting_page(config_data)
        case "7":
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
        case "8":
            match config_data["ssl_verify"]:
                case True:
                    config_data["ssl_verify"] = False
                    save_config(config_data)
                    print("已成功将“SSL 验证”设置为：关")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case False:
                    config_data["ssl_verify"] = True
                    save_config(config_data)
                    print("已成功将“SSL 验证”设置为：开")
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
                case _:
                    config_data["ssl_verify"] = False
                    save_config(config_data)
                    print("未知的设置，已将“SSL 验证”重置为默认值：关", file = sys.stderr)
                    os.system("pause")
                    return change_downloader_setting_page(config_data)
        case "9":
            answer = input("你确定要恢复默认设置吗？（y/yes/是=确认，其他=取消）：")
            if answer.casefold() in YES_LIST:
                config_data = reset_default_setting(config_data)
                print("恢复默认设置成功！")
                os.system("pause")
            return change_downloader_setting_page(config_data)
        case "10":
            return config_data
        case _:
            print("你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return change_downloader_setting_page(config_data)