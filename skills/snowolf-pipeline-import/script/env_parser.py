from common.context import PipelineContext

def parse_env_arch(ctx: PipelineContext, cfg: dict):
    env_data = cfg["environments"][ctx.env_name]
    return env_data["arch"]
