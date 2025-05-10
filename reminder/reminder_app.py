import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ReminderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("智能休息提醒器")
        # 增加图标文件存在性校验
        if not os.path.exists(resource_path('icon.ico')):
            raise FileNotFoundError("图标文件缺失，请确保icon.ico存在于项目根目录")
        try:
            self.root.iconbitmap(resource_path('icon.ico'))
        except Exception as e:
            print(f"图标加载失败: {str(e)}")
        
        self.is_running = False
        self.start_time = 0
        
        self.setup_ui()
        self.setup_tray_icon()
        
    def setup_ui(self):
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()
        
        self.status_label = tk.Label(self.frame, text="状态: 未运行", font=('微软雅黑', 12))
        self.status_label.pack(pady=10)
        
        self.start_btn = tk.Button(self.frame, text="开始", command=self.toggle_reminder,
                                  bg='#4CAF50', fg='white', font=('微软雅黑', 10))
        self.start_btn.pack(pady=5)
        
        self.time_label = tk.Label(self.frame, text="已运行: 0 分钟", font=('微软雅黑', 10))
        self.time_label.pack(pady=5)
        
    def setup_tray_icon(self):
        # 系统托盘功能需要额外库支持，此处留作后续扩展
        pass
        
    def toggle_reminder(self):
        if not self.is_running:
            self.start_reminder()
        else:
            self.stop_reminder()
        
    def start_reminder(self):
        self.is_running = True
        self.start_time = time.time()
        self.start_btn.config(text="停止", bg='#f44336')
        self.status_label.config(text="状态: 运行中")
        
        threading.Thread(target=self.reminder_loop, daemon=True).start()
        
    def stop_reminder(self):
        self.is_running = False
        self.start_btn.config(text="开始", bg='#4CAF50')
        self.status_label.config(text="状态: 已停止")
        
    def reminder_loop(self):
        while self.is_running:
            elapsed = (time.time() - self.start_time) / 60
            self.time_label.config(text=f"已运行: {int(elapsed)} 分钟")
            
            if elapsed >= 90:
                self.stop_reminder()
                messagebox.showinfo("完成", "90分钟计时已完成！")
                break
            
            interval = random.randint(180, 300)  # 3-5分钟
            time.sleep(interval)
            
            if self.is_running:
                self.root.iconify()
                self.root.deiconify()
                messagebox.showinfo("休息提醒", "该站起来活动一下了！", parent=self.root)
            
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def on_close(self):
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            self.root.destroy()

if __name__ == "__main__":
    app = ReminderApp()
    app.run()