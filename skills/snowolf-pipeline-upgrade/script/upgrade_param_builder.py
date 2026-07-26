from common import PipelineContext

def build_upgrade_params(ctx: PipelineContext) -> dict:
    """组装正式升级运行参数"""
    return {
        "env_name": ctx.env_name,
        "arch": ctx.arch,
        "version": ctx.version,
        "remote_package_path": ctx.remote_package_path
    }
