import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# 加载 .env 文件
load_dotenv()

def search(query):
    """
    使用 GLM 模型进行联网搜索并回答用户查询
    """
    print(f"🔍 正在执行 [GLM 模型] 网页搜索: {query}")
    api_key = os.getenv("SEARCHZHIPU_API_KEY")
    if not api_key:
        return "错误:SEARCHZHIPU_API_KEY 未在 .env 文件中配置。"

    client = ZhipuAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
        # 指定模型，例如 glm-4.7
        model=os.getenv("LLM_MODEL_ID"),
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
        # 关键点：启用联网搜索工具
        tools=[
            {
                "type": "web_search",
                "web_search": {
                    "enable": True,  # 必须设置为 True 来启用搜索
                    # 可选参数：控制搜索结果的详细程度，"simple" 或 "detailed"
                    # "search_result": True,  # 是否在响应中包含搜索结果详情
                    # "top_k": 10,  # 控制返回搜索结果的数量
                }
            }
        ],
    )
    

    # 提取模型生成的回答
        answer = response.choices[0].message.content

    except Exception as e:
        return f"搜索时发生错误: {e}"
    
    # 可选：检查是否有引用的搜索结果
    if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
        # 这里可以处理搜索结果详情，如果请求参数中设置了 "search_result": True
        # 详情通常在 response.choices[0].message.tool_calls 中
        pass
        
    return answer


"""
# 示例查询
query = "最近有什么重要的科技新闻？或者查询一下最新的苹果公司股价。"
answer = search(query)
print(f"回答: {answer}")

# 另一个需要实时信息的例子
query2 = "今天北京的天气怎么样？"
answer2 = search(query2)
print(f"回答: {answer2}")

# 再一个例子：模型知识截止日期之后的事情
query3 = "告诉我关于2024年巴黎奥运会的一些亮点。"
answer3 = search(query3)
print(f"回答: {answer3}")
"""
