import os
import sys
import time
import zipfile
import shutil
import requests
import subprocess

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QProgressBar, QPushButton, QMessageBox
)
from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import QTimer
from PySide6.QtCore import QSharedMemory
import toml

# ========== 配置 ==========
APP_NAME = "main.exe"   # 主程序名字
try:
    APP_VERSION=toml.load("main/_internal/core/config.toml")["SOFTWAREINFO"]["VERSION"]# 当前本地版本号
except Exception as e:
    print(e)
    APP_VERSION='0'
APP_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

# Gitee 仓库信息
GITEE_OWNER = "helloyutao"   # 你的 Gitee 用户名或组织名
GITEE_REPO = "our-todos"       # 仓库名
GITEE_RELEASE_API = f"https://gitee.com/api/v5/repos/{GITEE_OWNER}/{GITEE_REPO}/releases/latest"


# ========== 下载线程 ==========
class DownloadThread(QThread):
    progress = Signal(int)
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get("Content-Length", 0))
                downloaded = 0

                with open(self.save_path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total > 0:
                                percent = int(downloaded * 100 / total)
                                self.progress.emit(percent)
            self.finished.emit(self.save_path)
        except Exception as e:
            self.failed.emit(str(e))


# ========== 更新器主窗口 ==========
class UpdaterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ourTodos安装器")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        self.label = QLabel("正在检查更新...")
        self.progress = QProgressBar()
        self.button = QPushButton("开始更新")
        self.button.setEnabled(False)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.start_update)
        self.update_info = None

        self.check_update()

    def check_update(self):
        try:
            resp = requests.get(GITEE_RELEASE_API, timeout=5)
            data = resp.json()

            latest_version = data["tag_name"].lstrip("v")  # 去掉前缀 v
            changelog = data.get("body", "")
            assets = data.get("assets", [])
            download_url = assets[0]["browser_download_url"] if assets else None

            if latest_version > APP_VERSION and download_url:
                self.update_info = {
                    "version": latest_version,
                    "changelog": changelog,
                    "url": download_url
                }
                self.label.setText(f"发现新版本 {latest_version}:\n{changelog}")
                self.button.setEnabled(True)
            else:
                # self.label.setText("已是最新版本")
                self.launch_app()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"检查更新失败: {e}")
            self.launch_app()

    def start_update(self):
        if not self.update_info:
            return
        url = self.update_info["url"]
        zip_path = os.path.join(APP_DIR, "update.zip")

        self.button.setEnabled(False)
        self.label.setText("正在下载更新包...")
        self.progress.setValue(0)

        self.dl_thread = DownloadThread(url, zip_path)
        self.dl_thread.progress.connect(self.progress.setValue)
        self.dl_thread.finished.connect(self.on_download_finished)
        self.dl_thread.failed.connect(self.on_download_failed)
        self.dl_thread.start()

    def on_download_failed(self, msg):
        QMessageBox.critical(self, "下载失败", msg)
        self.launch_app()

    def on_download_finished(self, zip_path):
        self.label.setText("下载完成，正在安装...")
        QApplication.processEvents()
        try:
            self.extract_and_replace(zip_path)
            QMessageBox.information(self, "更新完成", "应用已更新到最新版本")
            self.launch_app()
        except Exception as e:
            QMessageBox.critical(self, "安装失败", str(e))

    def extract_and_replace(self, zip_path):
        new_dir = os.path.join(APP_DIR, "_new")
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(new_dir)

        time.sleep(1)

        preserve_files = ["_internal/core/config.toml"]
        ignore_files = ["updater.exe"]

        print("版本更新")
        # 遍历新版本内容，覆盖旧目录
        for root, _, files in os.walk(new_dir):
            rel_path = os.path.relpath(root, new_dir)
            dest_dir = os.path.join(APP_DIR, rel_path) if rel_path != "." else APP_DIR
            os.makedirs(dest_dir, exist_ok=True)

            for f in files:
                rel_file = os.path.normpath(os.path.join(rel_path, f)) if rel_path != "." else f

                if rel_file in ignore_files:
                    continue
                if rel_file in preserve_files:
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
        main_exe = os.path.join(APP_DIR,"main", APP_NAME)
        if os.path.exists(main_exe):
            subprocess.Popen([main_exe], cwd=os.path.join(APP_DIR,"main"))
        QTimer.singleShot(100, self.close)

# ========== 入口 ==========
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UpdaterWindow()
    win.show()
    sys.exit(app.exec())
