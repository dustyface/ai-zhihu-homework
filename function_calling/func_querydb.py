# 摘自OpenAI官方示例:
# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb

import sqlite3
from ..common import get_completion_through_dict, func_calling_call_func

# prepare the database
database_schema_string = """
CREATE TABLE orders (
    id INT PRIMARY KEY NOT NULL,  -- 主键，不允许为空
    customer_id INT NOT NULL,  -- 客户ID，不允许为空
    product_id STR NOT NULL,  -- 产品ID，不允许为空
    price DECIMAL(10, 2) NOT NULL,  -- 价格，不允许为空
    status INT NOT NULL,  -- 订单状态，不允许为空; 0 代表待支付, 1代表已支付， 2代表已退款
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间，默认当前时间
    pay_time TIMESTAMP  -- 支付时间，可以为空
);
"""
mock_data = [
    (1, 1001, "TSHIRT_1", 50.00, 0, "2023-10-12 10:00:00", None),
    (2, 1001, "TSHIRT_2", 75.50, 1, "2023-10-16 11:00:00", "2023-08-16 12:00:00"),
    (3, 1002, "SHOES_X2", 25.25, 2, "2023-10-17 12:30:00", "2023-08-17 13:00:00"),
    (4, 1003, "HAT_Z112", 60.75, 1, "2023-10-20 14:00:00", "2023-08-20 15:00:00"),
    (5, 1002, "WATCH_X001", 90.00, 0, "2023-10-28 16:00:00", None),
]

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute(database_schema_string)
for record in mock_data:
    cursor.execute(
        "INSERT INTO orders (id, customer_id, product_id, price, status, create_time, pay_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
        record,
    )
conn.commit()


def ask_database(query):
    print("ask_database()")
    print("query=", query)
    cursor.execute(query)
    records = cursor.fetchall()
    return records


prompt = "上个月销售额"
prompt = "统计每月每件商品的销售额"
prompt = "哪个用户消费最高？消费多少?"

messages = [
    {"role": "system", "content": "你是一个数据分析师，你可以查询数据库, 请基于order表回答用户问题"},
    {"role": "user", "content": prompt},
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "ask_database",
            "description": "Use this function to answer user question about business. \
            Output should be a fully formed SQL query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                        SQL query extracting info to answer the user's question.
                        SQL should be written using this database schema:
                        {database_schema_string}
                        The query should be returned in plain text, not in JSON.
                        The query should only contain grammars supported by SQLite.
                        """,
                    }
                },
                "required": ["query"],
            },
        },
    }
]

callback = {
    "ask_database": ask_database,
}

response = get_completion_through_dict(
    model="gpt-3.5-turbo-1106",
    messages=messages,
    tools=tools,
    seed=1024,
)
print("=== GPT回复 ===")
# print("response=", response)
response_message = response.choices[0].message

final_response = func_calling_call_func(
    response_message, messages, tools, callback, "ask_database"
)
print("=== 最终回复 ===")
print("final_response=", final_response.choices[0].message.content)
