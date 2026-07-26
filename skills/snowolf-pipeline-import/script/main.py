from common.config_loader import load_global_config
from common.logger import get_logger
from common.context import PipelineContext
from common.platform_api import UpgradePlatformClient
from .env_parser import parse_env_arch

logger = get_logger("skill-pipeline-import")

def run_pipeline_import(ctx: PipelineContext):
    cfg = load_global_config()
    arch = parse_env_arch(ctx, cfg)
    client = UpgradePlatformClient()
    resp = client.create_pipeline(ctx.env_name, arch)
    ctx.pipeline_id = resp["pipeline_id"]
    ctx.pipeline_name = resp["pipeline_name"]
    logger.info(f"流水线创建成功 ID={ctx.pipeline_id}, name={ctx.pipeline_name}")
