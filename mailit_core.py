#!/usr/bin/env python3
import sys
import subprocess
import smtplib
from email.mime.text import MIMEText
from os.path import expanduser
import os
import argparse

def get_default_config():
    """获取默认配置文件路径"""
    return os.path.join(expanduser("~"), ".mailit_config")

def load_config(config_file):
    """加载邮件配置"""
    config = {
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'username': 'your_email@example.com',
        'password': 'your_password',
        'from_addr': 'your_email@example.com',
        'to_addr': 'recipient@example.com',
        'use_tls': True
    }
    
    if os.path.exists(config_file):
        with open(config_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config

def send_email(subject, body, config):
    """发送邮件"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config['from_addr']
    msg['To'] = config['to_addr']
    
    try:
        with smtplib.SMTP(config['smtp_server'], int(config['smtp_port'])) as server:
            if config.get('use_tls', 'True').lower() == 'true':
                server.starttls()
            server.login(config['username'], config['password'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}", file=sys.stderr)
        return False

def run_command_with_mail(cmd, config_file=None, note=None):
    if not cmd:
        print("Error: No command provided", file=sys.stderr)
        return 1

    config = load_config(config_file or get_default_config())
    
    try:
        process = subprocess.Popen(
            cmd,
            shell=True if isinstance(cmd, str) else False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1  # 行缓冲
        )
        
        # 实时输出+捕获
        output_lines = []
        for line in process.stdout:
            print(line, end='')  # 实时打印到终端
            output_lines.append(line)
        
        return_code = process.wait()
        output = ''.join(output_lines)
        
        # 邮件发送逻辑（保持原样）
        subject = f"Command {'succeeded' if return_code == 0 else 'failed'}: {' '.join(cmd) if isinstance(cmd, list) else cmd}"
        body = f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}\nExit Code: {return_code}"
        if note:
            body += f"\nNote: {note}"
        body += f"\n\nOutput:\n{output}"
        
        send_email(subject, body, config)
        return return_code
        
    except Exception as e:
        error_msg = f"Error executing command: {e}"
        send_email("Command execution failed", error_msg, config)
        print(error_msg, file=sys.stderr)
        return 1

def setup_config():
    """交互式配置设置"""
    config_file = get_default_config()
    print(f"Creating mailit configuration file at {config_file}")
    
    config = {
        'smtp_server': input("SMTP Server [smtp.example.com]: ") or 'smtp.example.com',
        'smtp_port': input("SMTP Port [587]: ") or '587',
        'username': input("Email Username: "),
        'password': input("Email Password: "),
        'from_addr': input("From Address: "),
        'to_addr': input("To Address: "),
        'use_tls': input("Use TLS? [Y/n]: ").lower() in ('', 'y', 'yes')
    }
    
    with open(config_file, 'w') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    print(f"Configuration saved to {config_file}")
    print("You may need to configure your email provider to allow less secure apps if using Gmail etc.")

def main():
    parser = argparse.ArgumentParser(description='Run a command and mail its output')
    parser.add_argument('--setup', action='store_true', help='Setup mail configuration')
    parser.add_argument('--config', help='Path to custom config file')
    parser.add_argument('--note', default='', help='Additional note to include in the email')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Command to execute')
    
    args = parser.parse_args()
    
    if args.setup:
        setup_config()
        return 0
    
    if not args.command:
        parser.print_help()
        return 1
    
    return run_command_with_mail(args.command, args.config, args.note)

if __name__ == '__main__':
    sys.exit(main())
