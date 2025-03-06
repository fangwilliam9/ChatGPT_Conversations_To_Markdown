# ChatGPT Conversations to Markdown(cc2m)



[TOC]

## 简介

ChatGPT Conversations to Markdown is a Python script that converts your exported ChatGPT conversations into readable and well-formatted Markdown files by using the `conversations.json` file. The script provides a convenient way to archive and share your interactions with ChatGPT.



## Prerequisite预备知识/先修科目

- [什么是`.json`文件格式？](notes/what_is_json.md)
- [什么是`.markdown`文件格式？](notes/what_is_markdown.md)
- [什么是`config.json`(配置文件)？](notes/role_of_config_file.md)
- [`json`转`md`的源代码，详细解析](notes/src_analysis.md)







## Features特点/亮点功能
* Convert ChatGPT conversations stored in JSON format to Markdown
* Customize user and assistant names <u>using a configuration file</u>
* Include or exclude date in the output Markdown files
* Customize the format of file names, dates, and message separators
* Process **individual** JSON files OR **all** JSON files in a directory

## Installation如何克隆此代码仓库到本地进行编辑/使用？
1. Clone the repository or download the ZIP file and extract it to a folder on your computer.
```
git clone https://github.com/daugaard47/ChatGPT_Conversations_To_Markdown.git
```
2. Change into the project directory:
```
cd ChatGPT_Conversations_To_Markdown
````
3. Create a virtual environment (optional but recommended):
```
python -m venv venv
```
4. Activate the virtual environment:
```raw
# For Windows:
venv\Scripts\activate
```

```raw
# For Linux or macOS:
source venv/bin/activate
```



5. Install the required Python dependencies:
```
pip install tqdm
```

## Usage使用步骤
1. Update the `config.json` file with your desired settings, such as user and assistant names, input and output paths, and other formatting options.
2. Create your JSON input directory and add the JSON file e.g. `conversations.json` you received from the export of the ChatGPT conversations to this location. Add this path to your config file.
3. Create the Output Directory and add this path to your config file. Your markdown files will appear here after the script runs.
4. Run the script: `python chatgpt_json_to_markdown.py`
5. The script will process your conversations and save them as Markdown files in the specified output directory.
6. When the script is done, you will see a message like this:
```
All Done Buddy! You can access your files here: <output_directory>
```

Now you can easily read, share, or archive your ChatGPT conversations in a more human-readable format. Enjoy!





































