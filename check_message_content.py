# check_message_content.py

import json

# 设置文件路径
file_path = "io_input/gpt_export/conversations.json"

def read_json_file(file_path):
    """ 读取 JSON 文件 """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def check_message_structure(data):
    """ 遍历所有对话，提取 message['content'] 的结构 """
    content_types = {}

    for entry in data:
        mapping = entry.get("mapping", {})

        for item in mapping.values():
            # 确保 item 是字典，并且包含 message
            if not isinstance(item, dict) or "message" not in item or not isinstance(item["message"], dict):
                continue

            message = item["message"]
            content = message.get("content", {})

            # 记录不同格式的 content
            content_type = str(content.keys())  # 记录 key 结构
            if content_type not in content_types:
                content_types[content_type] = []
            content_types[content_type].append(content)

    # 打印不同的 content 结构
    print("\n===== 检测到的 message['content'] 结构 =====\n")
    for idx, (content_type, examples) in enumerate(content_types.items(), 1):
        print(f"🔹 结构 {idx}: {content_type}")
        print(f"  示例数据: {json.dumps(examples[0], indent=2, ensure_ascii=False)}\n")

if __name__ == "__main__":
    # 读取 JSON 数据
    data = read_json_file(file_path)
    
    # 检查 message 的结构
    check_message_structure(data)
