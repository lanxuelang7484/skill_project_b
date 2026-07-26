from common import PipelineContext

def build_preupgrade_params(ctx: PipelineContext) -> dict:
    """组装预升级运行参数"""
    return {
        "env": ctx.env_name,
        "arch": ctx.arch,
        "package_remote_path": ctx.remote_package_path,
        "version": ctx.version
    }
