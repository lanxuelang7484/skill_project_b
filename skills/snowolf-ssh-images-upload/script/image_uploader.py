from pathlib import Path
from common import SshUploader, get_logger

logger = get_logger("uploader-core")

def upload_package(
    ssh_host: str,
    ssh_port: int,
    ssh_user: str,
    ssh_pwd: str,
    local_file_path: str,
    remote_base_dir: str
) -> str:
    """
    通过SSH/SFTP上传制品包
    :param ssh_host: 目标主机IP
    :param ssh_port: SSH端口
    :param ssh_user: 用户名
    :param ssh_pwd: 密码
    :param local_file_path: 本地文件完整路径
    :param remote_base_dir: 远端存放根目录
    :return: 远端完整文件路径
    """
    local_path = Path(local_file_path)
    filename = local_path.name
    remote_full_path = str(Path(remote_base_dir) / filename)

    logger.info(f"准备上传：本地[{local_file_path}] -> 远端[{remote_full_path}]")
    uploader = SshUploader(
        host=ssh_host,
        port=ssh_port,
        user=ssh_user,
        pwd=ssh_pwd
    )
    try:
        uploader.connect()
        uploader.upload_file(str(local_path), remote_full_path)
        logger.info("文件上传成功")
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}", exc_info=True)
        raise
    finally:
        uploader.close()

    return remote_full_path
