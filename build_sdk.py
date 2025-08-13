#!/usr/bin/env python3
"""
Streamlit AgGrid SDK 快速构建脚本
"""

import subprocess
import sys
from pathlib import Path
import shutil
import platform


def run_cmd(cmd, cwd=None, timeout=300):
    """运行命令"""
    try:
        use_shell = platform.system() == "Windows"
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            shell=use_shell,
            timeout=timeout,
            capture_output=True,
            text=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"命令失败: {e}\n{e.stderr}"
    except subprocess.TimeoutExpired:
        return False, f"命令超时: {' '.join(cmd)}"
    except Exception as e:
        return False, f"异常: {e}"


def build_frontend():
    """构建前端"""
    frontend_dir = Path("st_aggrid/frontend")
    if not frontend_dir.exists():
        print("⚠️ 前端目录不存在，跳过前端构建")
        return True

    # 检查Node.js
    success, output = run_cmd(["node", "--version"])
    if not success:
        print("⚠️ Node.js不可用，跳过前端构建")
        return True

    print(f"📦 Node.js: {output.strip()}")

    # 选择包管理器
    if (frontend_dir / "yarn.lock").exists():
        install_cmd = ["yarn", "install"]
        build_cmd = ["yarn", "build"]
        pkg_mgr = "yarn"
    else:
        install_cmd = ["npm", "install"]
        build_cmd = ["npm", "run", "build"]
        pkg_mgr = "npm"

    print(f"🔧 使用 {pkg_mgr} 构建前端...")

    # 安装依赖
    success, output = run_cmd(install_cmd, cwd=frontend_dir, timeout=300)
    if not success:
        print(f"❌ 依赖安装失败: {output}")
        return False

    # 构建
    success, output = run_cmd(build_cmd, cwd=frontend_dir, timeout=600)
    if not success:
        print(f"❌ 前端构建失败: {output}")
        return False

    print("✅ 前端构建完成")
    return True


def build_python():
    """构建Python包"""
    print("🔧 构建Python包...")

    # 准备dist目录
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # 尝试PEP 517构建
    success, output = run_cmd([sys.executable, "-m", "pip", "install", "-U", "build"])
    if success:
        success, output = run_cmd([sys.executable, "-m", "build"])
        if success:
            print("✅ Python包构建完成 (PEP 517)")
            return True

    # 回退到setup.py
    if Path("setup.py").exists():
        success, output = run_cmd([sys.executable, "setup.py", "bdist_wheel"])
        if success:
            print("✅ Python包构建完成 (setup.py)")
            return True

    print(f"❌ Python包构建失败: {output}")
    return False


def main():
    """主函数"""
    print("🚀 Streamlit AgGrid SDK 快速构建")
    print("=" * 40)

    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8+")
        sys.exit(1)

    print(f"✅ Python: {sys.version.split()[0]}")

    # 构建前端
    if "--skip-frontend" not in sys.argv:
        if not build_frontend():
            if "--strict" in sys.argv:
                sys.exit(1)
            print("⚠️ 前端构建失败，继续Python包构建...")
    else:
        print("⏭️ 跳过前端构建")

    # 构建Python包
    if "--skip-python" not in sys.argv:
        if not build_python():
            sys.exit(1)
    else:
        print("⏭️ 跳过Python包构建")

    # 显示结果
    wheels = list(Path("dist").glob("*.whl"))
    if wheels:
        print(f"\n🎉 构建完成! 生成了 {len(wheels)} 个文件:")
        for wheel in wheels:
            print(f"  📦 {wheel.name}")
    else:
        print("\n⚠️ 未找到生成的wheel文件")


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
用法: python build_sdk.py [选项]

选项:
  --skip-frontend    跳过前端构建
  --skip-python      跳过Python包构建
  --strict           前端构建失败时停止
  --help, -h         显示帮助

示例:
  python build_sdk.py                 # 完整构建
  python build_sdk.py --skip-frontend # 只构建Python包
        """)
        sys.exit(0)

    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ 构建被中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 构建失败: {e}")
        sys.exit(1)
