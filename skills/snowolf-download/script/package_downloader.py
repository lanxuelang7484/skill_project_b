import os
from pathlib import Path

def download_package(base_path: str, version: str, arch: str, template: dict):
    filename = template[arch].format(version=version)
    save_path = Path(base_path) / filename
    os.makedirs(base_path, exist_ok=True)
    # 模拟下载逻辑，真实场景替换wget/requests下载
    with open(save_path, "w") as f:
        f.write(f"mock package {filename}")
    return str(save_path)
