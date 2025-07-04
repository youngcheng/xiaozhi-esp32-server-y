from core.handle.reportHandle import enqueue_asr_report
from core.handle.receiveAudioHandle import startToChat

TAG = __name__

async def handleReminderMessage(conn, msg_json):
    payload = msg_json.get("payload")
    if not isinstance(payload, dict):
        conn.logger.bind(tag=TAG).error("Reminder消息缺失payload或格式非字典")
        return

    content = payload.get("content")
    if content is None:
        conn.logger.bind(tag=TAG).error("Reminder消息缺少content字段")
        return

    conn.logger.bind(tag=TAG).info(f"收到提醒消息：{content}")

    if not content.strip():
        conn.logger.bind(tag=TAG).warning("Reminder消息content为空内容")
        return

    query = f"""你需要执行提醒任务：
1. 以你的方式立即提醒用户
2. 提醒内容：{content}
3. 用户如无应答，可再次提醒：
"""
    # 上报纯文字数据（复用ASR上报功能，但不提供音频数据）
    enqueue_asr_report(conn, query, [])
    # 需要LLM对文字内容进行答复
    await startToChat(conn, query, "system")