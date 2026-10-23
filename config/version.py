__lazy__ = ['os', 'json', 'requests', 'sys', 'time']

import os, json, requests, sys, time

def dump_version_list(version_list, save_path):
    json.dump(version_list, open(f"{save_path}{os.sep}version_manifest.json", "w", encoding = "utf-8"), ensure_ascii = False, indent = 4)

def load_version_list(load_path):
    return json.load(open(f"{load_path}{os.sep}version_manifest.json"))

def dump_client_manifest(client_manifest, save_path, has_multi_version):
    if has_multi_version:
        os.makedirs(f"{save_path}{os.sep}versions{os.sep}{client_manifest['id']}", exist_ok = True)
        json.dump(client_manifest, open(f"{save_path}{os.sep}versions{os.sep}{client_manifest['id']}{os.sep}{client_manifest['id']}.json", "w", encoding = "utf-8"), ensure_ascii = False, indent = 4)
    else:
        json.dump(client_manifest, open(f"{save_path}{os.sep}client.json", "w", encoding = "utf-8"), ensure_ascii = False, indent = 4)

def get_client_manifest(version_list, version):
    try:
        for i in version_list["versions"]:
            if i["id"] == version:
                client_manifest = requests.get(i["url"]).json()
                return client_manifest
    except:
        print(f"暂时无法下载版本 {version} 的客户端清单。请稍后再试。")
        time.sleep(3)
        sys.exit(1)