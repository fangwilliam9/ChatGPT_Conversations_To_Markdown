# ChatGPT_Conversations_To_Markdown\check_json.py"
import json

file_path = R"io_in/gpt_export/conversations.json"


# 读取 conversations.json
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)


# 打印第一个会话的数据
if data:
    print("第一条对话：", json.dumps(data[0], indent=2, ensure_ascii=False))
else:
    print("conversations.json 为空！")


# outcome: Printed the first conversation