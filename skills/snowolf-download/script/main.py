from common.config_loader import load_global_config
from common.logger import get_logger
from common.context import PipelineContext
from .arch_selector import get_target_arch
from .package_downloader import download_package

logger = get_logger("skill-download")

def run_download(ctx: PipelineContext):
    cfg = load_global_config()
    env_info = cfg["environments"][ctx.env_name]
    arch = get_target_arch(env_info)
    ctx.arch = arch
    logger.info(f"识别架构: {arch}")

    local_file = download_package(
        base_path=cfg["storage"]["base_download_path"],
        version=ctx.version,
        arch=arch,
        template=cfg["package_template"]
    )
    ctx.package_local_path = local_file
    logger.info(f"软件包下载完成，本地路径：{local_file}")
