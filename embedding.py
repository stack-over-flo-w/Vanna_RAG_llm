import json
from typing import Union

import openai
import requests
from openai import OpenAI
from openai._base_client import SyncHttpxClientWrapper
from openai.types import CreateEmbeddingResponse

from Config import cfg


class EmbeddingApi:
    """ embedding api"""

    @staticmethod
    def get_embedding_by_text(text: Union[list[str], str], model: str = cfg.embedding_model, url: str = cfg.embedding_url):
        """
        输入字符串，利用embedding model将其转化为向量

        Parameters:
        - text Union[list, str]: 需要转化为向量的文本， 或是文本列表

        Returns:
         调用失败 ：[]
         调用成功 : 转化为的 embeddings

        Raises:
        - requests.RequestException: If there is an error with the HTTP request.
        """
        try:
            if model == 'text-embedding-ada-002':
                return EmbeddingApi.get_embedding_by_openai(text, "text-embedding-ada-002")
            if not isinstance(text, list):
                emb_text = [text]
            else:
                emb_text = text
            headers = {'Content-Type': 'application/json'}
            data = {"input_texts": emb_text,
                    "model_name": model
                    }
            response = requests.post(url, headers=headers,
                                     data=json.dumps(data))
            if response.status_code == 200:
                if isinstance(text, list):
                    embedding = response.json().get("embeddings")
                else:
                    embedding = response.json().get("embeddings")[0]
                return embedding
        except Exception as e:
            return []
        return []

    @staticmethod
    def get_embedding_by_openai(text: Union[list[str], str], model: str = cfg.embedding_model):
        """输入字符串获得向量"""
        openai.api_key = cfg.openai_key
        if cfg.openai_proxy:
            openai.proxy = cfg.openai_proxy
        proxy_params = {}
        kwargs = dict(api_key=cfg.openai_key)
        if cfg.openai_proxy:
            proxy_params = {"proxies": cfg.openai_proxy}
        if proxy_params:
            kwargs["http_client"] = SyncHttpxClientWrapper(**proxy_params)
        client = OpenAI(**kwargs)
        result: CreateEmbeddingResponse = client.embeddings.create(
            model=model,
            input=text
        )
        return result.data[0].embedding