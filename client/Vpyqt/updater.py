import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import zipfile
import os, sys, shutil, time, subprocess

class UpdaterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ourTodos 安装器")
        self.root.geometry("400x200")

        self.label = tk.Label(root, text="正在检查更新...")
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(root, length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.button = tk.Button(root, text="开始更新", state="disabled", command=self.start_update)
        self.button.pack(pady=10)

        self.update_info = None
        threading.Thread(target=self.check_update).start()

    def check_update(self):
        try:
            resp = requests.get(GITEE_RELEASE_API, timeout=5)
            data = resp.json()
            latest_version = data["tag_name"].lstrip("v")
            changelog = data.get("body", "")
            assets = data.get("assets", [])
            download_url = assets[0]["browser_download_url"] if assets else None

            if latest_version > APP_VERSION and download_url:
                self.update_info = {"version": latest_version, "changelog": changelog, "url": download_url}
                self.label.config(text=f"发现新版本 {latest_version}:\n{changelog}")
                self.button.config(state="normal")
            else:
                self.launch_app()
        except Exception as e:
            messagebox.showerror("错误", f"检查更新失败: {e}")
            self.launch_app()

    def start_update(self):
        if not self.update_info:
            return
        self.button.config(state="disabled")
        self.label.config(text="正在下载更新包...")
        threading.Thread(target=self.download_file).start()

    def download_file(self):
        url = self.update_info["url"]
        zip_path = os.path.join(APP_DIR, "update.zip")
        with requests.get(url, stream=True) as r:
            total = int(r.headers.get("Content-Length", 0))
            downloaded = 0
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            percent = int(downloaded * 100 / total)
                            self.progress["value"] = percent
        self.extract_and_replace(zip_path)
        messagebox.showinfo("更新完成", "应用已更新到最新版本")
        self.launch_app()

    def extract_and_replace(self, zip_path):
        new_dir = os.path.join(APP_DIR, "_new")
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(new_dir)
        time.sleep(1)
        preserve_files = ["_internal/core/config.toml"]
        ignore_files = ["ourTodos.exe"]
        for root, _, files in os.walk(new_dir):
            rel_path = os.path.relpath(root, new_dir)
            dest_dir = os.path.join(APP_DIR, rel_path) if rel_path != "." else APP_DIR
            os.makedirs(dest_dir, exist_ok=True)
            for f in files:
                rel_file = os.path.normpath(os.path.join(rel_path, f)) if rel_path != "." else f
                if rel_file in ignore_files or rel_file in preserve_files:
                    continue
                src_file = os.path.join(root, f)
                dst_file = os.path.join(dest_dir, f)
                if os.path.exists(dst_file):
                    try:
                        os.remove(dst_file)
                    except PermissionError:
                        continue
                shutil.move(src_file, dst_file)
        shutil.rmtree(new_dir, ignore_errors=True)
        os.remove(zip_path)

    def launch_app(self):
        main_exe = os.path.join(APP_DIR, "main", APP_NAME)
        if os.path.exists(main_exe):
            # 用批处理延迟启动，避免文件占用
            bat_path = os.path.join(APP_DIR, "launch.bat")
            with open(bat_path, "w") as f:
                f.write(f"""
                @echo off
                timeout /t 1 >nul
                start "" "{main_exe}"
                del "%~f0"
                """)
            subprocess.Popen([bat_path], shell=True)
        self.root.after(100, self.root.destroy)

if __name__ == "__main__":
    APP_NAME = "main.exe"
    try:
        import toml
        APP_VERSION = toml.load("main/_internal/core/config.toml")["SOFTWAREINFO"]["VERSION"]
    except:
        APP_VERSION = "0"
    APP_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    GITEE_OWNER = "helloyutao"
    GITEE_REPO = "our-todos"
    GITEE_RELEASE_API = f"https://gitee.com/api/v5/repos/{GITEE_OWNER}/{GITEE_REPO}/releases/latest"

    root = tk.Tk()
    app = UpdaterWindow(root)
    root.mainloop()
