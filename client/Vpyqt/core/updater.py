import os
import shutil

def applyUpdate(main_exe):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(main_exe)))   # 工作目录，pyinstaller打包后的程序工作目录在_internal
    root_dir = os.path.dirname(base_dir)                   # 外层 ourTodos/

    print("开始应用更新...")
    # 把工作目录的ourTodos.exe覆盖掉root_dir的ourTodos.exe
    if not os.path.exists(os.path.join(base_dir, "ourTodos.exe")):
        return
    # 把base_dir的ui文件夹覆盖掉root_dir的ui文件夹
    if os.path.exists(os.path.join(root_dir, "ui")):
        shutil.rmtree(os.path.join(root_dir, "ui"))
    shutil.copytree(os.path.join(base_dir, "ui"), os.path.join(root_dir, "ui"))
    
    shutil.copy2(os.path.join(base_dir, "ourTodos.exe"), os.path.join(root_dir, "ourTodos.exe"))

    os.remove(os.path.join(base_dir, "ourTodos.exe"))  # 删除旧的main.exe
    print("更新完成 ✅")
    # QMessageBox.information(None,"info","更新完成 ✅")

if __name__=="__main__":
    print(__file__)
    applyUpdate(r"D:\myproject\git\our-todos\client\Vpyqt\dist\main\main.exe")