import requests
from common.config_loader import load_global_config
from common.logger import get_logger

logger = get_logger("platform-api")
cfg = load_global_config()

class UpgradePlatformClient:
    def __init__(self):
        self.base_url = cfg["platform"]["api_url"]
        self.username = cfg["platform"]["username"]
        self.password = cfg["platform"]["password"]
        self.session = requests.Session()

    def create_pipeline(self, env_name, arch):
        """创建流水线"""
        # 模拟API调用
        logger.info(f"创建流水线 env={env_name}, arch={arch}")
        return {"pipeline_id": f"pipe-{env_name}-{arch}-123456", "pipeline_name": f"Snowolf-{env_name}-upgrade"}

    def modify_preupgrade_config(self, pipeline_id, arch):
        """修改预升级配置"""
        logger.info(f"预升级配置更新 pipeline={pipeline_id}, arch={arch}")
        return True

    def trigger_preupgrade(self, pipeline_id):
        logger.info(f"触发预升级 pipeline={pipeline_id}")
        return {"build_id": f"pre-{pipeline_id}-run01"}

    def query_build_status(self, build_id):
        """查询构建状态：success/failed/timeout/running"""
        # 模拟轮询接口
        return {"status": "success"}

    def modify_upgrade_config(self, pipeline_id, env_name, arch):
        logger.info(f"正式升级参数配置 pipeline={pipeline_id}")
        return True

    def trigger_upgrade(self, pipeline_id):
        logger.info(f"触发正式升级 pipeline={pipeline_id}")
        return {"build_id": f"upgrade-{pipeline_id}-run01"}
