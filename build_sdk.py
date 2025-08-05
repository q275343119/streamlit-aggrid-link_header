#!/usr/bin/env python3
"""
SDK打包脚本
用于构建Windows和HuggingFace环境的SDK包
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def print_step(message):
    """打印步骤信息"""
    print(f"\n{'='*50}")
    print(f"📦 {message}")
    print(f"{'='*50}")

def check_requirements():
    """检查构建要求"""
    print_step("检查构建要求")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8+")
        return False
    
    # 检查必要文件
    required_files = [
        "setup_windows.py",
        "setup_huggingface.py",
        "requirements_windows.txt",
        "requirements_huggingface.txt",
        "st_aggrid/link_header_builder.py",
        "st_aggrid/frontend/src/components/LinkHeaderComponent.tsx"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {missing_files}")
        return False
    
    print("✅ 构建要求检查通过")
    return True

def build_frontend():
    """构建前端代码"""
    print_step("构建前端代码")
    
    frontend_dir = Path("st_aggrid/frontend")
    if not frontend_dir.exists():
        print("❌ 前端目录不存在")
        return False
    
    try:
        # 检查Node.js
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ 未找到Node.js，请先安装Node.js")
            return False
        
        # 安装依赖
        print("📦 安装前端依赖...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, shell=True)
        
        # 构建前端
        print("🔨 构建前端代码...")
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True, shell=True)
        
        print("✅ 前端构建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 前端构建失败: {e}")
        return False

def build_windows_sdk():
    """构建Windows SDK"""
    print_step("构建Windows SDK")
    
    try:
        # 使用Windows配置构建
        subprocess.run([
            sys.executable, "setup_windows.py", "sdist", "bdist_wheel"
        ], check=True)
        
        print("✅ Windows SDK构建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows SDK构建失败: {e}")
        return False

def build_huggingface_sdk():
    """构建HuggingFace SDK"""
    print_step("构建HuggingFace SDK")
    
    try:
        # 使用HuggingFace配置构建
        subprocess.run([
            sys.executable, "setup_huggingface.py", "sdist", "bdist_wheel"
        ], check=True)
        
        print("✅ HuggingFace SDK构建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ HuggingFace SDK构建失败: {e}")
        return False

def create_package_structure():
    """创建打包结构"""
    print_step("创建打包结构")
    
    # 创建输出目录
    output_dir = Path("sdk_output")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    
    # Windows SDK目录
    windows_dir = output_dir / "windows"
    windows_dir.mkdir()
    
    # HuggingFace SDK目录
    huggingface_dir = output_dir / "huggingface"
    huggingface_dir.mkdir()
    
    # 复制文件到Windows目录
    windows_files = [
        "setup_windows.py",
        "requirements_windows.txt",
        "install_windows.bat",
        "README_SDK.md",
        "link_header_example.py",
        "test_link_header.py"
    ]
    
    for file in windows_files:
        if Path(file).exists():
            shutil.copy2(file, windows_dir)
    
    # 复制文件到HuggingFace目录
    huggingface_files = [
        "setup_huggingface.py",
        "requirements_huggingface.txt",
        "install_huggingface.sh",
        "README_SDK.md",
        "link_header_example.py",
        "test_link_header.py"
    ]
    
    for file in huggingface_files:
        if Path(file).exists():
            shutil.copy2(file, huggingface_dir)
    
    # 复制st_aggrid目录
    if Path("st_aggrid").exists():
        shutil.copytree("st_aggrid", windows_dir / "st_aggrid")
        shutil.copytree("st_aggrid", huggingface_dir / "st_aggrid")
    
    print("✅ 打包结构创建完成")
    return True

def create_install_scripts():
    """创建安装脚本"""
    print_step("创建安装脚本")
    
    # Windows安装脚本
    windows_install = """@echo off
echo 正在安装 Enhanced Streamlit AgGrid SDK (Windows版本)
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 创建虚拟环境
if not exist ".venv" (
    echo 创建虚拟环境...
    python -m venv .venv
)

REM 激活虚拟环境
call .venv\\Scripts\\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements_windows.txt

REM 安装SDK
echo 安装SDK...
pip install -e .

echo.
echo 安装完成！
echo 运行示例: streamlit run link_header_example.py
pause
"""
    
    # HuggingFace安装脚本
    huggingface_install = """#!/bin/bash
echo "正在安装 Enhanced Streamlit AgGrid SDK (HuggingFace版本)"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements_huggingface.txt

# 安装SDK
echo "安装SDK..."
pip install -e .

echo ""
echo "安装完成！"
echo "运行示例: streamlit run link_header_example.py"
"""
    
    # 写入文件
    with open("sdk_output/windows/install.bat", "w", encoding="utf-8") as f:
        f.write(windows_install)
    
    with open("sdk_output/huggingface/install.sh", "w", encoding="utf-8") as f:
        f.write(huggingface_install)
    
    # 设置执行权限
    os.chmod("sdk_output/huggingface/install.sh", 0o755)
    
    print("✅ 安装脚本创建完成")

def main():
    """主函数"""
    print("🚀 Enhanced Streamlit AgGrid SDK 打包工具")
    print("="*60)
    
    # 检查要求
    if not check_requirements():
        sys.exit(1)
    
    # 构建前端
    if not build_frontend():
        print("⚠️ 前端构建失败，但继续打包...")
    
    # 构建Windows SDK
    if not build_windows_sdk():
        print("⚠️ Windows SDK构建失败")
    
    # 构建HuggingFace SDK
    if not build_huggingface_sdk():
        print("⚠️ HuggingFace SDK构建失败")
    
    # 创建打包结构
    if not create_package_structure():
        sys.exit(1)
    
    # 创建安装脚本
    create_install_scripts()
    
    print_step("打包完成")
    print("📦 SDK包已生成在 sdk_output/ 目录下")
    print("")
    print("📁 目录结构:")
    print("  sdk_output/")
    print("  ├── windows/          # Windows环境SDK")
    print("  └── huggingface/      # HuggingFace环境SDK")
    print("")
    print("🚀 使用方法:")
    print("  1. 进入对应环境目录")
    print("  2. 运行安装脚本")
    print("  3. 运行示例程序")
    print("")
    print("✅ 打包完成！")

if __name__ == "__main__":
    main() 