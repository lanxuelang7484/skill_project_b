from common.context import PipelineContext

def build_preupgrade_params(ctx: PipelineContext):
    return {
        "env": ctx.env_name,
        "arch": ctx.arch,
        "package_path": ctx.remote_package_path
    }
