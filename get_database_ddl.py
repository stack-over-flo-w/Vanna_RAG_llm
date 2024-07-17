import mysql.connector

# 连接到 MySQL 数据库
def connect_to_database(host, user, password, database,port):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    return connection

# 获取所有表名
def get_table_names(connection):
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'agent_data'"
    cursor = connection.cursor()
    cursor.execute(query)
    table_names = [item[0] for item in cursor.fetchall()]
    cursor.close()
    return table_names

# 获取指定表的DDL
def get_table_ddl(connection, table_name):
    query = f"SHOW CREATE TABLE {table_name}"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[1]  # 返回创建表的SQL语句

# 主函数
def get_ddls():
    host = ''          # 数据库主机地址
    user = ""     # 数据库用户名
    password = ''  # 数据库密码
    database = ''  # 数据库名
    port = ""
    ddls = []
    # 连接数据库
    connection = connect_to_database(host, user, password, database, port)

    # 获取所有表名
    table_names = get_table_names(connection)
    print("Table Names:", table_names)

    # 遍历每个表名，获取其DDL并打印
    for table in table_names:
        ddl = get_table_ddl(connection, table)
        ddls.append(ddl)

    # 关闭数据库连接
    connection.close()
    return ddls