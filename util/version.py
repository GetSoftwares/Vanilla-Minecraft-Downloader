__lazy__ = ['os', 'json', 'requests', 'sys', 'urllib3']

import os, json, requests, sys, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def dump_version_list(version_list, save_path):
    """转储版本列表。

    参数：

    version_list: 版本列表

    save_path: 要保存到的 Minecraft 文件夹"""
    json.dump(version_list, open(f"{save_path}{os.sep}version_manifest.json", "w", encoding = "utf-8"), ensure_ascii = False, indent = 4)

def load_version_list(load_path):
    """加载版本列表。

    参数：

    load_path: 要加载的 Minecraft 文件夹"""
    return json.load(open(f"{load_path}{os.sep}version_manifest.json"))

def dump_client_manifest(client_manifest, save_path, has_multi_version):
    """转储客户端清单。

    参数：

    client_manifest: 客户端清单

    save_path: 要保存到的 Minecraft 文件夹

    has_multi_version: 是否使用版本隔离，这会影响最终的保存路径"""
    if has_multi_version:
        os.makedirs(f"{save_path}{os.sep}versions{os.sep}{client_manifest['id']}", exist_ok = True)
        json.dump(client_manifest, open(f"{save_path}{os.sep}versions{os.sep}{client_manifest['id']}{os.sep}{client_manifest['id']}.json", "w", encoding = "utf-8"), ensure_ascii = False, indent = 4)
    else:
        json.dump(client_manifest, open(f"{save_path}{os.sep}client.json", "w", encoding = "utf-8"), ensure_ascii = False, indent = 4)

def get_client_manifest(version_list, version, /, ssl_verify):
    """获取指定版本的客户端清单。

    参数：

    version_list: 版本列表

    version: 要获取的版本

    ssl_verify: 是否进行 SSL 证书验证"""
    try:
        for i in version_list["versions"]:
            if i["id"] == version:
                client_manifest = requests.get(i["url"], verify = ssl_verify).json()
                return client_manifest
    except:
        print(f"暂时无法下载版本 {version} 的客户端清单。请稍后再试。")
        os.system("pause")
        sys.exit(1)