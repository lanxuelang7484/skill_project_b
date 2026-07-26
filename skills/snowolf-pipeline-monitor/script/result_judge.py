# 结果判定辅助（可扩展告警逻辑）
def judge_result(status: str):
    if status == "success":
        return True, "执行成功"
    elif status == "failed":
        return False, "任务失败，人工介入"
    else:
        return False, "任务超时，人工介入"
