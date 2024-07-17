import vanna
from openai import OpenAI
from pymilvus import MilvusClient
from vanna.remote import VannaDefault
from pymilvus import MilvusClient, model
from Config import cfg
from Logger import logger
from My_vanna import VannaMilvus

EXTRACTION_PROMPT_TEMPLATE = """
你的任务是基于信息生成SQL语句，根据已有的创建数据表的语句和举例中的sql问题和答案对于我询问你的问题生成新的sql。

**CONSTRAINTS**
- 不区分中英文，语义一致即可
- 不要反问用户
- 不要带有语气地回答
- 如果信息中的表多余一个则需要进行多表联查
- 如果提供的上下文足够，请生成一个有效的SQL查询，不对问题进行任何解释
- 如果提供的上下文几乎足够，但需要了解特定列中的特定字符串，请生成一个中间SQL查询来查找该列中的不同字符串。在查询前添加一条注释，说明intermediate_SQL
- 如果提供的上下文不充分，请解释为什么无法生成
- 如果问题之前已经被问过并回答过，请完全按照之前给出的答案重复
"""

TRUEFALSE_TEMPLATE = """
你的任务是基于信息判断生成的sql语句是否正确。信息之中包含了数据表的创建语句，一些作为例子的sql问答对和注释，在问题中包含一个问题和根据这个问题生成的sql语句，你需要判断这个语句是否能回答这个问题并且给出原因。

**CONSTRAINTS**
- 不区分中英文，语义一致即可。
- 不要反问用户
- 不要带有语气地回答.
"""

HYPO_TEMPLATE = """
你的任务是基于问题推断在生成sql语句时应该注意哪些信息。比如需要数据库中的哪些表，哪些字段，是否需要多表联查。

**CONSTRAINTS**
- 不区分中英文，语义一致即可。
- 不要反问用户
- 不要带有语气地回答.
- 不要给出任何sql语句，保证你的回答是描述性的，没有任何误导
"""

def llm_ask(vn,question):
    document = vn.get_related_documentation(question)
    prompt_sql = vn.get_similar_question_sql(question)
    relate_ddl = vn.get_related_ddl(question)
    prompt = vn.get_sql_prompt(
        initial_prompt=EXTRACTION_PROMPT_TEMPLATE,
        question=question,
        question_sql_list=prompt_sql,
        ddl_list=relate_ddl,
        doc_list=document,
    )
    for item in prompt:
        print(item['content'])
    logger.info(prompt)
    llm_response = vn.submit_prompt(prompt)
    logger.info(llm_response)


def llm_double(vn,question):
    '''
    document = vn_milvus.get_related_documentation(question)
    prompt_sql = vn_milvus.get_similar_question_sql(question)
    relate_ddl = vn_milvus.get_related_ddl(question)
    prompt = vn_milvus.get_sql_prompt(
        initial_prompt=EXTRACTION_PROMPT_TEMPLATE,
        question=question,
        question_sql_list=[],
        ddl_list=relate_ddl,
        doc_list=[],
    )
    logger.info(prompt)
    llm_response = vn_milvus.submit_prompt(prompt)
    logger.info(llm_response)
    # train = vn_milvus.get_training_data()

    new_prompt = vn_milvus.get_sql_prompt(
        initial_prompt=TRUEFALSE_TEMPLATE,
        question="问题: " + question + " 答案: " + llm_response,
        question_sql_list=prompt_sql,
        ddl_list=relate_ddl,
        doc_list=[],
    )
    logger.info(new_prompt)
    new_llm_response = vn_milvus.submit_prompt(new_prompt)
    logger.info(new_llm_response)
    '''
    document = vn_milvus.get_related_documentation(question)
    prompt_sql = vn_milvus.get_similar_question_sql(question)
    relate_ddl = vn_milvus.get_related_ddl(question)
    prompt = vn_milvus.get_sql_prompt(
        initial_prompt=HYPO_TEMPLATE,
        question=question,
        question_sql_list=[],
        ddl_list=relate_ddl,
        doc_list=[],
    )
    logger.info(prompt)
    llm_response = vn_milvus.submit_prompt(prompt)
    logger.info(llm_response)
    # train = vn_milvus.get_training_data()

    new_prompt = vn_milvus.get_sql_prompt(
        initial_prompt=EXTRACTION_PROMPT_TEMPLATE,
        question=question,
        question_sql_list=prompt_sql,
        ddl_list=relate_ddl,
        doc_list=[],
    )
    logger.info(new_prompt)
    new_llm_response = vn_milvus.submit_prompt(new_prompt)
    logger.info(new_llm_response)

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
            "max_tokens": 14000,
            "n_results":5
        }
    )

    vn_milvus.connect_to_mysql(host='myhost', dbname='mydbname', user='myuser', password='mypassword', port='myport')

    question = "这个月，有多少公司由于质量问题引起的产品退货情况。"

    #llm_double(vn_milvus, question)
    llm_ask(vn_milvus, question)
    #sql = vn_milvus.generate_sql(question)
    #train = vn_milvus.get_training_data()
    #vn_milvus.ask(question=question)

