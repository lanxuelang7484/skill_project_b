# skills/snowolf-pipeline-import/script/pipeline_creator.py
from common import UpgradePlatformClient, get_logger

logger = get_logger("pipeline-creator")

def create_upgrade_pipeline(client: UpgradePlatformClient, env_name: str, arch: str) -> dict:
    """
    调用升级平台API，根据环境与架构导入/创建流水线
    :param client: 平台API实例
    :param env_name: 环境标识(env-test-x86/env-test-arm)
    :param arch: 架构 x86_64 / arm64
    :return: dict {pipeline_id, pipeline_name}
    """
    logger.info(f"开始创建流水线，环境：{env_name}，架构：{arch}")
    resp = client.create_pipeline(env_name, arch)

    pipeline_id = resp.get("pipeline_id")
    pipeline_name = resp.get("pipeline_name")

    if not pipeline_id:
        raise RuntimeError(f"流水线创建失败，接口未返回pipeline_id，响应：{resp}")

    logger.info(f"流水线创建成功 >> ID:{pipeline_id}, Name:{pipeline_name}")
    return {
        "pipeline_id": pipeline_id,
        "pipeline_name": pipeline_name
    }
