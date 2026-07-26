from common.logger import get_logger
from common.context import PipelineContext
from common.platform_api import UpgradePlatformClient
from .preupgrade_config import build_preupgrade_params

logger = get_logger("skill-preupgrade")

def run_preupgrade(ctx: PipelineContext):
    client = UpgradePlatformClient()
    arch = ctx.arch
    pipeline_id = ctx.pipeline_id

    # 根据架构修改预升级配置
    client.modify_preupgrade_config(pipeline_id, arch)
    params = build_preupgrade_params(ctx)
    logger.info(f"预升级参数组装完成 {params}")

    trigger_resp = client.trigger_preupgrade(pipeline_id)
    ctx.preupgrade_build_id = trigger_resp["build_id"]
    logger.info(f"预升级任务已触发 build_id={ctx.preupgrade_build_id}")
