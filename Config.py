import os

from pymilvus.client.singleton_utils import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        """ logger """
        self.log_level = os.environ.get("LOG_LEVEL", "DEBUG")
        """ MODEL """
        # 大模型目前支持Qwen-72B-Chat-Int4、gpt-3.5-turbo-16k-0613, Qwen-72B-Chat-GPTQ-Int4-1.5
        self.chat_model = os.environ.get("CHAT_MODEL", "your_message")

        """ OPEN AI"""
        self.openai_key = os.environ.get("OPENAI_KEY", "your_message")
        self.openai_proxy = os.environ.get("OPENAI_PROXY", "your_message")
        self.serpapi_api_key = os.environ.get("SERPAPI_API_KEY", "your_message")
        self.openai_model = os.environ.get("OPENAI_MODEL", "your_message")
        self.openai_max_tokens = os.environ.get("OPENAI_MAX_TOKENS", 'your_message')

        """ MYSQL """
        self.mysql_host = os.environ.get('MYSQL_HOST', "your_message")
        self.mysql_port = os.environ.get('MYSQL_PORT', "your_message")
        self.mysql_user = os.environ.get('MYSQL_USER', "your_message")
        self.mysql_password = os.environ.get('MYSQL_PASSWORD', "your_message")
        self.mysql_database = os.environ.get('MYSQL_DATABASE', "your_message")
        self.mysql_url = f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        """ Milvus """
        self.milvus_host = os.environ.get('MILVUS_HOST', "your_message")
        self.milvus_port = os.environ.get('MILVUS_PORT', "your_message")
        # 集合后缀名，用于切换不同的向量模型
        self.collection_suf_name = os.environ.get("COLLECTION_SUF_NAME", "private")

        """ EMBEDDING """
        self.embedding_url = os.environ.get("EMBEDDING_URL", "your_message")
        # 向量模型维度， openai的是1536， gte_large是1024
        self.embedding_dim = int(os.environ.get("EMBEDDING_DIM", "1024"))
        self.embedding_model = os.environ.get("EMBEDDING_MODEL", "text-embedding-ada-002")
        self.rerank_model = os.environ.get("RERANK_MODEL", "bce-reranker-base_v1")
        self.rerank_url = os.environ.get("RERANK_URL", "your_message")

        """PRIVATE MODEL"""
        self.private_model_url = os.environ.get("PRIVATE_MODEL_URL", "your_message")

        """ BERT_DOCUMENT_SEGMENTATION_CONFIG """
        self.nlp_config_bert_host = os.environ.get("NLP_CONFIG_BERT_HOST", "your_message")
        self.nlp_config_bert_port = os.environ.get("NLP_CONFIG_BERT_PORT", "your_message")

        """tools key"""
        os.environ["SERPER_API_KEY"] = os.environ.get("SERPER_API_KEY", "your_message")
        os.environ["ALPHAVANTAGE_API_KEY"] = os.environ.get("ALPHAVANTAGE_API_KEY", "your_message")
        os.environ["APIFY_API_TOKEN"] = os.environ.get("APIFY_API_TOKEN", "your_message")
        os.environ["ELEVEN_API_KEY"] = os.environ.get("ELEVEN_API_KEY", "your_message")
        os.environ[
            "SCENEX_API_KEY"] = os.environ.get("SCENEX_API_KEY", "your_message")
        os.environ["OPENAI_API_KEY"] = self.openai_key

        """ ElasticSearch """
        self.es_url = os.environ.get("ES_URL", "your_message")
        self.es_api_key = os.environ.get("ES_API_KEY", "your_message==")
        self.es_index_name = os.environ.get("ES_INDEX_NAME", "knowledge_index")

cfg = Config()