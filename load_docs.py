import json
import re

def extract_api_information(api_text):    
    # Extract the API name (from the header)
    name_end = api_text.find("\n", 0)
    name = api_text[:name_end]

    # 提取描述
    desc_match = re.findall("`\n\n([\S\n\t\v ]*?)\*\*", api_text)
    description = desc_match[0].replace(">", "").replace("\n", "").strip() if desc_match else "No description"

    endpoint_match = re.search(r'`\s*(GET|POST|PUT|DELETE)\s+([^\s]+)\s*`', api_text)
    endpoint = f"{endpoint_match.group(1)} {endpoint_match.group(2)}" if endpoint_match else "No endpoint"

    # 使用正则表达式根据 "**Parameters**" 和 "**Response**" 进行拆分
    parts = re.split(r'\*\*(Parameters|Response|Permission)\*\*', api_text)

    parameters = "No parameters"
    response = "No response"

    # 遍历拆分后的部分，根据标记提取内容
    for i in range(1, len(parts), 2):
        if parts[i] == "Parameters":
            parameters = parts[i+1].strip()
        elif parts[i] == "Response":
            response_match = re.search(r'```js(.*?)```', parts[i + 1], re.DOTALL)
            if response_match:
                response = response_match[1].strip()
                # 清理多余的空格和换行符
                response = re.sub(r'\s+', ' ', response).replace(' ,', ',')
    
    # 返回提取到的结果，保证顺序为parameters -> response
    return {
        "name": name,
        "description": description,
        "endpoint": endpoint,
        "parameters": parameters,
        "response": response
    }

def load_api_data(file_path="docs/_rest-api.md"):
    with open(file_path, 'r') as file:
        data = file.read()

    sections = re.split(r'\n## ', data)

    parsed = []
    for i in sections:
        c = extract_api_information(i)
        parsed.append(c)
        
    return [
        {
            'id': i['name'],
            'text': json.dumps(i)
        }
        for i in parsed[1:]
    ]
