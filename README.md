# Mailit - 命令行执行监控邮件通知工具
（README 由 LLM 生成，仅作说明用途）
## 简介

Mailit 是一个 Bash 命令包装工具，能够记录任何命令的输出和返回码，并在命令执行完成后通过电子邮件发送执行结果。特别适合监控长时间运行的脚本或定时任务。

## 功能特性

- 📧 自动发送命令执行结果到指定邮箱
- 📝 支持为命令添加说明备注
- ⏱️ 实时显示命令输出同时捕获结果
- 🔧 简单易用的配置向导
- 📊 包含完整执行上下文（命令、返回码、输出）

## 安装步骤

1. 将脚本保存到系统路径：

```bash
sudo curl -o /usr/local/bin/mailit_core.py https://raw.githubusercontent.com/Undermyth/mailit/main/mailit_core.py
sudo curl -o /usr/local/bin/mailit https://raw.githubusercontent.com/Undermyth/mailit/main/mailit
```

2. 设置执行权限：

```bash
sudo chmod +x /usr/local/bin/mailit
sudo chmod +x /usr/local/bin/mailit_core.py
```

3. 安装Python依赖（如果需要）：

```bash
pip install secure-smtplib
```

## 配置向导

首次使用前需要配置邮件服务器：

```bash
mailit --setup
```

按照提示输入以下信息：
- SMTP服务器地址（如 smtp.gmail.com）
- SMTP端口（通常 587）
- 邮箱账号和密码
- 发件人和收件人地址
- 是否使用TLS加密

配置将保存到 `~/.mailit_config`

## 使用示例

### 基本用法

```bash
mailit <command>
```

示例：
```bash
mailit ls -l /var/log
```

### 添加执行备注

```bash
mailit --note "备注信息" <command>
```

示例：
```bash
mailit --note "数据库备份任务" pg_dump mydb > backup.sql
```

### 使用自定义配置文件

```bash
mailit --config /path/to/config <command>
```

### 监控长时间运行的任务

```bash
mailit python long_running_script.py
```

### 监控管道操作

```bash
mailit "grep 'error' /var/log/syslog | wc -l"
```

## 邮件内容格式

收到的邮件将包含以下信息：

```
Command: 执行的完整命令
Exit Code: 返回状态码

Note: 用户添加的备注（如有）

Output:
命令的完整输出内容
```

## 高级配置

### 手动编辑配置文件

配置文件位于 `~/.mailit_config`，格式如下：

```
smtp_server=smtp.example.com
smtp_port=587
username=your@email.com
password=yourpassword
from_addr=your@email.com
to_addr=recipient@email.com
use_tls=true
```

### Gmail用户注意事项

如需使用Gmail：
1. 可能需要启用"允许不够安全的应用"
2. 建议使用应用专用密码而非主密码
3. SMTP服务器设为 `smtp.gmail.com`，端口587

## 安全性说明

- 配置文件包含敏感信息，建议设置权限：
  ```bash
  chmod 600 ~/.mailit_config
  ```
- 考虑使用加密密码管理器存储SMTP凭证
- 不建议在共享系统上使用明文密码配置
