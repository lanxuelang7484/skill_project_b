from common.logger import get_logger
from common.context import PipelineContext
from common.platform_api import UpgradePlatformClient
from .upgrade_param_builder import build_upgrade_params

logger = get_logger("skill-upgrade")

def run_upgrade(ctx: PipelineContext):
    client = UpgradePlatformClient()
    pipeline_id = ctx.pipeline_id
    arch = ctx.arch
    env_name = ctx.env_name

    client.modify_upgrade_config(pipeline_id, env_name, arch)
    params = build_upgrade_params(ctx)
    logger.info(f"正式升级参数：{params}")

    trigger_resp = client.trigger_upgrade(pipeline_id)
    ctx.upgrade_build_id = trigger_resp["build_id"]
    logger.info(f"正式升级任务触发 build_id={ctx.upgrade_build_id}")
