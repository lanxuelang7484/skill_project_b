# skill_project_b

启动示例（Windows cmd/PowerShell）
# 完整执行全部skill
python run_pipeline.py --env env-test-x86 --version 2.1.0

# 跳过下载，只执行上传及后续流程
python run_pipeline.py --env env-test-arm --version 2.1.0 --skip-download

# 跳过下载+上传，直接从创建流水线开始
python run_pipeline.py --env env-prod-x86 --version 2.1.0 --skip-download --skip-upload

# 流水线中断后断点续跑（无需传入 env、version）
python run_pipeline.py --resume
