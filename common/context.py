from dataclasses import dataclass, field
from typing import Optional, Dict

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
