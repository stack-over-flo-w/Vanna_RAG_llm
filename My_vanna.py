import os

from vanna.milvus import Milvus_VectorStore
from vanna.openai import OpenAI_Chat
from vanna.vannadb import VannaDB_VectorStore

os.environ["OPENAI_API_KEY"] = "sk-***********"

class VannaMilvus(Milvus_VectorStore, OpenAI_Chat):
    def __init__(self, client, config=None):
        Milvus_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)
