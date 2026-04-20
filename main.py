import sys
import os
import sqlite3
import json
import webbrowser
from datetime import datetime, date
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTreeWidget, 
                             QTreeWidgetItem, QInputDialog, QProgressBar, 
                             QMessageBox, QCheckBox, QSystemTrayIcon, QMenu, QStyle,
                             QFrame, QLineEdit, QGroupBox, QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt, QTimer, QDateTime, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor

# 处理打包后的资源路径
def resource_path(relative_path):
    """获取资源的绝对路径，支持开发和打包后的环境"""
    base_path = os.path.abspath(".")
    
    # 对于静态资源，检查是否在data/fig目录下
    if relative_path.endswith(('.png', '.css', '.ico')):
        print(f"尝试加载资源: {relative_path}")
        fig_path = os.path.join(base_path, "data", "fig", os.path.basename(relative_path))
        if os.path.exists(fig_path):
            print(f"资源路径: {fig_path}")
            return fig_path
    
    return os.path.join(base_path, relative_path)

class FocusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能待办系统 v5.0")
        self.resize(1000, 500)  # 扁平布局：高比宽长
        
        # 加载样式文件
        try:
            style_path = resource_path("style.css")
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"加载样式文件失败: {e}")
        
        self.remaining_time = 0
        self.current_duration = 0
        self.is_work_mode = False  # 启动时默认休息模式
        self.todos = []  # 存储待办事项数据
        
        self.init_db()
        self.init_ui()
        self.init_tray()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.load_todos()

    def init_db(self):
        """初始化 SQLite 数据库"""
        # 使用data/db目录存储数据库
        base_dir = os.path.abspath(".")
        db_dir = os.path.join(base_dir, "data", "db")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "focus_data.db")
        
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.db_cursor = self.conn.cursor()
        
        # history 表：记录专注场次
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS history 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             timestamp DATETIME, 
             duration INTEGER, 
             tasks_done_count INTEGER)''')
        
        # todos 表：存储待办事项
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS todos 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             description TEXT,
             created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
             updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
             completed BOOLEAN DEFAULT 0,
             steps TEXT DEFAULT '[]')''')  # 存储小步骤的JSON数组
        
        self.conn.commit()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central) 
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 顶部区域 - 模式选择和计时器
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setSpacing(10)
        
        # 模式选择区域
        mode_frame = QFrame()
        mode_frame.setObjectName("card")
        mode_layout = QVBoxLayout(mode_frame)
        
        mode_title = QLabel("计时模式")
        mode_title.setObjectName("section_title")
        mode_layout.addWidget(mode_title)
        
        # 模式选择按钮
        self.mode_group = QButtonGroup(self)
        
        mode_btn_layout = QHBoxLayout()
        self.work_mode_btn = QRadioButton("工作模式")
        self.work_mode_btn.toggled.connect(self.on_mode_changed)
        self.mode_group.addButton(self.work_mode_btn)
        mode_btn_layout.addWidget(self.work_mode_btn)
        
        self.rest_mode_btn = QRadioButton("休息模式")
        self.rest_mode_btn.setChecked(True)  # 默认选中休息模式
        self.rest_mode_btn.toggled.connect(self.on_mode_changed)
        self.mode_group.addButton(self.rest_mode_btn)
        mode_btn_layout.addWidget(self.rest_mode_btn)
        
        mode_layout.addLayout(mode_btn_layout)
        top_layout.addWidget(mode_frame)
        
        # 计时器区域
        timer_frame = QFrame()
        timer_frame.setObjectName("card")
        timer_layout = QVBoxLayout(timer_frame)
        
        # 模式图标和计时器在一行
        timer_top_layout = QHBoxLayout()
        
        # 模式图标
        self.mode_icon = QLabel()
        self.mode_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mode_icon.setMinimumWidth(80)
        self.mode_icon.setMinimumHeight(80)
        timer_top_layout.addWidget(self.mode_icon)
        self.update_mode_icon()
        
        # 计时器显示
        self.timer_display = QLabel("00:00")
        self.timer_display.setObjectName("timer_display")
        self.timer_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_top_layout.addWidget(self.timer_display, 2)  # 计时器占更多空间
        
        timer_layout.addLayout(timer_top_layout)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        self.btn_start = QPushButton("开始计时")
        self.btn_start.clicked.connect(self.start_session)
        self.btn_start.setMinimumHeight(35)
        control_layout.addWidget(self.btn_start)
        timer_layout.addLayout(control_layout)
        
        top_layout.addWidget(timer_frame)
        
        # 数据分析按钮（紧凑布局）
        stats_frame = QFrame()
        stats_frame.setObjectName("card")
        stats_layout = QHBoxLayout(stats_frame)  # 改为水平布局
        
        stats_title = QLabel("数据分析:")
        stats_title.setObjectName("section_title")
        stats_layout.addWidget(stats_title)
        
        self.btn_daily_stats = QPushButton("工作统计")
        self.btn_daily_stats.clicked.connect(self.show_daily_stats)
        self.btn_daily_stats.setMinimumHeight(30)
        stats_layout.addWidget(self.btn_daily_stats)
        
        self.btn_productivity = QPushButton("生产力总结")
        self.btn_productivity.clicked.connect(self.show_productivity_summary)
        self.btn_productivity.setMinimumHeight(30)
        stats_layout.addWidget(self.btn_productivity)
        
        top_layout.addWidget(stats_frame)
        
        # 窗口置顶选项
        self.cb_ontop = QCheckBox("窗口置顶")
        self.cb_ontop.stateChanged.connect(self.toggle_ontop)
        top_layout.addWidget(self.cb_ontop)
        
        main_layout.addWidget(top_widget)
        
        # 中间区域 - 待办事项
        todo_frame = QFrame()
        todo_frame.setObjectName("card")
        todo_layout = QVBoxLayout(todo_frame)
        
        todo_title = QLabel("待办事项")
        todo_title.setObjectName("section_title")
        todo_layout.addWidget(todo_title)
        
        # 待办树（调整大小适应扁平窗口）
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["待办事项", "进度"])
        self.tree.setColumnWidth(0, 300)  # 减少列宽
        self.tree.setColumnWidth(1, 60)
        self.tree.setMinimumHeight(300)  # 增加高度
        todo_layout.addWidget(self.tree)
        
        # 待办操作按钮
        todo_btn_layout = QHBoxLayout()
        self.btn_add_todo = QPushButton("+ 添加待办")
        self.btn_add_todo.setObjectName("add_task_btn")
        self.btn_add_todo.clicked.connect(self.add_todo_dialog)
        todo_btn_layout.addWidget(self.btn_add_todo)
        todo_layout.addLayout(todo_btn_layout)
        
        main_layout.addWidget(todo_frame, 2)  # 待办区域占更多空间
        
        # 底部状态栏
        self.status_label = QLabel("就绪 - 选择模式并开始计时")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #6c757d; font-size: 11px; padding: 3px;")
        todo_layout.addWidget(self.status_label)
        
        # 设置拉伸因子
        main_layout.setStretch(0, 1)  # 顶部区域
        main_layout.setStretch(1, 3)  # 待办区域（更多空间）

    def update_mode_icon(self):
        """更新模式图标"""
        try:
            if self.is_work_mode:
                icon_path = resource_path("work.png")
                pixmap = QPixmap(icon_path)
            else:
                icon_path = resource_path("rest.png")
                pixmap = QPixmap(icon_path)
            
            if not pixmap.isNull():
                # 缩放图标到合适大小（适应扁平窗口）
                scaled_pixmap = pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio, 
                                            Qt.TransformationMode.SmoothTransformation)
                self.mode_icon.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"加载图标失败: {e}")
    
    def update_tray_icon(self):
        """更新托盘图标"""
        try:
            if self.is_work_mode:
                icon_name = "work.png"
            else:
                icon_name = "rest.png"
            
            # 尝试多种路径
            possible_paths = [
                resource_path(icon_name),  # 通过resource_path函数
                os.path.join("data", "fig", icon_name),  # 直接相对路径
                os.path.join(os.path.dirname(__file__), "data", "fig", icon_name),  # 绝对路径
            ]
            
            icon = None
            used_path = None
            
            for icon_path in possible_paths:
                if os.path.exists(icon_path):
                    print(f"找到托盘图标: {icon_path}")
                    icon = QIcon(icon_path)
                    used_path = icon_path
                    if not icon.isNull():
                        break
                    else:
                        print(f"警告: 无法加载图标 {icon_path}")
                        icon = None
            
            if icon is not None and not icon.isNull():
                self.tray_icon.setIcon(icon)
                print(f"托盘图标已设置: {used_path}")
            else:
                print(f"警告: 所有图标路径都失败，使用默认图标")
                # 使用默认图标作为后备
                default_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
                self.tray_icon.setIcon(default_icon)
                
        except Exception as e:
            print(f"加载托盘图标失败: {e}")
            import traceback
            traceback.print_exc()
            # 使用默认图标作为后备
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
    
    def on_mode_changed(self):
        """模式切换处理"""
        self.is_work_mode = self.work_mode_btn.isChecked()
        self.update_mode_icon()
        self.update_tray_icon()  # 更新托盘图标
        
        if self.is_work_mode:
            self.status_label.setText("已切换到工作模式")
            self.btn_start.setText("开始工作")
        else:
            self.status_label.setText("已切换到休息模式")
            self.btn_start.setText("开始休息")
    
    def switch_to_work_mode(self):
        """切换到工作模式（从托盘菜单）"""
        self.work_mode_btn.setChecked(True)
        self.on_mode_changed()
    
    def switch_to_rest_mode(self):
        """切换到休息模式（从托盘菜单）"""
        self.rest_mode_btn.setChecked(True)
        self.on_mode_changed()
    
    def reload_styles(self):
        """重新加载样式文件"""
        try:
            style_path = resource_path("style.css")
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"重新加载样式文件失败: {e}")
    
    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.update_tray_icon()  # 设置初始托盘图标
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("显示窗口")
        show_action.triggered.connect(self.show_window)
        
        hide_action = tray_menu.addAction("隐藏窗口")
        hide_action.triggered.connect(self.hide_window)
        
        tray_menu.addSeparator()
        
        # 模式切换菜单项
        mode_submenu = tray_menu.addMenu("切换模式")
        
        work_mode_action = mode_submenu.addAction("工作模式")
        work_mode_action.triggered.connect(self.switch_to_work_mode)
        
        rest_mode_action = mode_submenu.addAction("休息模式")
        rest_mode_action.triggered.connect(self.switch_to_rest_mode)
        
        tray_menu.addSeparator()
        
        exit_action = tray_menu.addAction("退出程序")
        exit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
        
        self.status_label.setText("程序已启动 - 右键托盘图标可切换模式或退出")

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def hide_window(self):
        self.hide()

    def quit_application(self):
        """托盘菜单点击退出"""
        # 1. 先保存
        self.save_all_todos()
        
        # 2. 断开数据库连接
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            # 设为 None，防止 closeEvent 再次操作它
            self.conn = None 
            
        # 3. 彻底退出，不给 closeEvent 报错的机会
        QApplication.instance().exit()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()

    def load_todos(self):
        """从数据库加载待办事项（只显示未完成的）"""
        try:
            self.db_cursor.execute("SELECT id, title, description, completed, steps FROM todos WHERE completed = 0 ORDER BY created_at DESC")
            todos = self.db_cursor.fetchall()
            
            self.tree.clear()
            self.todos = []
            
            for todo_id, title, description, completed, steps_json in todos:
                steps = json.loads(steps_json) if steps_json else []
                todo_data = {
                    'id': todo_id,
                    'title': title,
                    'description': description,
                    'completed': bool(completed),
                    'steps': steps
                }
                self.todos.append(todo_data)
                
                # 创建树节点
                item = QTreeWidgetItem(self.tree)
                item.setText(0, title)
                item.setData(0, Qt.ItemDataRole.UserRole, todo_id)
                
                # 计算进度
                total_steps = len(steps)
                completed_steps = sum(1 for step in steps if step.get('completed', False))
                progress = f"{completed_steps}/{total_steps}" if total_steps > 0 else "0/0"
                item.setText(1, progress)
                
                # 添加子步骤
                for step in steps:
                    child = QTreeWidgetItem(item)
                    child.setText(0, f"  • {step['title']}")
                    child.setCheckState(0, Qt.CheckState.Checked if step.get('completed', False) else Qt.CheckState.Unchecked)
                    child.setData(0, Qt.ItemDataRole.UserRole, step)
                    
                item.setExpanded(True)
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载待办事项失败: {str(e)}")

    def add_todo_dialog(self):
        """添加待办事项对话框"""
        title, ok = QInputDialog.getText(self, "添加待办", "请输入待办事项标题:")
        if ok and title:
            description, ok = QInputDialog.getText(self, "描述", "请输入详细描述 (可选):")
            if not ok:
                description = ""
            
            try:
                self.db_cursor.execute(
                    "INSERT INTO todos (title, description, steps) VALUES (?, ?, ?)",
                    (title, description, '[]')
                )
                self.conn.commit()
                self.load_todos()
                self.status_label.setText(f"已添加待办: {title}")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"添加待办失败: {str(e)}")

    def delete_selected_todo(self):
        """删除选中的待办事项"""
        current_item = self.tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请先选择一个待办事项")
            return
        
        todo_id = current_item.data(0, Qt.ItemDataRole.UserRole)
        if not todo_id:
            return
        
        reply = QMessageBox.question(
            self, "确认删除",
            "确定要删除这个待办事项及其所有步骤吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
                self.conn.commit()
                self.load_todos()
                self.status_label.setText("已删除待办事项")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除失败: {str(e)}")

    def add_step_dialog(self, todo_id):
        """为待办事项添加小步骤"""
        step_title, ok = QInputDialog.getText(self, "添加步骤", "请输入步骤内容:")
        if ok and step_title:
            try:
                # 获取当前步骤
                self.db_cursor.execute("SELECT steps FROM todos WHERE id = ?", (todo_id,))
                result = self.db_cursor.fetchone()
                steps = json.loads(result[0]) if result and result[0] else []
                
                # 添加新步骤
                new_step = {
                    'id': len(steps) + 1,
                    'title': step_title,
                    'completed': False,
                    'created_at': datetime.now().isoformat()
                }
                steps.append(new_step)
                
                # 更新数据库
                self.db_cursor.execute(
                    "UPDATE todos SET steps = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (json.dumps(steps, ensure_ascii=False), todo_id)
                )
                self.conn.commit()
                self.load_todos()
                self.status_label.setText(f"已添加步骤: {step_title}")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"添加步骤失败: {str(e)}")

    def toggle_todo_completion(self, todo_id):
        """切换待办事项完成状态"""
        try:
            self.db_cursor.execute("SELECT completed, title FROM todos WHERE id = ?", (todo_id,))
            result = self.db_cursor.fetchone()
            if result:
                old_status = result[0]
                todo_title = result[1]
                new_status = 0 if old_status else 1
                
                self.db_cursor.execute(
                    "UPDATE todos SET completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (new_status, todo_id)
                )
                
                # 如果从未完成变为完成，记录到专注历史
                if not old_status and new_status:
                    self.db_cursor.execute(
                        "INSERT INTO history (timestamp, duration, tasks_done_count) VALUES (?, ?, ?)", 
                        (datetime.now(), 0, 1)  # 0分钟专注，完成1个任务
                    )
                    self.status_label.setText(f"已标记完成: {todo_title}")
                else:
                    self.status_label.setText(f"已标记未完成: {todo_title}")
                
                self.conn.commit()
                self.load_todos()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"更新状态失败: {str(e)}")

    def save_all_todos(self):
        """保存所有待办事项状态"""
        try:
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                if item:
                    todo_id = item.data(0, Qt.ItemDataRole.UserRole)
                    
                    # 更新步骤状态
                    steps = []
                    child_count = item.childCount()
                    for j in range(child_count):
                        child = item.child(j)
                        if child:
                            step_data = child.data(0, Qt.ItemDataRole.UserRole)
                            if step_data:
                                step_data['completed'] = child.checkState(0) == Qt.CheckState.Checked
                                steps.append(step_data)
                    
                    if todo_id:
                        self.db_cursor.execute(
                            "UPDATE todos SET steps = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                            (json.dumps(steps, ensure_ascii=False), todo_id)
                        )
            
            self.conn.commit()
            self.status_label.setText("所有待办已保存")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存失败: {str(e)}")

    def show_stats(self):
        """显示统计概览"""
        try:
            # 统计待办事项
            self.db_cursor.execute("SELECT COUNT(*) FROM todos")
            total_todos = self.db_cursor.fetchone()[0]
            
            self.db_cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 1")
            completed_todos = self.db_cursor.fetchone()[0]
            
            # 统计专注场次
            self.db_cursor.execute("SELECT COUNT(*), SUM(duration), SUM(tasks_done_count) FROM history")
            stats = self.db_cursor.fetchone()
            total_sessions = stats[0] or 0
            total_duration = stats[1] or 0
            total_tasks_done = stats[2] or 0
            
            stats_text = f"""
            📊 统计概览
            
            待办事项:
            • 总计: {total_todos} 个
            • 已完成: {completed_todos} 个
            • 进行中: {total_todos - completed_todos} 个
            
            专注记录:
            • 总场次: {total_sessions} 次
            • 总时长: {total_duration} 分钟
            • 完成任务: {total_tasks_done} 项
            
            今日专注:
            • 场次: {self.get_today_sessions()} 次
            • 时长: {self.get_today_duration()} 分钟
            """
            
            QMessageBox.information(self, "统计概览", stats_text.strip())
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"获取统计失败: {str(e)}")

    def get_today_sessions(self):
        """获取今日专注场次"""
        try:
            self.db_cursor.execute(
                "SELECT COUNT(*) FROM history WHERE date(timestamp) = date('now')"
            )
            return self.db_cursor.fetchone()[0] or 0
        except:
            return 0

    def get_today_duration(self):
        """获取今日专注总时长"""
        try:
            self.db_cursor.execute(
                "SELECT SUM(duration) FROM history WHERE date(timestamp) = date('now')"
            )
            result = self.db_cursor.fetchone()[0]
            return result or 0
        except:
            return 0



    def show_daily_stats(self):
        """显示每日工作统计"""
        try:
            # 动态导入PlotlyVisualizer
            from plotly_visualizer import PlotlyVisualizer
            visualizer = PlotlyVisualizer()
            result = visualizer.show_daily_work_chart(30)
            self.status_label.setText("工作统计图表已在浏览器中打开")
        except ImportError as e:
            QMessageBox.warning(self, "错误", f"无法加载Plotly可视化模块: {str(e)}\n请安装: pip install plotly pandas")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"显示工作统计失败: {str(e)}")
    
    def show_productivity_summary(self):
        """显示生产力总结"""
        try:
            # 动态导入PlotlyVisualizer
            from plotly_visualizer import PlotlyVisualizer
            visualizer = PlotlyVisualizer()
            result = visualizer.show_productivity_summary()
            self.status_label.setText("生产力总结已在浏览器中打开")
        except ImportError as e:
            QMessageBox.warning(self, "错误", f"无法加载Plotly可视化模块: {str(e)}\n请安装: pip install plotly pandas")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"显示生产力总结失败: {str(e)}")

    def start_session(self):
        if self.is_work_mode:
            title = "设置工作时间"
            default = 25
        else:
            title = "设置休息时间"
            default = 5
        
        mins, ok = QInputDialog.getInt(self, title, f"请输入{title[:-2]}分钟数:", default, 1, 180, 5)
        if ok:
            self.current_duration = mins
            self.remaining_time = mins * 60
            self.timer.start(1000)
            
            # 重新加载样式，确保样式不丢失
            self.reload_styles()
            
            # 禁用模式切换和开始按钮
            self.work_mode_btn.setEnabled(False)
            self.rest_mode_btn.setEnabled(False)
            self.btn_start.setEnabled(False)
            
            if self.is_work_mode:
                self.btn_start.setText("工作中...")
                self.status_label.setText(f"工作开始: {mins}分钟")
                # 更新托盘图标提示
                self.tray_icon.setToolTip(f"工作中 - 剩余{mins}分钟")
            else:
                self.btn_start.setText("休息中...")
                self.status_label.setText(f"休息开始: {mins}分钟")
                # 更新托盘图标提示
                self.tray_icon.setToolTip(f"休息中 - 剩余{mins}分钟")

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            m, s = divmod(self.remaining_time, 60)
            self.timer_display.setText(f"{m:02d}:{s:02d}")
            
            # 更新托盘提示
            if self.is_work_mode:
                self.tray_icon.setToolTip(f"工作中 - 剩余{m:02d}:{s:02d}")
            else:
                self.tray_icon.setToolTip(f"休息中 - 剩余{m:02d}:{s:02d}")
            
            # 每10秒自动保存一次
            if self.remaining_time % 10 == 0:
                self.save_all_todos()
        else:
            self.timer.stop()
            self.finalize_session()

    def finalize_session(self):
        """倒计时结束：统计并持久化"""
        if self.is_work_mode:
            # 工作模式：统计完成的步骤并记录到数据库
            done_count = 0
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                if item:
                    child_count = item.childCount()
                    for j in range(child_count):
                        child = item.child(j)
                        if child and child.checkState(0) == Qt.CheckState.Checked:
                            done_count += 1
            
            # 写入数据库
            try:
                self.db_cursor.execute(
                    "INSERT INTO history (timestamp, duration, tasks_done_count) VALUES (?, ?, ?)", 
                    (datetime.now(), self.current_duration, done_count)
                )
                self.conn.commit()
                
                # 显示完成统计
                stats_text = f"""
                🎉 工作完成！
                
                本次工作:
                • 时长: {self.current_duration} 分钟
                • 完成步骤: {done_count} 个
                
                休息一下，准备下一轮工作！
                """
                
                QMessageBox.information(self, "工作结束", stats_text.strip())
                self.status_label.setText(f"工作完成: {done_count}个步骤")
                
            except Exception as e:
                QMessageBox.warning(self, "错误", f"保存工作记录失败: {str(e)}")
        else:
            # 休息模式：不记录到数据库，显示红光提醒
            self.show_window()
            self.raise_()
            self.activateWindow()
            
            # 保存原始样式
            self.original_style = self.styleSheet()
            
            # 应用红色警报样式
            red_alert_style = """
                QMainWindow {
                    background-color: #ff0000;
                    border: 5px solid #cc0000;
                }
                QFrame#card {
                    background-color: rgba(255, 255, 255, 0.9);
                    border-radius: 12px;
                    border: 2px solid #ff6666;
                    padding: 15px;
                    margin: 5px;
                }
                QLabel#timer_display {
                    font-size: 72px;
                    font-weight: 900;
                    color: white;
                    background-color: rgba(255, 0, 0, 0.8);
                    padding: 15px;
                    border-radius: 15px;
                    margin: 10px 0;
                    border: 3px solid #ff6666;
                }
                QPushButton {
                    background-color: #ff6666;
                    color: white;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-weight: 600;
                    font-size: 14px;
                    border: 2px solid #ff3333;
                }
                QPushButton:hover {
                    background-color: #ff3333;
                    border-color: #ff0000;
                }
                QRadioButton {
                    color: white;
                    font-weight: bold;
                }
                QCheckBox {
                    color: white;
                    font-weight: bold;
                }
                QLabel {
                    color: white;
                    font-weight: bold;
                }
            """
            
            # 应用红色样式
            self.setStyleSheet(red_alert_style)
            
            # 强制重绘窗口
            self.repaint()
            QApplication.processEvents()
            
            # 显示休息结束提醒（模态对话框会阻塞）
            reply = QMessageBox.information(
                self, 
                "休息结束", 
                f"🎉 休息完成！\n\n休息时长: {self.current_duration} 分钟\n\n准备开始工作吧！",
                QMessageBox.StandardButton.Ok
            )
            
            # 用户点击OK后恢复原样式
            self.reload_styles()
            self.status_label.setText("休息完成，准备开始工作")
        
        # 更新界面
        self.work_mode_btn.setEnabled(True)
        self.rest_mode_btn.setEnabled(True)
        self.btn_start.setEnabled(True)
        
        # 恢复托盘提示
        if self.is_work_mode:
            self.btn_start.setText("开始工作")
            self.tray_icon.setToolTip("工作模式就绪")
        else:
            self.btn_start.setText("开始休息")
            self.tray_icon.setToolTip("休息模式就绪")

    def toggle_ontop(self, state):
        flags = self.windowFlags()
        if state:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
        
        self.setWindowFlags(flags)
        self.show()
        self.status_label.setText("窗口置顶已" + ("开启" if state else "关闭"))

    def closeEvent(self, event):
        """点击窗口右上角 X"""
        # 检查连接是否还存在（如果是从 quit_application 触发的，此时 conn 应该是 None）
        if hasattr(self, 'conn') and self.conn:
            self.save_all_todos()
            self.hide()
            self.status_label.setText("程序已最小化到托盘")
            event.ignore()
        else:
            # 如果 conn 已经没了，说明是正常的程序退出流程
            event.accept()

    def tree_item_changed(self, item, column):
        """树节点状态变化时保存"""
        if column == 0 and item.childCount() == 0:  # 只处理步骤节点
            self.save_all_todos()
    
    def show_todo_context_menu(self, position):
        """显示待办项的右键菜单"""
        item = self.tree.itemAt(position)
        if not item:
            return
        
        todo_id = item.data(0, Qt.ItemDataRole.UserRole)
        if not todo_id:  # 不是待办项（可能是步骤）
            return
        
        # 获取待办项的完成状态
        completed = False
        for todo in self.todos:
            if todo['id'] == todo_id:
                completed = todo['completed']
                break
        
        menu = QMenu()
        
        # 添加步骤
        add_step_action = menu.addAction("添加步骤")
        add_step_action.triggered.connect(lambda: self.add_step_dialog(todo_id))
        
        # 切换完成状态
        toggle_action = menu.addAction("标记为完成" if not completed else "标记为未完成")
        toggle_action.triggered.connect(lambda: self.toggle_todo_completion(todo_id))
        
        menu.addSeparator()
        
        # 删除待办
        delete_action = menu.addAction("删除待办")
        delete_action.triggered.connect(lambda: self.delete_todo_by_id(todo_id))
        
        menu.exec(self.tree.viewport().mapToGlobal(position))
    
    def delete_todo_by_id(self, todo_id):
        """根据ID删除待办事项"""
        reply = QMessageBox.question(
            self, "确认删除",
            "确定要删除这个待办事项及其所有步骤吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
                self.conn.commit()
                self.load_todos()
                self.status_label.setText("已删除待办事项")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除失败: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    QApplication.setQuitOnLastWindowClosed(False)
    
    # 设置应用程序图标（任务栏图标）
    try:
        icon_path = resource_path("work.png")
        app_icon = QIcon(icon_path)
        if not app_icon.isNull():
            app.setWindowIcon(app_icon)
            print(f"应用程序图标已设置: {icon_path}")
        else:
            print("警告: 无法加载应用程序图标，使用默认图标")
            app.setWindowIcon(QIcon())
    except Exception as e:
        print(f"设置应用程序图标失败: {e}")
        app.setWindowIcon(QIcon())
    
    win = FocusApp()
    win.show()
    
    # 连接树节点变化信号
    win.tree.itemChanged.connect(win.tree_item_changed)
    
    # 启用右键菜单
    win.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    win.tree.customContextMenuRequested.connect(win.show_todo_context_menu)
    
    sys.exit(app.exec())