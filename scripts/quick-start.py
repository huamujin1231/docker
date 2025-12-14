#!/usr/bin/env python3
"""
通用Docker项目快速启动脚本
支持跨平台使用 (Windows/Linux/Mac)
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class DockerManager:
    def __init__(self):
        self.system = platform.system()
        self.project_root = Path(__file__).parent.parent
        self.app_port = "5000"
        self.init_script = "docker-init.py"
        
    def run_command(self, cmd, capture_output=False):
        """执行命令"""
        try:
            if capture_output:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.project_root)
                return result.returncode == 0, result.stdout, result.stderr
            else:
                result = subprocess.run(cmd, shell=True, cwd=self.project_root)
                return result.returncode == 0
        except Exception as e:
            print(f"❌ 命令执行失败: {e}")
            return False
            
    def print_header(self):
        """显示标题"""
        print("=" * 40)
        print("    Docker 项目快速启动脚本")
        print("=" * 40)
        print()
        
    def print_menu(self):
        """显示菜单"""
        print("请选择操作:")
        print("[1] 🚀 启动项目 (构建+运行)")
        print("[2] 🔄 重新构建并启动")
        print("[3] 🛑 停止项目")
        print("[4] 📊 查看运行状态")
        print("[5] 📋 查看日志")
        print("[6] 🗄️  初始化数据库")
        print("[7] 💻 进入应用容器")
        print("[8] 🧹 清理所有容器和镜像")
        print("[0] 👋 退出")
        print()
        
    def start_project(self):
        """启动项目"""
        print("🚀 启动项目...")
        if self.run_command("docker-compose up -d"):
            print("✅ 项目启动成功！")
            print(f"🌐 访问地址: http://localhost:{self.app_port}")
        else:
            print("❌ 启动失败")
            
    def rebuild_project(self):
        """重新构建并启动"""
        print("🔄 重新构建并启动...")
        if self.run_command("docker-compose up --build -d"):
            print("✅ 重新构建成功！")
            print(f"🌐 访问地址: http://localhost:{self.app_port}")
        else:
            print("❌ 构建失败")
            
    def stop_project(self):
        """停止项目"""
        print("🛑 停止项目...")
        if self.run_command("docker-compose down"):
            print("✅ 项目已停止")
        else:
            print("❌ 停止失败")
            
    def show_status(self):
        """查看运行状态"""
        print("📊 查看运行状态...")
        self.run_command("docker-compose ps")
        
    def show_logs(self):
        """查看日志"""
        print("📋 查看日志 (按 Ctrl+C 退出)...")
        self.run_command("docker-compose logs -f")
        
    def init_database(self):
        """初始化数据库"""
        print("🗄️ 初始化数据库...")
        if self.run_command(f"docker-compose exec app python {self.init_script}"):
            print("✅ 数据库初始化成功")
        else:
            print("❌ 数据库初始化失败")
            
    def enter_shell(self):
        """进入应用容器"""
        print("💻 进入应用容器...")
        shell_cmd = "bash" if self.system != "Windows" else "sh"
        self.run_command(f"docker-compose exec app {shell_cmd}")
        
    def cleanup_all(self):
        """清理所有容器和镜像"""
        print("⚠️  警告: 这将删除所有相关的容器、镜像和数据卷！")
        confirm = input("确认删除? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            if self.run_command("docker-compose down -v --rmi all"):
                print("✅ 清理完成")
            else:
                print("❌ 清理失败")
        else:
            print("取消清理")
            
    def check_docker(self):
        """检查Docker是否安装"""
        success, _, _ = self.run_command("docker --version", capture_output=True)
        if not success:
            print("❌ Docker 未安装或未启动")
            return False
            
        success, _, _ = self.run_command("docker-compose --version", capture_output=True)
        if not success:
            print("❌ Docker Compose 未安装")
            return False
            
        return True
        
    def run(self):
        """主运行函数"""
        self.print_header()
        
        # 检查Docker环境
        if not self.check_docker():
            print("请先安装并启动 Docker 和 Docker Compose")
            return
            
        while True:
            self.print_menu()
            try:
                choice = input("请输入选项 (0-8): ").strip()
                
                if choice == "1":
                    self.start_project()
                elif choice == "2":
                    self.rebuild_project()
                elif choice == "3":
                    self.stop_project()
                elif choice == "4":
                    self.show_status()
                elif choice == "5":
                    self.show_logs()
                elif choice == "6":
                    self.init_database()
                elif choice == "7":
                    self.enter_shell()
                elif choice == "8":
                    self.cleanup_all()
                elif choice == "0":
                    print("👋 再见！")
                    break
                else:
                    print("❌ 无效选项，请重新选择")
                    
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                
            print()
            input("按回车键继续...")
            print()

if __name__ == "__main__":
    manager = DockerManager()
    manager.run()