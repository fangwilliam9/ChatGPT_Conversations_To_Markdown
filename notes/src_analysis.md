➡️[此项目の完整介绍](report.md)

➡️[什么是：文件名消毒](filename_sanitization.md)

# 源码详解

## 此项目的简介

`GPT Chats to Md` is a Python script that converts your exported ChatGPT conversations into readable and well-formatted Markdown files by using the `conversations.json` file. The script provides a convenient way to archive and share your interactions with ChatGPT.

## Features特点/亮点功能

* Convert ChatGPT conversations stored in JSON format to Markdown
* Customize user and assistant names <u>using a configuration file</u>
* Include or exclude date in the output Markdown files
* Customize the format of file names, dates, and message separators
* Process **individual** JSON files OR **all** JSON files in a directory

## 一、导库


```python
import json
import os
import glob
from datetime import datetime
from tqdm import tqdm # 进度可视化Progress visualization
from pathvalidate import sanitize_filename # 文件名消毒
```

## 二、read_json


```python
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
```

## 三、消息内容解析核心


```python
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
```

## 四、主流程函数

### 4个清晰步骤

主流程函数process_conversations只有4个清晰步骤


```python
def process_conversations(data, output_dir, config):
    """处理对话数据的主流程控制器"""
    for entry in tqdm(data, desc="Processing conversations"):
        # 防御性检查：确保条目是字典类型
        if not isinstance(entry, dict):
            print(f"⚠️ 异常条目类型: {type(entry)}, 跳过处理")
            continue

        # 阶段1：数据提取
        messages = extract_and_sort_messages(entry)
        # 阶段2：元数据处理
        title = get_conversation_title(entry, messages)
        date_str = get_conversation_date(entry, messages, config)
        # 阶段3：文件操作
        file_path = generate_file_path(title, date_str, output_dir, config)
        # 阶段4：内容写入
        write_conversation_file(messages, file_path, config)
```

---


### 辅助函数区

每个函数的职责：

|      | 函数                        | 职责                   |
| ---- | --------------------------- | ---------------------- |
| 1    | `extract_and_sort_messages` | 负责原始数据提取和排序 |
| 2    | `get_conversation_title`    | 智能生成**对话标题**   |
| 3    | `get_conversation_date`     | 可靠获取**对话日期**   |
| 4    | `generate_file_path`        | 安全生成**输出路径**   |
| 5    | `write_conversation_file`   | 负责最终的格式化输出   |

主要改进点说明：

1. 模块化拆分：将原函数拆分为5个**独立函数**，每个函数**职责单一**
2. 防御性编程：每个步骤都包含**类型检查**、**异常处理**
3. 智能后备策略：关键数据（如标题、日期）都有**多层获取逻辑**
4. 安全增强：[文件名消毒](filename_sanitization.md)、路径安全检查等
5. 详细注释：每个函数、关键步骤都有中文注释说明

建议搭配以下学习策略：

1. 先看主流程函数的4个步骤
2. 逐个学习每个子函数的实现
3. 注意函数之间的参数传递
4. 重点关注防御性编程的处理方式
5. 多打印中间变量观察数据形态



#### 4.1 数据提取

提取&排序messages


```python
def extract_and_sort_messages(entry):
    """
    从原始条目中提取并排序消息
    Args:
        entry (dict): 原始对话条目
    Returns:
        list: 排序后的消息列表
    """
    # 安全获取消息映射表
    mapping = entry.get("mapping", {})
    
    # 消息提取流程
    extracted_messages = []
    for item in mapping.values():
        # 类型安全检查
        if not isinstance(item, dict):
            continue
        # 消息存在性检查
        message = item.get("message")
        if message is None:
            continue
        # 消息结构验证
        if not isinstance(message, dict):
            continue
        extracted_messages.append(message)
    
    # 排序策略：优先使用create_time，缺失值时排到最前
    def _sort_key(msg):
        timestamp = msg.get("create_time")
        # 处理异常时间戳（某些数据可能存在未来时间）
        try:
            return float(timestamp) if timestamp else float('-inf')
        except:
            return float('-inf')
    
    # 稳定排序确保顺序一致性
    return sorted(extracted_messages, key=_sort_key)

```

#### 4.2 元数据处理

###### 智能生成**对话标题**


```python
def get_conversation_title(entry, messages):
    """
    生成对话标题（三层后备策略）
    1. 优先使用条目自带的title字段
    2. 解析第一条用户消息内容
    3. 最终后备使用"Untitled"
    """
    # 第一层：原始标题
    original_title = entry.get("title")
    if original_title:
        return original_title
    
    # 第二层：解析首条消息
    if messages:
        first_msg = messages[0]
        content = _get_message_content(first_msg)
        # 提取有效首行（过滤空行）
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if lines:
            first_line = lines[0]
            # 智能截断逻辑（避免破坏URL等特殊内容）
            if len(first_line) > 50:
                return first_line[:47] + "..."
            return first_line
    
    # 第三层：终极后备
    return "Untitled"

```

###### 可靠获取**对话日期**


```python
def get_conversation_date(entry, messages, config):
    """
    获取对话日期（双重后备策略）
    1. 优先使用条目自身的create_time
    2. 使用第一条消息的create_time
    3. 返回"unknown_date"作为最后防线
    """
    def _timestamp_to_str(ts):
        """安全转换时间戳"""
        try:
            # 处理毫秒级时间戳（常见于JavaScript生成的数据）
            if ts > 1e12:
                ts /= 1000
            return datetime.fromtimestamp(ts).strftime(config['date_format'])
        except Exception as e:
            print(f"⚠️ 时间转换失败: {ts} | 错误: {e}")
            return "invalid_date"

    # 优先使用条目级别的时间戳
    entry_time = entry.get("create_time")
    if entry_time:
        return _timestamp_to_str(entry_time)
    
    # 后备使用第一条消息的时间
    if messages:
        first_msg_time = messages[0].get("create_time")
        if first_msg_time:
            return _timestamp_to_str(first_msg_time)
    
    # 终极后备
    return "unknown_date"

```

#### 4.3 文件操作

安全生成**输出路径**


```python
def generate_file_path(title, date_str, output_dir, config):
    """使用 pathvalidate 的安全路径生成"""
    # 消毒文件名（保留空格）
    sanitized_title = sanitize_filename(
        title,
        replacement_text="_",   # 非法字符替换为_
        max_len=100,        # 按需调整
        platform=config.get("platform", "auto")
    ).strip()

    # 动态格式化
    try:
        file_name = config['file_name_format'].format(
            date=date_str,
            title=sanitized_title
        ) + ".md"
    except KeyError:
        file_name = f"{date_str}_{sanitized_title}.md"

    # 路径安全检查
    full_path = os.path.abspath(os.path.join(output_dir, file_name))
    if not full_path.startswith(os.path.abspath(output_dir)):
        raise ValueError("路径越界风险！")

    return full_path

```

#### 4.4 内容写入

 负责最终的格式化输出，写入`.md`文件


```python
def write_conversation_file(messages, file_path, config):
    """
    将消息写入.md文件
    包含多种格式化选项和异常处理
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            # 写入日期头（如果配置需要）
            if config['include_date'] and messages:
                first_msg = messages[0]
                timestamp = first_msg.get("create_time")
                if timestamp:
                    try:
                        date = datetime.fromtimestamp(timestamp).strftime(config['date_format'])
                        f.write(f"<sub>{date}</sub>{config['message_separator']}")
                    except Exception as e:
                        print(f"⚠️ 日期头写入失败: {e}")
            
            # 消息写入循环
            for idx, msg in enumerate(messages):
                # 角色解析
                role = msg.get("author", {}).get("role", "unknown")
                # 内容解析
                content = _get_message_content(msg)
                
                # 空消息处理策略
                if config['skip_empty_messages'] and not content.strip():
                    continue
                
                # 角色映射（处理自定义名称）
                if role == "user":
                    author = config['user_name']
                elif role == "assistant":
                    author = config['assistant_name']
                else:
                    author = f"未知角色_{role}"
                
                # 消息格式化
                formatted = f"## {author}:\n\n{content}"
                # 分隔符处理（最后一条不加分隔符）
                if idx < len(messages) - 1:
                    formatted += config['message_separator']
                
                f.write(formatted)
                
    except IOError as e:
        print(f"⚠️ 文件写入失败: {file_path} | 错误: {e}")
    except Exception as e:
        print(f"⚠️ 未知写入错误: {type(e).__name__} | 错误: {e}")

```



## 五、main()


```python
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
```

## 六、执行


```python
if __name__ == "__main__":
    main()
```

```raw
Processing conversations: 100%|██████████████████████████████████████████████████| 86/86 [00:00<00:00, 1821.10it/s]

All Done Buddy! You can access your files here: io_out  
```



## 参考文献

1. 开源项目——[ChatGPT Conversations to Markdown](https://github.com/daugaard47/ChatGPT_Conversations_To_Markdown)
