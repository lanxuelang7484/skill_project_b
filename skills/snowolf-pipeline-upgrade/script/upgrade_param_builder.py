from common.context import PipelineContext

def build_upgrade_params(ctx: PipelineContext):
    return {
        "env_name": ctx.env_name,
        "arch": ctx.arch,
        "version": ctx.version,
        "package_remote_path": ctx.remote_package_path
    }
