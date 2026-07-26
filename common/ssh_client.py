import paramiko
from common.logger import get_logger
logger = get_logger("ssh-client")

class SshUploader:
    def __init__(self, host, port, user, pwd):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.ssh.connect(self.host, self.port, self.user, self.pwd)

    def upload_file(self, local_path, remote_path):
        sftp = self.ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        logger.info(f"上传完成 local:{local_path} -> remote:{remote_path}")

    def close(self):
        self.ssh.close()
