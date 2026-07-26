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



目标：我只有一台windows server 2019主机，里面安装了pycharm和python环境，要求在OpenClaw下自定义多个skill串联实现完成产品版本自动化流水线升级业务服务。
要求：
1.在这个主机上模拟创建snowolf-download、snowolf-ssh-images-upload、snowolf-pipeline-import、snowolf-pipeline-preupgrade、snowolf-pipeline-monitor、snowolf-pipeline-upgrade六个skill，各个skill完成各自的功能任务。
(1)snowolf-download自定义自动下载软件包（区分 arm 和 x86 架构）
(2)snowolf-ssh-images-upload自动上传镜像包（区分 arm 和 x86 架构）
(3)snowolf-pipeline-import自动根据不同环境信息导入创建升级流水线
(4)snowolf-pipeline-preupgrade预升级处理，自动匹配获取(3)输出的流水线id名称，能够自动根据不同架构对创建出来的流水线做预升级配置修改并运行
(5)snowolf-pipeline-monitor实时监控预升级流水线运行状态并返回结果，返回 “成功” 进入下一步进行；返回 “失败” 或 “超时”，提示要人工介入处理
(6)snowolf-pipeline-upgrade升级处理，自动根据不同环境名、不同架构对(4)修改后的流水线做服务升级参数配置修改并运行
(7)snowolf-pipeline-monitor实时监控流水线升级运行状态并返回结果，返回 “成功” 进入下一步进行；返回 “失败” 或 “超时”，提示要人工介入处理
2.这六个skill下script目录下一般会有2-4个python脚本，帮我模拟并生成这些脚本，其中一个为main.py作为该skill入口脚本，其他脚本是实现该skill功能模块。
3.有一个global_config.yaml公共配置文件用于索引不同环境信息（区分不同架构）、平台访问地址、平台用户名、平台密码、下载包路径等公共配置信息，六个skill在运行的时候都要加载这些公共配置，禁止硬编码
4.帮忙模拟创建一个简单项目，正常情况下按 snowolf-download ---> snowolf-ssh-images-upload ---> snowolf-pipeline-import ---> snowolf-pipeline-preupgrade ---> snowolf-pipeline-monitor ---> snowolf-pipeline-upgrade ---> snowolf-pipeline-monitor
依次顺序执行这些skill才能执行完成该项目。但(1)、(2)前面两个skill不是必选的，要支持手工命令参数跳过指定的skill，其他是必选切严格按顺序串行执行。
5.帮忙给出各个skill的大致参考样例，对这些零散skill编排调度、skill之间上下文传递、skill生命周期、各个阶段skill执行日志等进行统一管理

以上生成的代码放置到C:\python_project\python_test\openclaw\skill_project_c目录下
