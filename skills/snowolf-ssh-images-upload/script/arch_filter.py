# skills/snowolf-ssh-images-upload/script/arch_filter.py
from common import PipelineContext

def filter_upload_package(ctx: PipelineContext) -> str:
    """
    根据上下文架构筛选待上传包
    支持扩展：比如按架构名称过滤、校验文件是否存在
    """
    local_path = ctx.package_local_path
    if not local_path:
        raise RuntimeError("待上传本地包路径为空，请先执行 snowolf-download")
    return local_path
