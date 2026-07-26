import argparse
from pathlib import Path
from common.context import PipelineContext
from common.logger import get_logger
from common.config_loader import load_global_config
from common.checkpoint_const import (
    STEP_ORDER,
    STEP_DOWNLOAD, STEP_UPLOAD, STEP_PIPELINE_IMPORT,
    STEP_PREUPGRADE, STEP_MONITOR_PRE, STEP_UPGRADE, STEP_MONITOR_UPGRADE, STEP_FINISH
)
from skills.snowolf_download.script.main import run_download
from skills.snowolf_ssh_images_upload.script.main import run_upload
from skills.snowolf_pipeline_import.script.main import run_pipeline_import
from skills.snowolf_pipeline_preupgrade.script.main import run_preupgrade
from skills.snowolf_pipeline_monitor.script.main import run_monitor
from skills.snowolf_pipeline_upgrade.script.main import run_upgrade

logger = get_logger("pipeline-scheduler")
BASE_DIR = Path(__file__).parent

def main():
    parser = argparse.ArgumentParser(description="Snowolf自动化升级流水线调度器【支持断点续跑】")
    parser.add_argument("--env", help="环境名称 env-test-x86/env-test-arm（新建流水线必填，续跑忽略）")
    parser.add_argument("--version", help="软件版本号（新建流水线必填，续跑忽略）")
    parser.add_argument("--skip-download", action="store_true", help="跳过下载skill（新建流水线生效）")
    parser.add_argument("--skip-upload", action="store_true", help="跳过镜像上传skill（新建流水线生效）")
    parser.add_argument("--resume", action="store_true", help="断点续跑，从pipeline_breakpoint.json加载上下文")
    args = parser.parse_args()

    cfg = load_global_config()
    checkpoint_path = BASE_DIR / cfg["checkpoint"]["checkpoint_filename"]
    ctx: PipelineContext

    # 分支：新建流水线 / 断点续跑
    if args.resume:
        logger.info(f"=====开启断点续跑，加载断点文件: {checkpoint_path}=====")
        ctx = PipelineContext.load_checkpoint(checkpoint_path)
        logger.info(f"当前断点位置：{ctx.checkpoint_step}")
    else:
        if not args.env or not args.version:
            raise Exception("新建流水线必须传入 --env 和 --version")
        logger.info(f"=====全新流水线启动 env={args.env}, version={args.version}=====")
        ctx = PipelineContext(
            env_name=args.env,
            version=args.version,
            skip_download=args.skip_download,
            skip_upload=args.skip_upload,
            checkpoint_step=STEP_INIT
        )
        ctx.save_checkpoint(checkpoint_path)

    try:
        # 1. snowolf-download
        if ctx.checkpoint_step < STEP_DOWNLOAD:
            if not ctx.skip_download:
                logger.info(">>> 执行 snowolf-download")
                run_download(ctx)
            else:
                logger.info(">>> 跳过 snowolf-download")
            ctx.checkpoint_step = STEP_DOWNLOAD
            ctx.save_checkpoint(checkpoint_path)

        # 2. snowolf-ssh-images-upload
        if ctx.checkpoint_step < STEP_UPLOAD:
            if not ctx.skip_upload:
                logger.info(">>> 执行 snowolf-ssh-images-upload")
                run_upload(ctx)
            else:
                logger.info(">>> 跳过 snowolf-ssh-images-upload")
            ctx.checkpoint_step = STEP_UPLOAD
            ctx.save_checkpoint(checkpoint_path)

        # 3. snowolf-pipeline-import
        if ctx.checkpoint_step < STEP_PIPELINE_IMPORT:
            logger.info(">>> 执行 snowolf-pipeline-import")
            run_pipeline_import(ctx)
            ctx.checkpoint_step = STEP_PIPELINE_IMPORT
            ctx.save_checkpoint(checkpoint_path)

        # 4. snowolf-pipeline-preupgrade
        if ctx.checkpoint_step < STEP_PREUPGRADE:
            logger.info(">>> 执行 snowolf-pipeline-preupgrade")
            run_preupgrade(ctx)
            ctx.checkpoint_step = STEP_PREUPGRADE
            ctx.save_checkpoint(checkpoint_path)

        # 5. monitor 预升级监控
        if ctx.checkpoint_step < STEP_MONITOR_PRE:
            logger.info(">>> 执行 snowolf-pipeline-monitor【预升级监控】")
            monitor_result = run_monitor(ctx, monitor_type="preupgrade")
            if monitor_result != "success":
                raise Exception(f"预升级执行结果:{monitor_result}，需要人工介入，流水线终止")
            ctx.checkpoint_step = STEP_MONITOR_PRE
            ctx.save_checkpoint(checkpoint_path)

        # 6. snowolf-pipeline-upgrade
        if ctx.checkpoint_step < STEP_UPGRADE:
            logger.info(">>> 执行 snowolf-pipeline-upgrade")
            run_upgrade(ctx)
            ctx.checkpoint_step = STEP_UPGRADE
            ctx.save_checkpoint(checkpoint_path)

        # 7. monitor 正式升级监控
        if ctx.checkpoint_step < STEP_MONITOR_UPGRADE:
            logger.info(">>> 执行 snowolf-pipeline-monitor【正式升级监控】")
            monitor_result = run_monitor(ctx, monitor_type="upgrade")
            if monitor_result != "success":
                raise Exception(f"正式升级执行结果:{monitor_result}，需要人工介入，流水线终止")
            ctx.checkpoint_step = STEP_MONITOR_UPGRADE
            ctx.save_checkpoint(checkpoint_path)

        # 全部流程完成
        ctx.checkpoint_step = STEP_FINISH
        logger.info("=====✅整条自动化升级流水线全部执行完成=====")
        if cfg["checkpoint"]["auto_clean_on_finish"] and checkpoint_path.exists():
            checkpoint_path.unlink()
            logger.info(f"流水线执行完毕，自动清理断点文件 {checkpoint_path}")

    except Exception as e:
        logger.error(f"流水线异常终止：{str(e)}", exc_info=True)
        logger.warning(f"断点已保存至 {checkpoint_path}，修复问题后执行：python run_pipeline.py --resume 恢复运行")
        raise

if __name__ == "__main__":
    main()
