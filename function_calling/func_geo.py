import requests
from ..common import get_completion_through_dict, func_calling_call_func

amap_key = "6d672e6194caa3b639fccf2caf06c342"


def get_location_coordinate(location, city="北京"):
    print("get_location_coordinate()=", location, city)
    url = f"https://restapi.amap.com/v5/place/text?key={amap_key}&keywords={location}&region={city}"
    print("url=", url)
    r = requests.get(url)
    result = r.json()
    if "pois" in result and result["pois"]:
        return result["pois"][0]
    return None


def search_nearby_pois(longitude, latitude, keyword):
    print("search_nearby_pois()=", longitude, latitude, keyword)
    url = f"https://restapi.amap.com/v5/place/around?key={amap_key}&keywords={keyword}&location={longitude},{latitude}"
    print("url=", url)
    r = requests.get(url)
    result = r.json()
    ans = ""
    if "pois" in result and result["pois"]:
        for i in range(min(3, len(result["pois"]))):
            name = result["pois"][i]["name"]
            address = result["pois"][i]["address"]
            distance = result["pois"][i]["distance"]
            ans += f"{name}\n{address}\n距离: {distance}米\n\n"
    return ans


prompt = "北京三里屯附近的咖啡"
messages = [
    {"role": "system", "content": "你是一个地图通，你可以找到任何地址"},
    {"role": "user", "content": prompt},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_location_coordinate",
            "description": "根据POI名称，获得POI的经纬度坐标",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "POI名称, 必须是中文",
                    },
                    "city": {
                        "type": "string",
                        "description": "POI所在城市名称, 必须是中文",
                    },
                },
                "required": ["location", "city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_nearby_pois",
            "description": "根据给定经纬度坐标，搜索附近的POI",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitude": {
                        "type": "string",
                        "description": "中心点的经度",
                    },
                    "latitude": {
                        "type": "string",
                        "description": "中心点的纬度",
                    },
                    "keyword": {
                        "type": "string",
                        "description": "目标poi关键词",
                    },
                },
                "required": ["longitude", "latitude", "keyword"],
            },
        },
    },
]

# 启动第一轮对话
response = get_completion_through_dict(
    messages=messages, model="gpt-3.5-turbo-1106", tools=tools, seed=1024
)
response_message = response.choices[0].message
print("=== GPT回复 ===")
print("response=", response)

callback = {
    "get_location_coordinate": get_location_coordinate,
    "search_nearby_pois": search_nearby_pois,
}
location_response = func_calling_call_func(
    response_message, messages, tools, callback, "get_location_coordinate"
)
print("=== get_location_coordinate 回复 ===")
print("location_response=", location_response)

location_response_message = location_response.choices[0].message
final_response = func_calling_call_func(
    location_response_message, messages, tools, callback, "search_nearby_pois"
)
print("=== search_nearby_pois 最终回复 ===")
print("final_response=", final_response.choices[0].message.content)
