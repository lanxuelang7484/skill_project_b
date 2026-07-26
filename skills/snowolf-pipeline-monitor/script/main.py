import time
from common.config_loader import load_global_config
from common.logger import get_logger
from common.context import PipelineContext
from common.platform_api import UpgradePlatformClient
from .status_poller import poll_status

logger = get_logger("skill-monitor")

def run_monitor(ctx: PipelineContext, monitor_type: str):
    cfg = load_global_config()
    interval = cfg["monitor"]["poll_interval"]
    max_wait = cfg["monitor"]["max_wait_seconds"]
    client = UpgradePlatformClient()

    if monitor_type == "preupgrade":
        build_id = ctx.preupgrade_build_id
    elif monitor_type == "upgrade":
        build_id = ctx.upgrade_build_id
    else:
        raise Exception("monitor_type 非法")

    logger.info(f"开始轮询监控 {monitor_type} build_id={build_id}")
    result = poll_status(client, build_id, interval, max_wait)
    logger.info(f"{monitor_type}监控结果：{result}")
    return result
