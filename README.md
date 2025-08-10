# 法律卷宗管理系统

一个用于管理法律案件卷宗和PDF文件的桌面应用程序。

## 主要功能

- 卷宗信息管理
- PDF文件批量处理和预览
- 智能预加载和缓存机制
- 用户友好的图形界面
- 数据库存储和管理

## 技术栈

- Python 3.x
- Tkinter (GUI)
- SQLite (数据库)
- PyPDF2, pdfplumber, PyMuPDF (PDF处理)
- PIL (图像处理)

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python main.py
```

## 项目结构

- `main.py` - 主应用程序
- `database_config.py` - 基础数据库配置
- `database_config_enhanced.py` - 增强数据库功能
- `login_window.py` - 登录窗口
- `database_schema.sql` - 数据库结构
- `requirements.txt` - 项目依赖

## 贡献

欢迎提交问题和改进建议！