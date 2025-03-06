# source code of the converting logic
# path of this file: "ChatGPT_Conversations_To_Markdown\chatgpt_json_to_markdown.py"
import json
import os
import sys
import glob
from datetime import datetime
from tqdm import tqdm # 进度可视化Progress visualization


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# 消息内容解析核心（_get_message_content）
def _get_message_content(message):
    """ 解析 message['content']，多类型消息解析器，适配不同格式 """
    content = message.get("content", {})

    # 类型安全校验
    if not isinstance(content, dict):
        return ""

    content_type = content.get("content_type", "")

    # 普通文本消息
    if content_type == "text":
        return "\n".join(content.get("parts", []))

    # 用户上下文信息（静默跳过）
    elif content_type == "user_editable_context":
        return ""

    # 浏览器搜索相关（可能是联网查询的结果，跳过）
    elif content_type == "tether_browsing_display":
        return ""

    # 其他未知类型处理，避免崩溃
    else:
        return f"[未知消息类型: {content_type}]"




# 标题生成逻辑（_get_title）
def _get_title(title, first_message):
    """
    三段式标题生成策略
    Return conversation['title'] if it exists, otherwise infer it from the first message
    """
    if title:
        return title # 优先使用原始标题
    
    # If there is no title, use the first message
    # 后备方案：解析首条消息
    content = _get_message_content(first_message)

    # 智能截取首行（处理多行消息）
    first_line = content.split("\n", 1)[0]
    return first_line.rstrip() + "..."  # 添加省略号避免截断感




# core_对话数据处理
def process_conversations(data, output_dir, config):
    # 带进度条的迭代处理
    for entry in tqdm(data, desc="Processing conversations"):
        # Ensure each entry is a dictionary 
        # 防御性类型检查（重要！）
        if not isinstance(entry, dict):
            print(f"Skipping entry, expected dict but got {type(entry).__name__}: {entry}")
            continue

        # Safely get the title and mapping
        # 安全获取嵌套数据（避免KeyError）
        title = entry.get("title", None)
        mapping = entry.get("mapping", {})

        # Extract messages from the "mapping" key
        # 消息提取与过滤
        messages = [
            item["message"] 
            for item in mapping.values() 
            if isinstance(item, dict) and item.get("message") is not None
        ]

        # Sort messages by their create_time, handling None values
        # 稳定排序（处理缺失时间戳）
        messages.sort(key=lambda x: x.get("create_time") or float('-inf'))

        # Use the first message to infer the title if it's not available 
        # 智能标题生成
        inferred_title = _get_title(title, messages[0] if messages else {"content": {"text": "Untitled"}})

        # Sanitize the title to ensure it's a valid filename
        # 文件名消毒处理（重要安全措施）
        sanitized_title = ''.join(c for c in inferred_title if c.isalnum() or c in [' ', '_']).rstrip()
        file_name = f"{config['file_name_format'].format(title=sanitized_title.replace(' ', '_').replace('/', '_'))}.md"
        file_path = os.path.join(output_dir, file_name)
        # print(f"📂 正在写入文件: {file_path}")
        # print(f"🔄 处理对话: {inferred_title}，消息数: {len(messages)}")


        # Write messages to file文件写入操作
        with open(file_path, "w", encoding="utf-8") as f:
            # 可选日期头
            if messages and messages[0].get("create_time") and config['include_date']:
                date = datetime.fromtimestamp(messages[0]["create_time"]).strftime(config['date_format'])
                f.write(f"<sub>{date}</sub>{config['message_separator']}")
            
            # 消息流处理
            for message in messages:
                author_role = message["author"]["role"]
                content = _get_message_content(message) # 内容解析核心
                author_name = config['user_name'] if author_role == "user" else config['assistant_name']

                # 空消息过滤逻辑
                if not config['skip_empty_messages'] or content.strip():
                    f.write(f"## {author_name}:\n\n {content}{config['message_separator']}")





def main():
    # read config file
    config_path = "config.json"
    config = read_json_file(config_path) # load crucial configurations

    input_path = config['input_path']
    output_dir = config['output_directory']

    # 创建输出目录（防御性编程）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 输入模式判断（文件/目录）
    if config['input_mode'] == 'directory':
        json_files = glob.glob(os.path.join(input_path, '*.json'))
        for json_file in json_files:
            data = read_json_file(json_file)
            process_conversations(data, output_dir, config)
    else:
        data = read_json_file(input_path)
        process_conversations(data, output_dir, config)

    print(f"All Done Buddy! You can access your files here: {output_dir}")


if __name__ == "__main__":
    main()
