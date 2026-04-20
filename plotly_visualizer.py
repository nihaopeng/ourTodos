#!/usr/bin/env python3
"""
使用Plotly进行数据可视化
生成每日工作时间折线图，支持悬停查看当天完成的工作
"""

import sqlite3
import os
import webbrowser
import tempfile
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class PlotlyVisualizer:
    def __init__(self, db_path=None):
        """初始化可视化器"""
        if db_path is None:
            # 使用data/db目录的数据库
            base_dir = os.path.abspath(".")
            db_path = os.path.join(base_dir, "data", "db", "focus_data.db")
        
        self.db_path = db_path
        print(f"PlotlyVisualizer 数据库路径: {self.db_path}")
    
    def get_daily_stats(self, days=30):
        """获取每日统计数据"""
        conn = sqlite3.connect(self.db_path)
        
        # 获取最近N天的数据
        query = """
        SELECT 
            date(timestamp) as day,
            SUM(duration) as total_duration,
            SUM(tasks_done_count) as total_tasks,
            GROUP_CONCAT(DISTINCT 
                CASE WHEN tasks_done_count > 0 THEN 
                    (SELECT GROUP_CONCAT(title, '; ') 
                     FROM todos 
                     WHERE date(updated_at) = date(h.timestamp) 
                     AND completed = 1)
                ELSE '' END
            ) as completed_tasks
        FROM history h
        WHERE date(timestamp) >= date('now', ?)
        GROUP BY date(timestamp)
        ORDER BY day DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(f'-{days} days',))
        conn.close()
        
        # 处理数据
        if not df.empty:
            df['day'] = pd.to_datetime(df['day'])
            df['total_duration'] = df['total_duration'].fillna(0).astype(int)
            df['total_tasks'] = df['total_tasks'].fillna(0).astype(int)
            df['completed_tasks'] = df['completed_tasks'].fillna('无')
        
        return df
    
    def create_daily_work_chart(self, days=30):
        """创建每日工作时间折线图"""
        df = self.get_daily_stats(days)
        
        if df.empty:
            return None
        
        # 创建图表
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('每日工作时间（分钟）', '每日完成任务数'),
            vertical_spacing=0.15,
            row_heights=[0.6, 0.4]
        )
        
        # 添加工作时间折线图
        fig.add_trace(
            go.Scatter(
                x=df['day'],
                y=df['total_duration'],
                mode='lines+markers',
                name='工作时间',
                line=dict(color='#4dabf7', width=3),
                marker=dict(size=8, color='#339af0'),
                hovertemplate=(
                    '<b>日期: %{x|%Y-%m-%d}</b><br>' +
                    '工作时间: %{y}分钟<br>' +
                    '完成任务: %{customdata[0]}个<br>' +
                    '完成事项: %{customdata[1]}<br>' +
                    '<extra></extra>'
                ),
                customdata=df[['total_tasks', 'completed_tasks']].values
            ),
            row=1, col=1
        )
        
        # 添加任务数柱状图
        fig.add_trace(
            go.Bar(
                x=df['day'],
                y=df['total_tasks'],
                name='完成任务',
                marker_color='#40c057',
                hovertemplate=(
                    '<b>日期: %{x|%Y-%m-%d}</b><br>' +
                    '完成任务: %{y}个<br>' +
                    '<extra></extra>'
                )
            ),
            row=2, col=1
        )
        
        # 更新布局
        fig.update_layout(
            title=dict(
                text=f'最近{days}天工作统计',
                x=0.5,
                font=dict(size=20, color='#2c3e50')
            ),
            template='plotly_white',
            hovermode='x unified',
            showlegend=True,
            height=700,
            margin=dict(t=80, b=50, l=50, r=50)
        )
        
        # 更新x轴
        fig.update_xaxes(
            title_text="日期",
            tickformat="%m-%d",
            row=1, col=1
        )
        fig.update_xaxes(
            title_text="日期",
            tickformat="%m-%d",
            row=2, col=1
        )
        
        # 更新y轴
        fig.update_yaxes(
            title_text="工作时间（分钟）",
            row=1, col=1
        )
        fig.update_yaxes(
            title_text="完成任务数",
            row=2, col=1
        )
        
        return fig
    
    def show_daily_work_chart(self, days=30):
        """显示每日工作图表（在浏览器中打开）"""
        fig = self.create_daily_work_chart(days)
        
        if fig is None:
            return "没有找到历史数据"
        
        # 创建临时HTML文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_file = f.name
            fig.write_html(
                html_file,
                include_plotlyjs='cdn',
                full_html=True,
                auto_open=False
            )
        
        # 在浏览器中打开
        webbrowser.open(f'file://{html_file}')
        
        return f"图表已在浏览器中打开: {html_file}"
    
    def create_productivity_summary(self):
        """创建生产力总结图表"""
        conn = sqlite3.connect(self.db_path)
        
        # 获取总体统计
        queries = {
            'total_sessions': "SELECT COUNT(*) FROM history",
            'total_duration': "SELECT SUM(duration) FROM history",
            'total_tasks': "SELECT SUM(tasks_done_count) FROM history",
            'total_todos': "SELECT COUNT(*) FROM todos",
            'completed_todos': "SELECT COUNT(*) FROM todos WHERE completed = 1"
        }
        
        stats = {}
        for key, query in queries.items():
            cursor = conn.execute(query)
            stats[key] = cursor.fetchone()[0] or 0
        
        conn.close()
        
        # 创建仪表板
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('总工作时间', '总完成任务', '待办统计', '专注场次'),
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}]]
        )
        
        # 总工作时间
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=stats['total_duration'],
                title={"text": "分钟"},
                number={'suffix': " min", 'font': {'size': 40}},
                domain={'row': 0, 'column': 0}
            ),
            row=1, col=1
        )
        
        # 总完成任务
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=stats['total_tasks'],
                title={"text": "个任务"},
                number={'suffix': " 个", 'font': {'size': 40}},
                domain={'row': 0, 'column': 1}
            ),
            row=1, col=2
        )
        
        # 待办统计
        if stats['total_todos'] > 0:
            completed_percent = (stats['completed_todos'] / stats['total_todos']) * 100
        else:
            completed_percent = 0
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=completed_percent,
                title={'text': "待办完成率"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#40c057"},
                    'steps': [
                        {'range': [0, 50], 'color': "#fa5252"},
                        {'range': [50, 80], 'color': "#fab005"},
                        {'range': [80, 100], 'color': "#40c057"}
                    ]
                },
                domain={'row': 1, 'column': 0}
            ),
            row=2, col=1
        )
        
        # 专注场次
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=stats['total_sessions'],
                title={"text": "场次"},
                number={'suffix': " 次", 'font': {'size': 40}},
                domain={'row': 1, 'column': 1}
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title=dict(
                text='生产力总结',
                x=0.5,
                font=dict(size=24, color='#2c3e50')
            ),
            template='plotly_white',
            height=600,
            margin=dict(t=100, b=50, l=50, r=50)
        )
        
        return fig
    
    def show_productivity_summary(self):
        """显示生产力总结（在浏览器中打开）"""
        fig = self.create_productivity_summary()
        
        # 创建临时HTML文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_file = f.name
            fig.write_html(
                html_file,
                include_plotlyjs='cdn',
                full_html=True,
                auto_open=False
            )
        
        # 在浏览器中打开
        webbrowser.open(f'file://{html_file}')
        
        return f"生产力总结已在浏览器中打开: {html_file}"

def main():
    """测试函数"""
    visualizer = PlotlyVisualizer()
    
    print("1. 显示每日工作图表")
    result = visualizer.show_daily_work_chart(30)
    print(result)
    
    print("\n2. 显示生产力总结")
    result = visualizer.show_productivity_summary()
    print(result)

if __name__ == "__main__":
    main()