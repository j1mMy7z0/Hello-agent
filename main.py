"""
ReAct Agent 测试脚本
"""
import os
from dotenv import load_dotenv
from HelloAgentsLLM import HelloAgentsLLM
from ToolExecutor import ToolExecutor
from Search import search
from ReAct import ReActAgent

# 加载环境变量
load_dotenv()

def main():
    print("=" * 60)
    print("ReAct Agent 测试程序")
    print("=" * 60)

    # 1. 初始化 LLM 客户端
    print("\n[1/3] 初始化 LLM 客户端...")
    try:
        llm_client = HelloAgentsLLM()
        print(f"✅ LLM 客户端初始化成功 (模型: {llm_client.model})")
    except ValueError as e:
        print(f"❌ LLM 客户端初始化失败: {e}")
        return

    # 2. 初始化工具执行器
    print("\n[2/3] 初始化工具执行器...")
    tool_executor = ToolExecutor()

    # 注册搜索工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_description, search)
    print("✅ 搜索工具已注册")
    print(f"可用工具: {tool_executor.getAvailableTools()}")

    # 3. 初始化 ReAct Agent
    print("\n[3/3] 初始化 ReAct Agent...")
    agent = ReActAgent(
        llm_client=llm_client,
        tool_executor=tool_executor,
        max_steps=5
    )
    print("✅ ReAct Agent 初始化完成")

    # 4. 运行测试问题
    print("\n" + "=" * 60)
    print("开始运行 ReAct Agent")
    print("=" * 60)

    test_question = "英伟达最新的GPU型号是什么？"

    print(f"\n📝 问题: {test_question}\n")

    try:
        answer = agent.run(test_question)
        if answer:
            print(f"\n✅ 最终答案: {answer}")
        else:
            print("\n⚠️ 未能获得最终答案")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
