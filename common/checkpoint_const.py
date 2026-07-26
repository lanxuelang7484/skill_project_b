# 流水线执行步骤常量，严格顺序
STEP_INIT = "init"
STEP_DOWNLOAD = "snowolf-download"
STEP_UPLOAD = "snowolf-ssh-images-upload"
STEP_PIPELINE_IMPORT = "snowolf-pipeline-import"
STEP_PREUPGRADE = "snowolf-pipeline-preupgrade"
STEP_MONITOR_PRE = "snowolf-monitor-preupgrade"
STEP_UPGRADE = "snowolf-pipeline-upgrade"
STEP_MONITOR_UPGRADE = "snowolf-monitor-upgrade"
STEP_FINISH = "finish"

# 执行顺序列表，不可变更
STEP_ORDER = [
    STEP_DOWNLOAD,
    STEP_UPLOAD,
    STEP_PIPELINE_IMPORT,
    STEP_PREUPGRADE,
    STEP_MONITOR_PRE,
    STEP_UPGRADE,
    STEP_MONITOR_UPGRADE
]
