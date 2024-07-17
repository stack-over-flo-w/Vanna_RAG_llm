import pandas as pd

def extract_tables_from_excel(file_path):
    data = pd.read_excel(file_path, header=None)  # 不使用header，因为数据不是标准的表头

    # 寻找数据块的起始点，以"数据表名称"为标识
    start_indexes = data.index[data[0] == '数据表名称'].tolist()

    # 每个表的结束索引可以视作下一个表的开始索引，最后一个表的结束索引是DataFrame的末尾
    end_indexes = start_indexes[1:] + [data.shape[0]]

    # 提取和格式化每个表
    texts = []
    for start, end in zip(start_indexes, end_indexes):
        # 提取单个表格
        table = data.iloc[start:end].reset_index(drop=True)

        # 格式化文本
        text = f"数据表名称：{table.iloc[0, 1]}\n"
        text += f"数据表含义：{table.iloc[1, 1]}\n"
        for index in range(3, table.shape[0]):
            if pd.notna(table.iloc[index, 1]) and pd.notna(table.iloc[index, 2]):
                name = table.iloc[index, 0].strip()
                field_name = table.iloc[index, 1].strip()
                comment = table.iloc[index, 2].strip()
                text += f"字段名:{name}  类型:{field_name}  注释: {comment}\n"

        texts.append(text)

    return texts

#print(extract_tables_from_excel("schema注释.xlsx"))