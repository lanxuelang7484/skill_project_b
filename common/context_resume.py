from dataclasses import dataclass, field, asdict
from typing import Optional, Dict
import json
from pathlib import Path

@dataclass
class PipelineContext:
    # 入参
    env_name: str
    version: str
    skip_download: bool = False
    skip_upload: bool = False

    # snowolf-download 输出
    package_local_path: Optional[str] = None
    arch: Optional[str] = None

    # snowolf-ssh-images-upload 输出
    remote_package_path: Optional[str] = None

    # snowolf-pipeline-import 输出
    pipeline_id: Optional[str] = None
    pipeline_name: Optional[str] = None

    # preupgrade输出
    preupgrade_build_id: Optional[str] = None

    # upgrade输出
    upgrade_build_id: Optional[str] = None

    # 全局缓存
    extra_data: Dict = field(default_factory=dict)

    # 断点标记：记录当前执行点位
    checkpoint_step: str = "init"

    def to_dict(self):
        """转为可序列化字典"""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict):
        """从字典恢复实例"""
        return PipelineContext(**data)

    def save_checkpoint(self, checkpoint_file: Path):
        """保存断点文件"""
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_checkpoint(checkpoint_file: Path):
        """加载断点文件"""
        if not checkpoint_file.exists():
            raise FileNotFoundError(f"断点文件不存在: {checkpoint_file}")
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return PipelineContext.from_dict(data)
