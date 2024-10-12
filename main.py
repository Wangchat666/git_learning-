import pandas as pd
from openai import OpenAI
import httpx

client = OpenAI(
    base_url="https://api.xty.app/v1",
    api_key="sk-n7PZWcYgdjdgWOIE8aFa5e5fCdBd4193B985198878726d77",
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)


def classfication(msg):
    prompt = """
    现在你需要根据传入的文章内容，文章进行分类，从以下词组中选择最适合的分类标签：
	科学技术观，科技发展的趋势，基础研究的作用，科学和技术的关系，科学技术与社会的关系；科学技术功能，科学技术生产力功能，科学技术是第一生产力论，创新驱动发展；科学技术功能实现，科技体制改革，教育和人才的支撑作用，全球科技",
     可以选择一个或多个词组(最多不超过四个)。如果你认为文章内容与以上几个分类标签不合适，可以输入你认为合适的分类标签，但请标注。
     注意：只返回分类标签即可，不要给出多余的句子。
     """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': msg}
        ],
        temperature=0.8
    )
    print(completion.choices[0].message.content)

fiLe_path = "./contents.xlsx"
df = pd.read_excel(fiLe_path)
contents = df['content']
contents = [str(i).replace('\\', '') for i in contents if pd.notna(i)]
for content in contents:
    msg = content
    classfication(msg)
