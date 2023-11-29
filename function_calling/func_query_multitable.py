import sqlite3
from ..common import get_completion_through_dict, func_calling_call_func

database_schema_customers = """
CREATE TABLE customers (
    id INT PRIMARY KEY NOT NULL,  -- 主键，不允许为空
    customer_name VARCHAR(255) NOT NULL,  -- 客户姓名，不允许为空
    email VARCHAR(255) UNIQUE,  -- 邮箱，唯一
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 注册时间，默认当前时间
);
"""
database_schema_products = """
CREATE TABLE products (
    id INT PRIMARY KEY NOT NULL,  -- 主键，不允许为空
    product_name VARCHAR(255) NOT NULL,  -- 产品名称，不允许为空
    price DECIMAL(10, 2) NOT NULL  -- 价格，不允许为空
);
"""
database_schema_orders = """
CREATE TABLE orders (
    id INT PRIMARY KEY NOT NULL,  -- 主键，不允许为空
    customer_id INT NOT NULL,  -- 客户ID，不允许为空
    product_id INT NOT NULL,  -- 产品ID，不允许为空
    price DECIMAL(10, 2) NOT NULL,  -- 价格，不允许为空
    status INT NOT NULL,  -- 订单状态，不允许为空; 0 代表待支付, 1代表已支付， 2代表已退款
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间，默认当前时间
    pay_time TIMESTAMP  -- 支付时间，可以为空
);
"""
database_schema_string = (
    database_schema_customers + database_schema_products + database_schema_orders
)
print("database_schema_string=", database_schema_string)

mock_data_customers = [
    (1001, "王卓然", "wangzhuoran@163.colm", "2023-10-12 10:00:00"),
    (1002, "孙志刚", "sunzhigang@126.com", "2023-10-16 11:00:00"),
    (1003, "李晓明", "lixiaoming@hotmail.com", "2023-10-17 12:30:00"),
]
mock_data_products = [
    (2001, "TSHIRT_1", 50.00),
    (2002, "TSHIRT_2", 75.50),
    (2003, "SHOES_X2", 25.25),
    (2004, "HAT_Z112", 60.75),
    (2005, "WATCH_X001", 90.00),
]
mock_data_orders = [
    (1, 1001, 2001, 50.00, 0, "2023-10-12 10:00:00", None),
    (2, 1001, 2002, 75.50, 1, "2023-10-16 11:00:00", "2023-08-16 12:00:00"),
    (3, 1002, 2003, 25.25, 2, "2023-10-17 12:30:00", "2023-08-17 13:00:00"),
    (4, 1003, 2004, 60.75, 1, "2023-10-20 14:00:00", "2023-08-20 15:00:00"),
    (5, 1002, 2005, 90.00, 0, "2023-10-28 16:00:00", None),
    (6, 1002, 2002, 75.50, 1, "2023-10-16 12:00:00", "2023-10-19 12:00:00"),
]

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute(database_schema_customers)
cursor.execute(database_schema_products)
cursor.execute(database_schema_orders)

for record in mock_data_customers:
    cursor.execute(
        "INSERT INTO customers (id, customer_name, email, register_time) VALUES (?, ?, ?, ?)",
        record,
    )
for record in mock_data_products:
    cursor.execute(
        "INSERT INTO products (id, product_name, price) VALUES (?, ?, ?)",
        record,
    )
for record in mock_data_orders:
    cursor.execute(
        "INSERT INTO orders (id, customer_id, product_id, price, status, create_time, pay_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
        record,
    )
conn.commit()


def query_db(query):
    print("query_db()")
    print("query=", query)
    cursor.execute(query)
    records = cursor.fetchall()
    return records


prompt = "统计每月每件商品的销售额"
# 如果使用了后半句注释的话，
prompt = "这个月消费最高的用户是谁?"  # 他买了哪些商品？每件商品买了几件？ 花费多少?"
messages = [
    {
        "role": "system",
        "content": "你是一个数据分析师，你可以查询数据库, 请基于order, product, customer等表回答用户问题",
    },
    {"role": "user", "content": prompt},
]

callback = {"query_db": query_db}
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_db",
            "description": "Use this function to answer user question about business. \
            Output should be a fully formed SQL query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                        a SQL query extracting data from the user's question.
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

response = get_completion_through_dict(
    model="gpt-3.5-turbo-1106", messages=messages, tools=tools
)
print("=== GPT 回复 ===")
print("response=", response)
response_message = response.choices[0].message

final_response = func_calling_call_func(
    response_message, messages, tools, callback, "query_db"
)
print("=== 最终回复 ===")
print("final_response=", final_response.choices[0].message.content)
