import argparse
from common.context import PipelineContext
from common.logger import get_logger
from skills.snowolf_download.script.main import run_download
from skills.snowolf_ssh_images_upload.script.main import run_upload
from skills.snowolf_pipeline_import.script.main import run_pipeline_import
from skills.snowolf_pipeline_preupgrade.script.main import run_preupgrade
from skills.snowolf_pipeline_monitor.script.main import run_monitor
from skills.snowolf_pipeline_upgrade.script.main import run_upgrade

logger = get_logger("pipeline-scheduler")

def main():
    parser = argparse.ArgumentParser(description="Snowolf自动化升级流水线调度器")
    parser.add_argument("--env", required=True, help="环境名称 env-test-x86/env-test-arm")
    parser.add_argument("--version", required=True, help="软件版本号")
    parser.add_argument("--skip-download", action="store_true", help="跳过下载skill")
    parser.add_argument("--skip-upload", action="store_true", help="跳过镜像上传skill")
    args = parser.parse_args()

    # 初始化上下文
    ctx = PipelineContext(
        env_name=args.env,
        version=args.version,
        skip_download=args.skip_download,
        skip_upload=args.skip_upload
    )
    logger.info(f"=====流水线启动 env={ctx.env_name}, version={ctx.version}=====")

    try:
        # 1. snowolf-download
        if not ctx.skip_download:
            logger.info(">>> 执行 snowolf-download")
            run_download(ctx)
        else:
            logger.info(">>> 跳过 snowolf-download")

        # 2. snowolf-ssh-images-upload
        if not ctx.skip_upload:
            logger.info(">>> 执行 snowolf-ssh-images-upload")
            run_upload(ctx)
        else:
            logger.info(">>> 跳过 snowolf-ssh-images-upload")

        # 3. snowolf-pipeline-import【必选不可跳过】
        logger.info(">>> 执行 snowolf-pipeline-import")
        run_pipeline_import(ctx)

        # 4. snowolf-pipeline-preupgrade【必选】
        logger.info(">>> 执行 snowolf-pipeline-preupgrade")
        run_preupgrade(ctx)

        # 5. monitor 监控预升级
        logger.info(">>> 执行 snowolf-pipeline-monitor【预升级监控】")
        monitor_result = run_monitor(ctx, monitor_type="preupgrade")
        if monitor_result != "success":
            raise Exception(f"预升级执行结果:{monitor_result}，需要人工介入，流水线终止")

        # 6. snowolf-pipeline-upgrade【必选】
        logger.info(">>> 执行 snowolf-pipeline-upgrade")
        run_upgrade(ctx)

        # 7. monitor 监控正式升级
        logger.info(">>> 执行 snowolf-pipeline-monitor【正式升级监控】")
        monitor_result = run_monitor(ctx, monitor_type="upgrade")
        if monitor_result != "success":
            raise Exception(f"正式升级执行结果:{monitor_result}，需要人工介入，流水线终止")

        logger.info("=====✅整条自动化升级流水线全部执行完成=====")

    except Exception as e:
        logger.error(f"流水线异常终止：{str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
