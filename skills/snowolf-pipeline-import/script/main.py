# skills/snowolf-pipeline-import/script/main.py
from common import load_global_config, get_logger, PipelineContext, UpgradePlatformClient
from .env_parser import parse_env_arch
from .pipeline_creator import create_upgrade_pipeline

logger = get_logger("skill-pipeline-import")

def run_pipeline_import(ctx: PipelineContext):
    cfg = load_global_config()
    arch = parse_env_arch(ctx, cfg)
    client = UpgradePlatformClient()

    result = create_upgrade_pipeline(client, ctx.env_name, arch)
    ctx.pipeline_id = result["pipeline_id"]
    ctx.pipeline_name = result["pipeline_name"]
