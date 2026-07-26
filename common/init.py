# common/__init__.py
"""
公共工具包统一导出入口
供外部简洁导入，统一模块访问规范
"""

# 导出核心类与函数，上层代码不用深层import
from .context import PipelineContext
from .logger import get_logger
from .config_loader import load_global_config
from .ssh_client import SshUploader
from .platform_api import UpgradePlatformClient
from .checkpoint_const import (
    STEP_INIT,
    STEP_DOWNLOAD,
    STEP_UPLOAD,
    STEP_PIPELINE_IMPORT,
    STEP_PREUPGRADE,
    STEP_MONITOR_PRE,
    STEP_UPGRADE,
    STEP_MONITOR_UPGRADE,
    STEP_FINISH,
    STEP_ORDER
)

# 包版本标识（可选）
__version__ = "1.0.0"
