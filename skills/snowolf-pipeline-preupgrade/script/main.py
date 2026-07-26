from common import get_logger, PipelineContext, UpgradePlatformClient
from .preupgrade_config import build_preupgrade_params
from .pipeline_trigger import trigger_preupgrade_task

logger = get_logger("skill-preupgrade")

def run_preupgrade(ctx: PipelineContext):
    client = UpgradePlatformClient()
    arch = ctx.arch
    pipeline_id = ctx.pipeline_id

    if not pipeline_id:
        raise RuntimeError("缺少pipeline_id，请先执行 snowolf-pipeline-import")

    # 根据架构修改流水线预升级配置
    client.modify_preupgrade_config(pipeline_id, arch)
    params = build_preupgrade_params(ctx)

    trigger_result = trigger_preupgrade_task(client, pipeline_id, params)
    ctx.preupgrade_build_id = trigger_result["build_id"]
    logger.info(f"预升级build_id已写入上下文：{ctx.preupgrade_build_id}")
