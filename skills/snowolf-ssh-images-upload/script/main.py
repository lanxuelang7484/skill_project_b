# skills/snowolf-ssh-images-upload/script/main.py
from common import load_global_config, get_logger, PipelineContext
from .arch_filter import filter_upload_package
from .image_uploader import upload_package

logger = get_logger("skill-upload")

def run_upload(ctx: PipelineContext):
    cfg = load_global_config()
    env_info = cfg["environments"][ctx.env_name]
    local_file = filter_upload_package(ctx)

    remote_base = "/data/package"
    remote_path = upload_package(
        ssh_host=env_info["ssh_host"],
        ssh_port=env_info["ssh_port"],
        ssh_user=env_info["ssh_user"],
        ssh_pwd=env_info["ssh_pwd"],
        local_file_path=local_file,
        remote_base_dir=remote_base
    )

    ctx.remote_package_path = remote_path
    logger.info(f"镜像上传完成，远端路径：{remote_path}")
