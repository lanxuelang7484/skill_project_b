from common import UpgradePlatformClient, get_logger

logger = get_logger("preupgrade-trigger")

def trigger_preupgrade_task(client: UpgradePlatformClient, pipeline_id: str, run_params: dict) -> dict:
    """
    触发预升级流水线任务
    :param client: 升级平台API客户端
    :param pipeline_id: 目标流水线ID
    :param run_params: 预升级运行参数
    :return: {"build_id": "任务唯一标识"}
    """
    logger.info(f"准备触发预升级流水线 pipeline_id={pipeline_id}")
    logger.debug(f"预升级传入参数: {run_params}")

    resp = client.trigger_preupgrade(pipeline_id)
    build_id = resp.get("build_id")

    if not build_id:
        raise RuntimeError(f"预升级任务触发失败，接口未返回build_id，原始响应:{resp}")

    logger.info(f"预升级任务触发成功，build_id = {build_id}")
    return {"build_id": build_id}
