import os
import shutil

def applyUpdate(main_exe):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(main_exe)))   # 工作目录，pyinstaller打包后的程序工作目录在_internal
    root_dir = os.path.dirname(base_dir)                   # 外层 ourTodos/
    update_dir = base_dir       # 子目录（旧的updater解压出来的）
    print(base_dir)
    print(root_dir)
    print(update_dir)

    if not os.path.exists(update_dir):
        print(update_dir)
        print("没有发现 ourTodos 更新目录，跳过更新")
        # QMessageBox.information(None,"info",update_dir+"没有发现 ourTodos 更新目录，跳过更新")
        return

    print("开始应用更新...")

    for root, dirs, files in os.walk(update_dir):
        rel_path = os.path.relpath(root, update_dir)
        target_root = os.path.join(root_dir, rel_path) if rel_path != "." else root_dir

        os.makedirs(target_root, exist_ok=True)

        for f in files:
            src_file = os.path.join(root, f)
            dst_file = os.path.join(target_root, f)

            try:
                if os.path.exists(dst_file):
                    os.remove(dst_file)  # 删除旧文件（包括旧的 updater.exe）
                shutil.copy2(src_file, dst_file)
                print(f"更新: {dst_file}")
            except Exception as e:
                print(f"无法更新 {dst_file}: {e}")

    # 删除 ourTodos 子目录（清理现场）
    # shutil.rmtree(update_dir, ignore_errors=True)

    print("更新完成 ✅")
    # QMessageBox.information(None,"info","更新完成 ✅")

if __name__=="__main__":
    print(__file__)
    applyUpdate(r"D:\myproject\git\our-todos\client\Vpyqt\dist\main\main.exe")