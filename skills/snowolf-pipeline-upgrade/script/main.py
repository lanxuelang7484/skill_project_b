from common import get_logger, PipelineContext, UpgradePlatformClient
from .upgrade_param_builder import build_upgrade_params
from .upgrade_trigger import trigger_upgrade_task

logger = get_logger("skill-upgrade")

def run_upgrade(ctx: PipelineContext):
    client = UpgradePlatformClient()
    pipeline_id = ctx.pipeline_id
    arch = ctx.arch
    env_name = ctx.env_name

    if not pipeline_id:
        raise RuntimeError("缺少pipeline_id，请先执行 snowolf-pipeline-import")

    # 根据环境、架构修改流水线升级参数配置
    client.modify_upgrade_config(pipeline_id, env_name, arch)
    params = build_upgrade_params(ctx)
    logger.info(f"正式升级参数：{params}")

    trigger_result = trigger_upgrade_task(client, pipeline_id, params)
    ctx.upgrade_build_id = trigger_result["build_id"]
    logger.info(f"正式升级build_id写入上下文：{ctx.upgrade_build_id}")
