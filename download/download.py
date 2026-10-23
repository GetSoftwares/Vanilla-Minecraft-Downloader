__lazy__ = ["os", "os.path", "sys", "hashlib", "datetime", "copy"]

import os, os.path, sys, hashlib, datetime as dt, copy
from config import *

def download_special_version(client_manifest, /, minecraft_folder: str, has_multi_version: bool, check_hash: bool, auto_retry: bool, show_log: bool, debug: bool):
    version = client_manifest["id"]
    pending_download = {"libraries": [], "assets": []}
    retry_queue = copy.deepcopy(pending_download)
    hash_size_failed_queue = copy.deepcopy(pending_download)
    # client.jar
    if show_log:
        print("开始下载客户端……")
    client_jar = client_manifest["downloads"]["client"]["url"]
    if has_multi_version:
        dump_client_manifest(client_manifest, minecraft_folder, has_multi_version)
        downloaded_jar = f"{minecraft_folder}{os.sep}versions{os.sep}{version}{os.sep}{version}.jar"
    else:
        try:
            os.rename(f"{minecraft_folder}{os.sep}client.jar", f"{minecraft_folder}{os.sep}client.jar.bak")
            os.rename(f"{minecraft_folder}{os.sep}client.json", f"{minecraft_folder}{os.sep}client.json.bak")
        except OSError:
            print("当前 Minecraft 实例正在运行，请关闭实例后重试。", file = sys.stderr)
            sys.exit(1)
        dump_client_manifest(client_manifest, minecraft_folder, has_multi_version)
        downloaded_jar = f"{minecraft_folder}{os.sep}client.jar"
    failed = True
    if auto_retry:
        retry = MAX_RETRY
        hash_size_failed = False
        while retry:
            os.system(f'aria2c --disable-ipv6=true -x4 -s4 -c -R -d"{os.path.dirname(downloaded_jar)}" -o"{os.path.basename(downloaded_jar)}" {'--auto-file-renaming=false --allow-overwrite=true' if hash_size_failed else ''} {client_jar} 1>{"CON" if show_log else "NUL"}')
            hash_size_failed = False
            if not os.path.exists(downloaded_jar):
                print("错误：客户端下载失败，将重新下载……", file = sys.stderr)
            elif os.path.exists(f"{downloaded_jar}.aria2"):
                print("错误：客户端下载未完成，将继续下载……", file = sys.stderr)
            elif (current_size := os.path.getsize(downloaded_jar)) != (required_size := client_manifest["downloads"]["client"]["size"]):
                print(f"错误：客户端大小不正确，预期大小 {required_size}，实际大小 {current_size}，将继续下载……", file = sys.stderr)
                hash_size_failed = True
            elif check_hash and (current_hash := hashlib.file_digest(open(downloaded_jar, "rb"), "sha1").hexdigest().lower()) != (required_hash := client_manifest["downloads"]["client"]["sha1"]):
                print(f"错误：客户端哈希不正确，预期哈希 {required_hash}，实际哈希 {current_hash}，将重新下载……", file = sys.stderr)
                hash_size_failed = True
            else:
                failed = False
            if failed:
                print("客户端下载失败，将重新下载……")
                retry -= 1
            else:
                break
        else:
            print("下载失败：重试次数已用尽，请重新下载！", file = sys.stderr)
            sys.exit(1)
    else:
        os.system(f'aria2c --disable-ipv6=true -x4 -s4 -c -R -d"{os.path.dirname(downloaded_jar)}" -o"{os.path.basename(downloaded_jar)}" {client_jar} 1>{"CON" if show_log else "NUL"}')
        if not os.path.exists(downloaded_jar):
            print("错误：客户端下载失败！", file = sys.stderr)
        elif os.path.exists(f"{downloaded_jar}.aria2"):
            print("错误：客户端下载未完成！", file = sys.stderr)
        elif (current_size := os.path.getsize(downloaded_jar)) != (required_size := client_manifest["downloads"]["client"]["size"]):
            print(f"错误：客户端大小不正确，预期大小 {required_size}，实际大小 {current_size}！", file = sys.stderr)
        elif check_hash and (current_hash := hashlib.file_digest(open(downloaded_jar, "rb"), "sha1").hexdigest().lower()) != (required_hash := client_manifest["downloads"]["client"]["sha1"]):
            print(f"错误：客户端哈希不正确，预期哈希 {required_hash}，实际哈希 {current_hash}！", file = sys.stderr)
        else:
            failed = False
        if failed:
            print("下载失败：客户端下载失败，请重新下载！", file = sys.stderr)
            sys.exit(1)
    if show_log:
        print("客户端下载完毕！")
    # log
    if client_manifest.get("logging"):
        if show_log:
            print("开始下载 log4j2 日志配置文件……")
        log4j2_xml = client_manifest["logging"]["client"]["file"]["url"]
        if has_multi_version:
            dump_client_manifest(client_manifest, minecraft_folder, has_multi_version)
            downloaded_log4j2_xml = f"{minecraft_folder}{os.sep}versions{os.sep}{version}{os.sep}log4j2.xml"
        else:
            try:
                os.rename(f"{minecraft_folder}{os.sep}client.jar", f"{minecraft_folder}{os.sep}log4j2.bak")
            except OSError:
                print("当前 Minecraft 实例正在运行，请关闭实例后重试。", file = sys.stderr)
                sys.exit(1)
            dump_client_manifest(client_manifest, minecraft_folder, has_multi_version)
            downloaded_log4j2_xml = f"{minecraft_folder}{os.sep}log4j2.xml"
        failed = True
        if auto_retry:
            hash_size_failed = False
            retry = MAX_RETRY
            while retry:
                os.system(f'aria2c --disable-ipv6=true -c -R -d"{os.path.dirname(downloaded_log4j2_xml)}" -o"{os.path.basename(downloaded_log4j2_xml)}" {'--auto-file-renaming=false --allow-overwrite=true' if hash_size_failed else ''} {log4j2_xml} 1>{"CON" if show_log else "NUL"}')
                hash_size_failed = False
                if not os.path.exists(downloaded_log4j2_xml):
                    print("错误：log4j2 日志配置文件下载失败，将重新下载……", file = sys.stderr)
                elif os.path.exists(f"{downloaded_log4j2_xml}.aria2"):
                    print("错误：log4j2 日志配置文件下载未完成，将继续下载……", file = sys.stderr)
                elif (current_size := os.path.getsize(downloaded_log4j2_xml)) != (required_size := client_manifest["logging"]["client"]["file"]["size"]):
                    print(f"错误：log4j2 日志配置文件大小不正确，预期大小 {required_size}，实际大小 {current_size}，将继续下载……", file = sys.stderr)
                    hash_size_failed = True
                elif check_hash and (current_hash := hashlib.file_digest(open(downloaded_log4j2_xml, "rb"), "sha1").hexdigest().lower()) != (required_hash := client_manifest["logging"]["client"]["file"]["sha1"]):
                    print(f"错误：log4j2 日志配置文件哈希不正确，预期哈希 {required_hash}，实际哈希 {current_hash}，将重新下载……", file = sys.stderr)
                    hash_size_failed = True
                else:
                    failed = False
                if failed:
                    print("log4j2 日志配置文件下载失败，将重新下载……")
                    retry -= 1
                else:
                    break
            else:
                print("下载失败：重试次数已用尽，请重新开始下载！", file = sys.stderr)
                sys.exit(1)
        else:
            os.system(f'aria2c --disable-ipv6=true -c -R -d"{os.path.dirname(downloaded_log4j2_xml)}" -o"{os.path.basename(downloaded_log4j2_xml)}" {log4j2_xml} 1>{"CON" if show_log else "NUL"}')
            if not os.path.exists(downloaded_log4j2_xml):
                print("错误：log4j2 日志配置文件下载失败！", file = sys.stderr)
            elif os.path.exists(f"{downloaded_log4j2_xml}.aria2"):
                print("错误：log4j2 日志配置文件下载未完成！", file = sys.stderr)
            elif (current_size := os.path.getsize(downloaded_log4j2_xml)) != (required_size := client_manifest["logging"]["client"]["file"]["size"]):
                print(f"错误：log4j2 日志配置文件大小不正确，预期大小 {required_size}，实际大小 {current_size}！", file = sys.stderr)
            elif check_hash and (current_hash := hashlib.file_digest(open(downloaded_log4j2_xml, "rb"), "sha1").hexdigest().lower()) != (required_hash := client_manifest["logging"]["client"]["file"]["sha1"]):
                print(f"错误：log4j2 日志配置文件哈希不正确，预期哈希 {required_hash}，实际哈希 {current_hash}！", file = sys.stderr)
            else:
                failed = False
            if failed:
                print("下载失败：log4j2 日志配置文件下载失败，请重新下载！", file = sys.stderr)
                sys.exit(1)
        if show_log:
            print("log4j2 日志配置文件下载完毕！")
    # libraries
    if show_log:
        print("开始下载依赖库……")
    for entry in client_manifest["libraries"]:
        if entry.get("rules"):
            allow = True
            for rule in entry["rules"]:
                if rule["action"] == "allow":
                    if rule.get("os"):
                        allow = is_target_platform(rule["os"]["name"])
                elif rule["action"] == "disallow":
                    if rule.get("os"):
                        allow = not is_target_platform(rule["os"]["name"])
            if allow:
                if entry["downloads"].get("artifact"):
                    pending_download["libraries"].append({"name": entry["name"], "download": entry["downloads"]["artifact"]})
                if entry["downloads"].get("classifiers"):
                    pending_download["libraries"].append({"name": entry["name"], "download": entry["downloads"]["classifiers"][entry["natives"][get_platform()].replace(r"${arch}", "64" if sys.maxsize > 2**31-1 else "32")]})
        else:
            if entry["downloads"].get("artifact"):
                pending_download["libraries"].append({"name": entry["name"], "download": entry["downloads"]["artifact"]})
            if entry["downloads"].get("classifiers"):
                pending_download["libraries"].append({"name": entry["name"], "download": entry["downloads"]["classifiers"][entry["natives"][get_platform()].replace(r"${arch}", "64" if sys.maxsize > 2**31-1 else "32")]})
    if debug:
        print(f"等待下载的库：{pending_download["libraries"]}", file = sys.stderr)
    failed = True
    if auto_retry:
        retry = MAX_RETRY
        while retry:
            with open(f"{minecraft_folder}{os.sep}download.list", "w", encoding = "utf-8") as index_file:
                for entry in pending_download["libraries"]:
                    library_file = f"{minecraft_folder}{os.sep}libraries{os.sep}{entry['download']['path'].replace('/', os.sep)}"
                    if os.path.exists(library_file):
                        if show_log:
                            print(f"{library_file} 存在，跳过")
                        continue
                    if show_log:
                        print(f"正在将 {entry['name']} 加入下载队列……")
                    print(f"""{entry['download']['url']}
  out={entry['download']['path']}
""", file = index_file)
                for entry in retry_queue["libraries"]:
                    if show_log:
                        print(f"正在将 {entry['name']} 加入下载队列……")
                    print(f"""{entry['download']['url']}
  out={entry['download']['path']}
""", file = index_file)
                    pending_download["libraries"].append(entry)
                for entry in hash_size_failed_queue["libraries"]:
                    if show_log:
                        print(f"正在将 {entry['name']} 加入下载队列……")
                    print(f"""{entry['download']['url']}
  out={entry['download']['path']}
  auto-file-renaming=false
  allow-overwrite=true
""", file = index_file)
                    pending_download["libraries"].append(entry)
            retry_queue["libraries"].clear()
            hash_size_failed_queue["libraries"].clear()
            if show_log:
                print("下载列表创建完毕，开始下载……")
            os.system(f'aria2c --disable-ipv6=true -x16 -j16 -s16 -c -R -d{minecraft_folder}{os.sep}libraries -i"{minecraft_folder}{os.sep}download.list" --auto-file-renaming=false --allow-overwrite=false 1>{'CON' if show_log else 'NUL'} 2>&1')
            if show_log:
                print("下载完毕，开始检查下载的文件……")
            for entry in pending_download["libraries"]:
                library_file = f"{minecraft_folder}{os.sep}libraries{os.sep}{entry['download']['path'].replace('/', os.sep)}"
                if not os.path.exists(library_file):
                    print(f"错误：依赖库 {entry['name']} 不存在，将重新下载……", file = sys.stderr)
                    retry_queue["libraries"].append(entry)
                elif os.path.exists(f"{library_file}.aria2"):
                    print(f"错误：依赖库 {entry['name']} 未下载完成，将继续下载……", file = sys.stderr)
                    retry_queue["libraries"].append(entry)
                elif (current_size := os.path.getsize(library_file)) != entry["download"]["size"]:
                    print(f"错误：依赖库 {entry['name']} 的大小不正确，预期大小 {entry['download']['size']}，实际大小 {current_size}，将重新下载……", file = sys.stderr)
                    hash_size_failed_queue["libraries"].append(entry)
                elif check_hash and (current_hash := hashlib.file_digest(open(library_file, "rb"), "sha1").hexdigest().lower()) != (required_hash := entry["download"]["sha1"].lower()):
                    print(f"错误：依赖库 {entry['name']} 的大小不正确，预期哈希 {required_hash}，实际哈希 {current_hash}，将重新下载……", file = sys.stderr)
                    hash_size_failed_queue["libraries"].append(entry)
            else:
                failed = False
            if failed:
                print("依赖库有部分文件下载失败，将重新下载……", file = sys.stderr)
                pending_download["libraries"].clear()
                retry -= 1
            else:
                break
        else:
            print("下载失败：重试次数已用尽，请重新开始下载！", file = sys.stderr)
            sys.exit(1)
    else:
        with open(f"{minecraft_folder}{os.sep}download.list", "w", encoding = "utf-8") as index_file:
            for entry in pending_download["libraries"]:
                library_file = f"{minecraft_folder}{os.sep}libraries{os.sep}{entry['download']['path'].replace('/', os.sep)}"
                if os.path.exists(library_file):
                    if show_log:
                        print(f"{library_file} 存在，跳过")
                    continue
                if show_log:
                    print(f"正在将 {entry['name']} 加入下载队列……")
                print(f"""{entry['download']['url']}
  out={entry['download']['path']}
""", file = index_file)
        if show_log:
            print("下载列表创建完毕，开始下载……")
        os.system(f'aria2c --disable-ipv6=true -x16 -j16 -s16 -c -R -d{minecraft_folder}{os.sep}libraries -i"{minecraft_folder}{os.sep}download.list" --auto-file-renaming=false --allow-overwrite=false 1>{'CON' if show_log else 'NUL'} 2>&1')
        if show_log:
            print("下载完毕，开始检查下载的文件……")
        for entry in pending_download["libraries"]:
            library_file = f"{minecraft_folder}{os.sep}libraries{os.sep}{entry['download']['path'].replace('/', os.sep)}"
            if not os.path.exists(library_file):
                print(f"错误：依赖库 {entry['name']} 不存在！", file = sys.stderr)
            elif os.path.exists(f"{library_file}.aria2"):
                print(f"错误：依赖库 {entry['name']} 未下载完成！", file = sys.stderr)
            elif (current_size := os.path.getsize(library_file)) != entry["download"]["size"]:
                print(f"错误：依赖库 {entry['name']} 的大小不正确，预期大小 {entry['download']['size']}，实际大小 {current_size}！", file = sys.stderr)
            elif check_hash and (current_hash := hashlib.file_digest(open(library_file, "rb"), "sha1").hexdigest().lower()) != (required_hash := entry["download"]["sha1"].lower()):
                print(f"错误：依赖库 {entry['name']} 的大小不正确，预期哈希 {required_hash}，实际哈希 {current_hash}！", file = sys.stderr)
        else:
            failed = False
        if failed:
            print("下载失败：依赖库有部分文件下载失败，请重新下载！", file = sys.stderr)
            sys.exit(1)
    if show_log:
        print("依赖库下载完毕！")
    # assetindex
    downloaded_assetindex = f"{minecraft_folder}{os.sep}assets{os.sep}indexes{os.sep}{client_manifest['assetIndex']['id']}.json"
    if show_log:
        print("开始下载资源索引文件……")
    assetindex_url = client_manifest["assetIndex"]["url"]
    failed = True
    if auto_retry:
        retry = MAX_RETRY
        hash_size_failed = False
        while retry:
            os.system(f'aria2c --disable-ipv6=true -c -R -d"{os.path.dirname(downloaded_assetindex)}" -o"{os.path.basename(downloaded_assetindex)}" {'--auto-file-renaming=false --allow-overwrite=true' if hash_size_failed else ''} {assetindex_url} 1>{"CON" if show_log else "NUL"}')
            hash_size_failed = False
            if not os.path.exists(downloaded_assetindex):
                print("错误：资源索引文件下载失败，将重新下载……", file = sys.stderr)
            elif os.path.exists(f"{downloaded_assetindex}.aria2"):
                print("错误：资源索引文件下载未完成，将继续下载……", file = sys.stderr)
            elif (current_size := os.path.getsize(downloaded_assetindex)) != (required_size := client_manifest["assetIndex"]["size"]):
                print(f"错误：资源索引文件大小不正确，预期大小 {required_size}，实际大小 {current_size}，将继续下载……", file = sys.stderr)
                hash_size_failed = True
            elif check_hash and (current_hash := hashlib.file_digest(open(downloaded_assetindex, "rb"), "sha1").hexdigest().lower()) != (required_hash := client_manifest["assetIndex"]["sha1"]):
                print(f"错误：资源索引文件哈希不正确，预期哈希 {required_hash}，实际哈希 {current_hash}，将重新下载……", file = sys.stderr)
                hash_size_failed = True
            else:
                failed = False
            if failed:
                print("资源索引文件下载失败，将重新下载……")
                retry -= 1
            else:
                break
        else:
            print("下载失败：重试次数已用尽，请重新开始下载！", file = sys.stderr)
            sys.exit(1)
    else:
        os.system(f'aria2c --disable-ipv6=true -c -R -d"{os.path.dirname(downloaded_assetindex)}" -o"{os.path.basename(downloaded_assetindex)}" {assetindex_url} 1>{"CON" if show_log else "NUL"}')
        if not os.path.exists(downloaded_assetindex):
            print("错误：资源索引文件下载失败！", file = sys.stderr)
        elif os.path.exists(f"{downloaded_assetindex}.aria2"):
            print("错误：资源索引文件下载未完成！", file = sys.stderr)
        elif (current_size := os.path.getsize(downloaded_assetindex)) != (required_size := client_manifest["assetIndex"]["size"]):
            print(f"错误：资源索引文件大小不正确，预期大小 {required_size}，实际大小 {current_size}！", file = sys.stderr)
        elif check_hash and (current_hash := hashlib.file_digest(open(downloaded_assetindex, "rb"), "sha1").hexdigest().lower()) != (required_hash := client_manifest["assetIndex"]["sha1"]):
            print(f"错误：资源索引文件哈希不正确，预期哈希 {required_hash}，实际哈希 {current_hash}！", file = sys.stderr)
        else:
            failed = False
        if failed:
            print("下载失败：资源索引文件下载失败，请重新下载！", file = sys.stderr)
            sys.exit(1)
    if show_log:
        print("资源索引文件下载完毕！")
    # assets
    if show_log:
        print("开始下载资源文件……")
    assetindex = json.load(open(downloaded_assetindex, "r", encoding = "utf-8"))["objects"]
    for entry in assetindex:
        pending_download["assets"].append({"path": entry, "size": assetindex[entry]["size"], "hash": assetindex[entry]["hash"]})
    failed = True
    if auto_retry:
        retry = MAX_RETRY
        while retry:
            with open(f"{minecraft_folder}{os.sep}download.list", "w", encoding = "utf-8") as index_file:
                for entry in pending_download["assets"]:
                    asset_file = f"{minecraft_folder}{os.sep}assets{os.sep}objects{os.sep}{entry['hash'][:2]}{os.sep}{entry['hash']}"
                    if os.path.exists(asset_file):
                        if show_log:
                            print(f"{asset_file} 存在，跳过")
                        continue
                    if show_log:
                        print(f"正在将 {entry['path']} 加入下载队列……")
                    print(f"""{RESOURCES_DOWNLOAD_URL}/{entry['hash'][:2]}/{entry['hash']}
  out={entry['hash'][:2]}{os.sep}{entry['hash']}
""", file = index_file)
                for entry in retry_queue["assets"]:
                    if show_log:
                        print(f"正在将 {entry['path']} 加入下载队列……")
                    print(f"""{RESOURCES_DOWNLOAD_URL}/{entry['hash'][:2]}/{entry['hash']}
  out={entry['hash'][:2]}{os.sep}{entry['hash']}
""", file = index_file)
                    pending_download["assets"].append(entry)
                for entry in hash_size_failed_queue["assets"]:
                    if show_log:
                        print(f"正在将 {entry['path']} 加入下载队列……")
                    print(f"""{RESOURCES_DOWNLOAD_URL}/{entry['hash'][:2]}/{entry['hash']}
  out={entry['hash'][:2]}{os.sep}{entry['hash']}
  auto-file-renaming=false
  allow-overwrite=true
""", file = index_file)
                    pending_download["assets"].append(entry)
            retry_queue["assets"].clear()
            hash_size_failed_queue["assets"].clear()
            if show_log:
                print("下载列表创建完毕，开始下载……")
            os.system(f'aria2c --disable-ipv6=true -x16 -j16 -s16 -c -R -d{minecraft_folder}{os.sep}assets{os.sep}objects -i"{minecraft_folder}{os.sep}download.list" --auto-file-renaming=false --allow-overwrite=false 1>{'CON' if show_log else 'NUL'} 2>&1')
            if show_log:
                print("下载完毕，开始检查下载的文件……")
            for entry in pending_download["assets"]:
                asset_file = f"{minecraft_folder}{os.sep}assets{os.sep}objects{os.sep}{entry['hash'][:2]}{os.sep}{entry['hash']}"
                if not os.path.exists(asset_file):
                    print(f"错误：资源文件 {entry['path']} 不存在，将重新下载……", file = sys.stderr)
                    retry_queue["assets"].append(entry)
                elif os.path.exists(f"{asset_file}.aria2"):
                    print(f"错误：资源文件 {entry['path']} 未下载完成，将继续下载……", file = sys.stderr)
                    retry_queue["assets"].append(entry)
                elif (current_size := os.path.getsize(asset_file)) != entry["size"]:
                    print(f"错误：资源文件 {entry['path']} 的大小不正确，预期大小 {entry['download']['size']}，实际大小 {current_size}，将重新下载……", file = sys.stderr)
                    hash_size_failed_queue["assets"].append(entry)
                elif check_hash and (current_hash := hashlib.file_digest(open(asset_file, "rb"), "sha1").hexdigest().lower()) != (required_hash := entry["hash"].lower()):
                    print(f"错误：资源文件 {entry['path']} 的大小不正确，预期哈希 {required_hash}，实际哈希 {current_hash}，将重新下载……", file = sys.stderr)
                    hash_size_failed_queue["assets"].append(entry)
            else:
                failed = False
            if failed:
                print("资源文件有部分文件下载失败，将重新下载……", file = sys.stderr)
                pending_download["assets"].clear()
                retry -= 1
            else:
                break
        else:
            print("下载失败：重试次数已用尽，请重新开始下载！", file = sys.stderr)
            sys.exit(1)
    else:
        with open(f"{minecraft_folder}{os.sep}download.list", "w", encoding = "utf-8") as index_file:
            for entry in pending_download["assets"]:
                asset_file = f"{minecraft_folder}{os.sep}assets{os.sep}objects{os.sep}{entry['hash'][:2]}{os.sep}{entry['hash']}"
                if os.path.exists(asset_file):
                    if show_log:
                        print(f"{asset_file} 存在，跳过")
                    continue
                if show_log:
                    print(f"正在将 {entry['path']} 加入下载队列……")
                print(f"""{RESOURCES_DOWNLOAD_URL}/{entry['hash'][:2]}/{entry['hash']}
  out={entry['hash'][:2]}{os.sep}{entry['hash']}
""", file = index_file)
        if show_log:
            print("下载列表创建完毕，开始下载……")
        os.system(f'aria2c --disable-ipv6=true -x16 -j16 -s16 -c -R -d{minecraft_folder}{os.sep}assets{os.sep}objects -i"{minecraft_folder}{os.sep}download.list" --auto-file-renaming=false --allow-overwrite=false 1>{'CON' if show_log else 'NUL'} 2>&1')
        if show_log:
            print("下载完毕，开始检查下载的文件……")
        for entry in pending_download["assets"]:
            asset_file = f"{minecraft_folder}{os.sep}assets{os.sep}objects{os.sep}{entry['hash'][:2]}{os.sep}{entry['hash']}"
            if not os.path.exists(asset_file):
                print(f"错误：资源文件 {entry['path']} 不存在！", file = sys.stderr)
            elif os.path.exists(f"{asset_file}.aria2"):
                print(f"错误：资源文件 {entry['path']} 未下载完成！", file = sys.stderr)
            elif (current_size := os.path.getsize(asset_file)) != entry["size"]:
                print(f"错误：资源文件 {entry['path']} 的大小不正确，预期大小 {entry['download']['size']}，实际大小 {current_size}！", file = sys.stderr)
            elif check_hash and (current_hash := hashlib.file_digest(open(asset_file, "rb"), "hash").hexdigest().lower()) != (required_hash := entry["hash"].lower()):
                print(f"错误：资源文件 {entry['path']} 的大小不正确，预期哈希 {required_hash}，实际哈希 {current_hash}！", file = sys.stderr)
        else:
            failed = False
        if failed:
            print("下载失败：资源文件有部分文件下载失败，请重新下载！", file = sys.stderr)
            sys.exit(1)
    if show_log:
        print("资源文件下载完毕！")
    # Done
    print(f"版本 {version} 下载完毕！")
    time.sleep(3)
    return

def download_latest_none_april_fool_version(version_list, /, minecraft_folder: str, has_multi_version: bool, check_hash: bool, auto_retry: bool, show_log: bool, debug: bool):
    for version in version_list["versions"]:
        release_time = dt.datetime.fromisoformat(version["releaseTime"])
        if (release_time.month, release_time.day) in [(3, 31), (4, 1), (4, 2)]:
            continue
        else:
            download_special_version(get_client_manifest(version_list, version["id"]), minecraft_folder, has_multi_version, check_hash, auto_retry, show_log, debug)
            return