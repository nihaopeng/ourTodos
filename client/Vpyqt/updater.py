import os, sys, requests, subprocess, tempfile, zipfile

APP_VERSION = "1.0.0"

def check_update():
    url = "https://example.com/version.json"
    try:
        r = requests.get(url, timeout=5)
        info = r.json()
        if info["version"] > APP_VERSION:
            return info
    except Exception as e:
        print("检查更新失败:", e)
    return None

def download_zip(url):
    tmp_path = os.path.join(tempfile.gettempdir(), "update.zip")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
    return tmp_path

def run_updater(zip_path):
    updater_path = os.path.join(os.path.dirname(sys.executable), "updater.exe")
    subprocess.Popen([updater_path, zip_path, sys.executable])
    sys.exit(0)  # 退出主程序

import os, sys, time, zipfile, shutil

def extract_and_replace(zip_path, target_exe):
    app_dir = os.path.dirname(target_exe)

    # 等待主程序退出
    time.sleep(2)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.namelist():
            # 先删除旧文件（避免覆盖失败）
            dest_path = os.path.join(app_dir, member)
            if os.path.exists(dest_path):
                if os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)
                else:
                    os.remove(dest_path)
            zip_ref.extract(member, app_dir)

    # 删除zip
    os.remove(zip_path)

    # 重启主程序
    os.startfile(target_exe)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: updater.exe update.zip target.exe")
        sys.exit(1)

    zip_path, target_exe = sys.argv[1], sys.argv[2]
    extract_and_replace(zip_path, target_exe)
