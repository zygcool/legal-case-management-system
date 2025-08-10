-- 卷宗管理系统数据库结构
-- 创建数据库
CREATE DATABASE IF NOT EXISTS lawyer_assistant DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE lawyer_assistant;

-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
    email VARCHAR(100) COMMENT '邮箱',
    full_name VARCHAR(100) COMMENT '真实姓名',
    role ENUM('admin', 'user') DEFAULT 'user' COMMENT '用户角色',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '用户状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    last_login TIMESTAMP NULL COMMENT '最后登录时间'
) COMMENT='用户表';

-- 卷宗表
CREATE TABLE cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_name VARCHAR(200) NOT NULL COMMENT '卷宗名称',
    case_number VARCHAR(100) UNIQUE COMMENT '卷宗案号',
    file_path VARCHAR(500) NOT NULL COMMENT '卷宗文件在本地硬盘的完整路径',
    file_size BIGINT COMMENT '文件大小（字节）',
    file_type VARCHAR(20) DEFAULT 'PDF' COMMENT '文件类型',
    description TEXT COMMENT '卷宗描述',
    created_by INT NOT NULL COMMENT '创建用户ID',
    status ENUM('active', 'archived', 'deleted') DEFAULT 'active' COMMENT '卷宗状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT
) COMMENT='卷宗表';

-- 卷宗目录表（对应目录框中的内容）
CREATE TABLE case_directories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT NOT NULL COMMENT '所属卷宗ID',
    sequence_number VARCHAR(20) NOT NULL COMMENT '目录序号',
    file_name VARCHAR(300) NOT NULL COMMENT '文件名称',
    page_number INT NOT NULL COMMENT '页码',
    sort_order INT DEFAULT 0 COMMENT '排序顺序',
    is_custom BOOLEAN DEFAULT FALSE COMMENT '是否为用户自定义添加',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE,
    INDEX idx_case_id (case_id),
    INDEX idx_sort_order (sort_order)
) COMMENT='卷宗目录表';

-- 用户会话表（可选，用于管理登录状态）
CREATE TABLE user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE COMMENT '会话令牌',
    expires_at TIMESTAMP NOT NULL COMMENT '过期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_token (session_token),
    INDEX idx_expires_at (expires_at)
) COMMENT='用户会话表';

-- 操作日志表（可选，记录用户操作）
CREATE TABLE operation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    case_id INT NULL COMMENT '相关卷宗ID',
    operation_type ENUM('login', 'logout', 'create_case', 'update_case', 'delete_case', 'add_directory', 'update_directory', 'delete_directory') NOT NULL COMMENT '操作类型',
    operation_detail TEXT COMMENT '操作详情',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_operation_type (operation_type),
    INDEX idx_created_at (created_at)
) COMMENT='操作日志表';

-- 插入默认管理员用户（密码需要在应用中加密）
INSERT INTO users (username, password, email, full_name, role) VALUES 
('admin', 'admin123', 'admin@example.com', '系统管理员', 'admin');

-- 创建索引以提高查询性能
CREATE INDEX idx_cases_created_by ON cases(created_by);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_directories_case_page ON case_directories(case_id, page_number);

-- 创建视图：卷宗目录详情视图
CREATE VIEW case_directory_view AS
SELECT 
    cd.id,
    cd.case_id,
    c.case_name,
    c.case_number,
    cd.sequence_number,
    cd.file_name,
    cd.page_number,
    cd.sort_order,
    cd.is_custom,
    cd.created_at,
    cd.updated_at,
    u.username as created_by_username
FROM case_directories cd
JOIN cases c ON cd.case_id = c.id
JOIN users u ON c.created_by = u.id
WHERE c.status = 'active'
ORDER BY cd.case_id, cd.sort_order, cd.sequence_number;

COMMIT;