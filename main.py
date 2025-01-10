# -*- coding: utf-8 -*-
from tqdm import tqdm
import openai
import pandas as pd
from openai import OpenAI
import httpx
import openpyxl

client = OpenAI(
    base_url="https://api.xty.app/v1",
    api_key="Your_API-KEY",
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)


def classfication(msg):
    prompt = """
    现在你需要根据传入的文本进行关键词提取、主题分析、情绪分析(只有积极或者消极，没有中性)和使用倾向，用中文分号分隔每一类标签。
    对于无法提取关键词、主题的文本，返回 无法提取 即可，不要道歉，不要返回其他无关的语句。现提供以下示例:
    输入：目前的大模型不具备智能，本质还是函数拟合，跟人工智能没啥关系！
    你的回答：智能，本质，函数拟合，人工智能；技术本质；消极；无倾向
     """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 模型名称
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': msg}
        ],
        temperature=0.8
    )
    return completion.choices[0].message.content


# 需要处理的文本路径
file_path = "./data/data_clear_LM+LLM（full version).xlsx"
file = openpyxl.load_workbook(file_path)
sheet = file.active  # 确定当前活动的工作表
df = pd.read_excel(file_path)
contents = df['评论']
contents = [str(i).replace('\\', '') for i in contents if pd.notna(i)]
i = 2
for content in tqdm(contents, desc="数据写入", ncols=100):
    try:
        msg = content
        response = classfication(msg)
        parts = response.split('；')  # 使用中文分号分割字符串
        for j, part in enumerate(parts):
            column_to_write = j + 5  # 确定要写入的列，这里从第五列开始
            sheet.cell(row=i, column=column_to_write).value = part.strip()
            file.save(file_path)
    except openai.BadRequestError as e:
        print("第{}条数据写入失败".format(i - 1))
    i += 1
print("所有数据处理完成")
