# 本例是用assistant API执行查询高德地图的例子;
import os
import json
import requests
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
amap_key = os.getenv("AMAP_KEY")
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE")
)


def get_location_coordinate(location, city="北京"):
    pass


def search_nearby_pois(longtitude, latitude, keyword):
    pass


assistant = client.beta.assistants.create(
    name="导游",
    description="这是一个地图通，你可以找到任何地址",
    model="gpt-3.5-turbo-1106",
    # 创建assistant，可以选择带有的function calling的定义
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_location_coordinate",
                "description": "根据POI的名称，获得POI的经纬度坐标",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "POI的名称",
                        },
                        "city": {
                            "type": "string",
                            "description": "POI所在的城市",
                        },
                    },
                    "required": ["location", "city"],
                },
            },
        },
        {
            "type": "function",
            "fucntion": {
                "name": "search_nearby_pois",
                "description": "根据经纬度坐标，搜索附近的POI",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "longtitude": {
                            "type": "string",
                            "description": "中心点经度",
                        },
                        "latitude": {
                            "type": "string",
                            "description": "中心点纬度",
                        },
                        "keyword": {
                            "type": "string",
                            "description": "目标poi的关键字",
                        },
                    },
                    "required": ["longtitude", "latitude", "keyword"],
                },
            },
        },
    ],
)

thread = client.beta.threads.create(
    messages=[{"role": "user", "content": "北京三里屯附近的咖啡"}]
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

print("=== run ===")
print(run)

while True:
    pass
