from common.context import PipelineContext

def filter_upload_package(ctx: PipelineContext):
    # 根据上下文架构筛选待上传包
    return ctx.package_local_path
