from common.config_loader import load_global_config
from common.logger import get_logger
from common.context import PipelineContext
from common.ssh_client import SshUploader
from .arch_filter import filter_upload_package

logger = get_logger("skill-upload")

def run_upload(ctx: PipelineContext):
    cfg = load_global_config()
    env_info = cfg["environments"][ctx.env_name]
    local_file = filter_upload_package(ctx)

    ssh = SshUploader(
        host=env_info["ssh_host"],
        port=env_info["ssh_port"],
        user=env_info["ssh_user"],
        pwd=env_info["ssh_pwd"]
    )
    ssh.connect()
    remote_path = f"/data/package/{Path(local_file).name}"
    ssh.upload_file(local_file, remote_path)
    ssh.close()

    ctx.remote_package_path = remote_path
    logger.info(f"镜像上传完成，远端路径：{remote_path}")
