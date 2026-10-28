__lazy__ = ["os", "sys"]
import os, sys
from util import *

def change_folder_setting_page(config_data):
    os.system("cls")
    if len(config_data["minecraft_folders"]) == 0:
        print("\n这里没有可以设置的文件夹。请添加一个文件夹然后再进行设置。", file = sys.stderr)
        os.system("pause")
        return config_data
    elif config_data["minecraft_folders"].get(config_data["default_folder_uuid"]) == None:
        print("\n所使用的文件夹不存在！请重新设置一个默认文件夹，然后再进行设置。")
        os.system("pause")
        return config_data
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
            return change_folder_setting_page(config_data)
        case "2":
            setting_value = input("你想要将“下载愚人节版本”更新为什么设置：（auto=自动，on=开，off=关）")
            match setting_value:
                case "auto" | "on" | "off":
                    config_data["minecraft_folders"][config_data["default_folder_uuid"]]["april_fool_control"] = setting_value
                    print(f"已成功将“下载愚人节版本”设为：{setting_value}")
                    os.system("pause")
                    return change_folder_setting_page(config_data)
                case _:
                    print(f"未知的设置：{setting_value}", file = sys.stderr)
                    os.system("pause")
                    return change_folder_setting_page(config_data)
        case "3":
            return config_data
        case _:
            print(f"你没有输入对应的选项。请再试一次。", file = sys.stderr)
            os.system("pause")
            return change_folder_setting_page(config_data)

def minecraft_folder_management_page(config_data):
    os.system("cls")
    print(r"""
Minecraft 文件夹管理

以下是你当前可用的 Minecraft 文件夹：
""")
    if len(config_data["minecraft_folders"]) == 0:
        print("\n这里没有可用的文件夹。你需要先添加一个文件夹才能进行管理。", file = sys.stderr)
    else:
        folder_index = 0
        for entry in config_data["minecraft_folders"]:
            folder_index += 1
            print(f"    [{folder_index}] {config_data['minecraft_folders'][entry]['path']}{'（默认）' if entry == config_data['default_folder_uuid'] else ''}")
    print(r"""
除此以外，你还可以执行以下操作：

    [A] 添加一个文件夹
    [B] 设置默认文件夹
    [C] 更改当前文件夹的设置
    [D] 更改当前文件夹的路径
    [E] 删除一个文件夹
    [F] 退出
""")
    index_or_operation = input("你想要操作哪个文件夹或执行什么操作：")
    if not index_or_operation:
        print("你没有输入任何序号，请重新输入。", file = sys.stderr)
        os.system("pause")
        return minecraft_folder_management_page(config_data)
    if index_or_operation.isnumeric():
        folder_index = int(index_or_operation)
        if folder_index < 1 or folder_index > len(config_data["minecraft_folders"]):
            print("你指定了不在列表中的序号，请重新输入。", file = sys.stderr)
            os.system("pause")
            return minecraft_folder_management_page(config_data)
        folder_uuid = list(config_data["minecraft_folders"].keys())[folder_index - 1]
        print(r"""
你想要执行什么操作？

    [1] 更改当前文件夹的设置
    [2] 更改文件夹的路径
    [3] 设为默认文件夹
    [4] 删除文件夹
    [5] 退出操作
""")
        option = input("请选择：")
        match option:
            case "1":
                config_data = change_folder_setting_page(config_data)
                return minecraft_folder_management_page(config_data)
            case "2":
                new_path = input(f"请输入你想要更改的路径：")
                if not new_path:
                    print("你没有输入任何路径。请重新输入。")
                    os.system("pause")
                    return minecraft_folder_management_page(config_data)
                new_path = os.path.abspath(os.path.expandvars(new_path.replace('"', '')))
                if not os.path.isdir(new_path):
                    print(f"{new_path} 不是一个文件夹或不存在。请检查你的输入，然后再试一次。", file = sys.stderr)
                elif check_folder_exists(config_data, new_path):
                    print(f"{new_path} 已经存在！", file = sys.stderr)
                else:
                    config_data = change_minecraft_folder_path(config_data, folder_uuid = folder_uuid, new_path = new_path)
                    print("更改文件夹路径成功！")
                os.system("pause")
                return minecraft_folder_management_page(config_data)
            case "3":
                config_data = change_default_minecraft_folder(config_data, folder_uuid)
                print(f"已成功更改默认文件夹为 {config_data['minecraft_folders'][folder_uuid]['path']}。")
                os.system("pause")
                return minecraft_folder_management_page(config_data)
            case "4":
                answer = input(f"你确定要删除 {config_data['minecraft_folders'][folder_uuid]['path']} 吗？（y/yes/是=删除，其他=保留）：")
                if answer in YES_LIST:
                    config_data = remove_minecraft_folder(config_data, folder_uuid)
                    print("删除成功！")
                else:
                    print("你已取消删除。")
                os.system("pause")
                return minecraft_folder_management_page(config_data)
            case "5":
                return config_data
            case _:
                print(f"你没有输入对应的选项。请再试一次。", file = sys.stderr)
                os.system("pause")
                return minecraft_folder_management_page(config_data)
    elif index_or_operation.isalpha():
        operation = index_or_operation
        match operation:
            case "A" | "a":
                new_path = input("请输入你想要添加的 Minecraft 文件夹的路径：")
                if not new_path:
                    print("你没有输入要添加的文件夹的路径。请重新输入。", file = sys.stderr)
                    os.system("pause")
                    return minecraft_folder_management_page(config_data)
                new_path = os.path.abspath(os.path.expandvars(new_path.replace('"', '')))
                if not os.path.isdir(new_path):
                    print(f"{new_path} 不是一个文件夹或不存在。请检查你的输入，然后再试一次。", file = sys.stderr)
                elif check_folder_exists(config_data, new_path):
                    print(f"{new_path} 已经存在！", file = sys.stderr)
                else:
                    config_data = add_minecraft_folder(config_data, new_path)
                    print("已成功添加文件夹。")
                os.system("pause")
                return minecraft_folder_management_page(config_data)
            case "B" | "b":
                folder_index = input("你想要将哪个文件夹作为你的默认文件夹？请输入文件夹前面的数字序号：")
                if folder_index.isnumeric():
                    folder_index = int(folder_index)
                else:
                    print("你输入了非数字序号，请重新输入。", file = sys.stderr)
                    os.system("pause")
                    return minecraft_folder_management_page(config_data)
                if folder_index < 1 or folder_index > len(config_data["minecraft_folders"]):
                    print("你指定了不在列表中的序号，请重新输入。", file = sys.stderr)
                    os.system("pause")
                    return minecraft_folder_management_page(config_data)
                folder_uuid = list(config_data["minecraft_folders"].keys())[folder_index - 1]
                config_data = change_default_minecraft_folder(config_data, folder_uuid)
                print(f"已成功更改默认文件夹为 {config_data['minecraft_folders'][folder_uuid]['path']}。")
                os.system("pause")
                return minecraft_folder_management_page(config_data)
            case "C" | "c":
                config_data = change_folder_setting_page(config_data)
                return minecraft_folder_management_page(config_data)
            case "D" | "d":
                new_path = input(f"请输入你想要更改的路径：")
                if not new_path:
                    print("你没有输入任何路径。请重新输入。")
                    os.system("pause")
                    return minecraft_folder_management_page(config_data)
                new_path = os.path.abspath(os.path.expandvars(new_path.replace('"', '')))
                if not os.path.isdir(new_path):
                    print(f"{new_path} 不是一个文件夹或不存在。请检查你的输入，然后再试一次。", file = sys.stderr)
                elif check_folder_exists(config_data, new_path):
                    print(f"{new_path} 已经存在！", file = sys.stderr)
                else:
                    config_data = change_minecraft_folder_path(config_data, new_path = new_path)
                    print("更改文件夹路径成功！")
                os.system("pause")
                return minecraft_folder_management_page(config_data)
            case "E" | "e":
                folder_index = input("你想要删除哪个文件夹？请输入文件夹前面的数字序号：")
                if folder_index.isnumeric():
                    folder_index = int(folder_index)
                else:
                    print("你输入了非数字序号，请重新输入。", file = sys.stderr)
                    os.system("pause")
                    return minecraft_folder_management_page(config_data)
                if folder_index < 1 or folder_index > len(config_data["minecraft_folders"]):
                    print("你指定了不在列表中的序号，请重新输入。", file = sys.stderr)
                    os.system("pause")
                    return minecraft_folder_management_page(config_data)
                folder_uuid = list(config_data["minecraft_folders"].keys())[folder_index - 1]
                answer = input(f"你确定要删除 {config_data['minecraft_folders'][folder_uuid]['path']} 吗？（y/yes/是=删除，其他=保留）：")
                if answer in YES_LIST:
                    config_data = remove_minecraft_folder(config_data, folder_uuid)
                    print("删除成功！")
                else:
                    print("你已取消删除。")
                os.system("pause")
                return minecraft_folder_management_page(config_data)
            case "F" | "f":
                return config_data
            case _:
                print("你没有输入对应的选项。请再试一次。", file = sys.stderr)
                os.system("pause")
                return minecraft_folder_management_page(config_data)
    else:
        print("你输入了非数字序号或字母序号，请重新输入。", file = sys.stderr)
        os.system("pause")
        return minecraft_folder_management_page(config_data)