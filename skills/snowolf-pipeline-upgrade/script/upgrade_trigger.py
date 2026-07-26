from common import UpgradePlatformClient, get_logger

logger = get_logger("upgrade-trigger")

def trigger_upgrade_task(client: UpgradePlatformClient, pipeline_id: str, run_params: dict) -> dict:
    """
    触发正式服务升级流水线任务
    :param client: 平台API客户端实例
    :param pipeline_id: 流水线唯一ID
    :param run_params: 升级运行入参
    :return: {"build_id": "升级任务唯一编号"}
    """
    logger.info(f"准备触发正式升级流水线 pipeline_id={pipeline_id}")
    logger.debug(f"正式升级传入参数：{run_params}")

    resp = client.trigger_upgrade(pipeline_id)
    build_id = resp.get("build_id")

    if not build_id:
        raise RuntimeError(f"正式升级任务触发失败，接口未返回build_id，原始响应：{resp}")

    logger.info(f"正式升级任务触发成功，build_id = {build_id}")
    return {"build_id": build_id}
