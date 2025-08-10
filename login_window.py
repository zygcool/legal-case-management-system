# 登录窗口模块
import tkinter as tk
from tkinter import ttk, messagebox
from database_config import DatabaseManager, UserManager
import hashlib

class LoginWindow:
    """登录窗口类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("律师办案智能助手 - 用户登录")
        self.root.geometry("400x580")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(False, False)
        
        # 居中显示窗口
        self.center_window()
        
        # 数据库管理器
        self.db_manager = DatabaseManager()
        self.user_manager = None
        
        # 用户信息
        self.current_user = None
        self.session_token = None
        
        # 创建界面
        self.create_login_interface()
        
        # 连接数据库
        self.connect_database()
    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def connect_database(self):
        """连接数据库"""
        if self.db_manager.connect():
            self.user_manager = UserManager(self.db_manager)
            self.status_label.config(text="数据库连接成功", fg="green")
        else:
            self.status_label.config(text="数据库连接失败，请检查配置", fg="red")
            messagebox.showerror("错误", "无法连接到数据库，请检查数据库配置")
    
    def create_login_interface(self):
        """创建登录界面"""
        # 主容器
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg='#f0f8ff')
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # 应用图标
        icon_label = tk.Label(title_frame, text="⚖️", font=('Arial', 48), 
                             bg='#f0f8ff', fg='#4a90e2')
        icon_label.pack(pady=(0, 10))
        
        # 应用标题
        title_label = tk.Label(title_frame, text="律师办案智能助手", 
                              font=('Microsoft YaHei', 18, 'bold'),
                              bg='#f0f8ff', fg='#333333')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="请登录您的账户", 
                                 font=('Microsoft YaHei', 12),
                                 bg='#f0f8ff', fg='#666666')
        subtitle_label.pack(pady=(5, 0))
        
        # 登录表单
        form_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 表单内容
        form_content = tk.Frame(form_frame, bg='#ffffff')
        form_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # 用户名输入行
        username_frame = tk.Frame(form_content, bg='#ffffff')
        username_frame.pack(fill=tk.X, pady=(0, 15))
        
        username_label = tk.Label(username_frame, text="用户名:", 
                                  font=('Microsoft YaHei', 11),
                                  bg='#ffffff', fg='#333333', width=8)
        username_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.username_entry = tk.Entry(username_frame, 
                                      font=('Microsoft YaHei', 11),
                                      relief=tk.FLAT, bd=5,
                                      bg='#f8f9fa')
        self.username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)
        
        # 密码输入行
        password_frame = tk.Frame(form_content, bg='#ffffff')
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        password_label = tk.Label(password_frame, text="密码:", 
                                 font=('Microsoft YaHei', 11),
                                 bg='#ffffff', fg='#333333', width=8)
        password_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.password_entry = tk.Entry(password_frame, 
                                      font=('Microsoft YaHei', 11),
                                      relief=tk.FLAT, bd=5,
                                      bg='#f8f9fa', show='*')
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)
        
        # 记住密码选项
        remember_frame = tk.Frame(form_content, bg='#ffffff')
        remember_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(remember_frame, text="记住密码",
                                       variable=self.remember_var,
                                       font=('Microsoft YaHei', 10),
                                       bg='#ffffff', fg='#666666')
        remember_check.pack(side=tk.LEFT)
        
        # 忘记密码链接
        forgot_label = tk.Label(remember_frame, text="忘记密码？",
                               font=('Microsoft YaHei', 10),
                               bg='#ffffff', fg='#4a90e2',
                               cursor='hand2')
        forgot_label.pack(side=tk.RIGHT)
        forgot_label.bind('<Button-1>', self.forgot_password)
        
        # 登录按钮
        login_btn = tk.Button(form_content, text="登录",
                             font=('Microsoft YaHei', 12, 'bold'),
                             bg='#4a90e2', fg='white',
                             relief=tk.FLAT, bd=0,
                             pady=12, cursor='hand2',
                             command=self.login)
        login_btn.pack(fill=tk.X, pady=(0, 15))
        
        # 注册链接
        register_frame = tk.Frame(form_content, bg='#ffffff')
        register_frame.pack(fill=tk.X)
        
        register_text = tk.Label(register_frame, text="还没有账户？",
                                font=('Microsoft YaHei', 10),
                                bg='#ffffff', fg='#666666')
        register_text.pack(side=tk.LEFT)
        
        register_link = tk.Label(register_frame, text="立即注册",
                                font=('Microsoft YaHei', 10),
                                bg='#ffffff', fg='#4a90e2',
                                cursor='hand2')
        register_link.pack(side=tk.LEFT, padx=(5, 0))
        register_link.bind('<Button-1>', self.show_register)
        
        # 状态栏
        status_frame = tk.Frame(main_frame, bg='#f0f8ff')
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(status_frame, text="正在连接数据库...",
                                    font=('Microsoft YaHei', 9),
                                    bg='#f0f8ff', fg='#666666')
        self.status_label.pack()
        
        # 绑定回车键登录
        self.root.bind('<Return>', lambda e: self.login())
        
        # 设置初始焦点
        self.username_entry.focus()
    
    def login(self):
        """用户登录"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
        
        if not self.user_manager:
            messagebox.showerror("错误", "数据库连接失败")
            return
        
        # 验证用户
        user = self.user_manager.authenticate_user(username, password)
        
        if user:
            # 创建会话
            token = self.user_manager.create_session(user['id'])
            
            if token:
                self.current_user = user
                self.session_token = token
                
                messagebox.showinfo("成功", f"欢迎，{user['full_name'] or user['username']}！")
                
                # 关闭登录窗口，打开主程序
                self.open_main_application()
            else:
                messagebox.showerror("错误", "创建会话失败")
        else:
            messagebox.showerror("错误", "用户名或密码错误")
    
    def open_main_application(self):
        """打开主应用程序"""
        self.root.destroy()
        
        # 导入并启动主程序
        from main import PDFChatApp
        
        main_root = tk.Tk()
        app = PDFChatApp(main_root, self.current_user, self.session_token, self.db_manager)
        main_root.mainloop()
    
    def show_register(self, event=None):
        """显示注册窗口"""
        register_window = RegisterWindow(self.db_manager)
        register_window.show()
    
    def forgot_password(self, event=None):
        """忘记密码处理"""
        messagebox.showinfo("提示", "请联系系统管理员重置密码")
    
    def run(self):
        """运行登录窗口"""
        self.root.mainloop()
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        if hasattr(self, 'db_manager') and self.db_manager:
            self.db_manager.disconnect()

class RegisterWindow:
    """注册窗口类"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.user_manager = UserManager(db_manager)
        
    def show(self):
        """显示注册窗口"""
        self.window = tk.Toplevel()
        self.window.title("用户注册")
        self.window.geometry("400x600")
        self.window.configure(bg='#f0f8ff')
        self.window.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 创建注册界面
        self.create_register_interface()
    
    def center_window(self):
        """窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_register_interface(self):
        """创建注册界面"""
        # 主容器
        main_frame = tk.Frame(self.window, bg='#f0f8ff')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # 标题
        title_label = tk.Label(main_frame, text="用户注册", 
                              font=('Microsoft YaHei', 18, 'bold'),
                              bg='#f0f8ff', fg='#333333')
        title_label.pack(pady=(0, 30))
        
        # 注册表单
        form_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        form_frame.pack(fill=tk.X)
        
        form_content = tk.Frame(form_frame, bg='#ffffff')
        form_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # 表单字段
        fields = [
            ("用户名:", "username"),
            ("密码:", "password"),
            ("确认密码:", "confirm_password"),
            ("真实姓名:", "full_name"),
            ("邮箱:", "email")
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            label = tk.Label(form_content, text=label_text,
                           font=('Microsoft YaHei', 11),
                           bg='#ffffff', fg='#333333')
            label.pack(anchor='w', pady=(0, 5))
            
            entry = tk.Entry(form_content,
                           font=('Microsoft YaHei', 11),
                           relief=tk.FLAT, bd=5,
                           bg='#f8f9fa')
            
            if 'password' in field_name:
                entry.config(show='*')
            
            entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
            self.entries[field_name] = entry
        
        # 注册按钮
        register_btn = tk.Button(form_content, text="注册",
                               font=('Microsoft YaHei', 12, 'bold'),
                               bg='#5cb85c', fg='white',
                               relief=tk.FLAT, bd=0,
                               pady=12, cursor='hand2',
                               command=self.register)
        register_btn.pack(fill=tk.X, pady=(0, 15))
        
        # 取消按钮
        cancel_btn = tk.Button(form_content, text="取消",
                             font=('Microsoft YaHei', 12),
                             bg='#6c757d', fg='white',
                             relief=tk.FLAT, bd=0,
                             pady=12, cursor='hand2',
                             command=self.window.destroy)
        cancel_btn.pack(fill=tk.X)
    
    def register(self):
        """用户注册"""
        # 获取表单数据
        data = {}
        for field_name, entry in self.entries.items():
            data[field_name] = entry.get().strip()
        
        # 验证数据
        if not all([data['username'], data['password'], data['confirm_password']]):
            messagebox.showerror("错误", "请填写必填字段")
            return
        
        if data['password'] != data['confirm_password']:
            messagebox.showerror("错误", "两次输入的密码不一致")
            return
        
        if len(data['password']) < 6:
            messagebox.showerror("错误", "密码长度至少6位")
            return
        
        # 检查用户名是否已存在
        check_query = "SELECT id FROM users WHERE username = %s"
        existing = self.db_manager.execute_query(check_query, (data['username'],))
        
        if existing:
            messagebox.showerror("错误", "用户名已存在")
            return
        
        # 创建用户
        hashed_password = UserManager.hash_password(data['password'])
        
        insert_query = """
            INSERT INTO users (username, password, full_name, email)
            VALUES (%s, %s, %s, %s)
        """
        
        user_id = self.db_manager.execute_insert(insert_query, (
            data['username'],
            hashed_password,
            data['full_name'] or None,
            data['email'] or None
        ))
        
        if user_id > 0:
            messagebox.showinfo("成功", "注册成功！请使用新账户登录。")
            self.window.destroy()
        else:
            messagebox.showerror("错误", "注册失败，请重试")

if __name__ == "__main__":
    # 启动登录窗口
    login_app = LoginWindow()
    login_app.run()