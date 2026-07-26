from common import PipelineContext

def parse_env_arch(ctx: PipelineContext, cfg: dict):
    """从全局配置读取当前环境对应的架构信息"""
    env_data = cfg["environments"].get(ctx.env_name)
    if not env_data:
        raise KeyError(f"global_config.yaml 不存在环境配置：{ctx.env_name}")
    return env_data["arch"]
