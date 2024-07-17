import os
import re
import pandas as pd
import vanna
from openai import OpenAI
from vanna.remote import VannaDefault
from pymilvus import MilvusClient, model

import SQL_QA
import get_database_ddl
from Config import cfg
from Logger import logger
from My_vanna import VannaMilvus
from embedding import EmbeddingApi
from extract_excel import extract_tables_from_excel

EXPLAIN_TEMPLATE = """
你的任务是基于信息和sql问答对提取关键知识。信息之中包含了数据表的创建语句，你需要从sql问答对中提取出创建语句中所没有的关键信息，比如对某些字段信息的额外解释

**CONSTRAINTS**
- 不区分中英文，语义一致即可
- 不要反问用户
- 不要带有语气地回答
- 要详细描述这个关键词的含义，为什么在sql中选取了这个数值
"""

def llm_train_sql(vn,question,sql):
    document = vn.get_related_documentation(question)
    prompt_sql = vn.get_similar_question_sql(question)
    relate_ddl = vn.get_related_ddl(question)
    prompt = vn.get_sql_prompt(
        initial_prompt=EXPLAIN_TEMPLATE,
        question="问题: "+ question+" sql: " + sql,
        question_sql_list=[],
        ddl_list=relate_ddl,
        doc_list=[],
    )
    logger.info(prompt)
    llm_response = vn.submit_prompt(prompt)
    logger.info(llm_response)

    vn.train(documentation=llm_response)

def train_with_schema(vn):
    docs = extract_tables_from_excel(r"C:\Users\michi\PycharmProjects\vanna_sh\schema注释.xlsx")
    for doc in docs:
        vn.train(documentation=doc)

def train_ddl(vn):
    ddls = get_database_ddl.get_ddls()
    for ddl in ddls:
        vn.train(ddl=ddl)


if __name__ == "__main__":
    milvus_client = MilvusClient(uri=f"http://{cfg.milvus_host}:{cfg.milvus_port}")

    qwen_client = OpenAI(base_url=cfg.private_model_url)
    vn_milvus = VannaMilvus(
        client=qwen_client,
        config={
            "model": cfg.chat_model,
            "milvus_client": milvus_client,
            "embedding_function": model.dense.OpenAIEmbeddingFunction(
                model_name=cfg.embedding_model,  # Specify the model name
                api_key=cfg.openai_key,  # Provide your OpenAI API key

            ),
            "max_tokens": 14000
        }
    )

    vn_milvus.connect_to_mysql(host='myhost', dbname='mydbname', user='myuser', password='mypassword', port='myport')
    for item in SQL_QA.SQL_QA_2:
        question = item["question"]
        sql = item["sql"]
        vn_milvus.train(question=question,sql=sql)
        llm_train_sql(vn_milvus,question,sql)
    #train_ddl(vn_milvus)
    #train_with_schema(vn_milvus)
    #vn_milvus.train(question="HRMDEPARTMENT	中的id是部门唯一id")
