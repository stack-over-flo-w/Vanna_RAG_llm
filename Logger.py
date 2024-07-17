#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
from types import FrameType
from typing import cast

from loguru import logger as _logger

from Config import cfg
from Singleton import Singleton


class Logger(metaclass=Singleton):

    def __init__(self):
        self.formatter = "<green>{time:YYYY-MM-DD HH:mm:ss}</green>|<cyan>{file}</cyan>:<cyan>{line}</cyan>｜<cyan>{level}</cyan>: {message}"
        self.formatter = self.formatter.replace('\n', '<nl>')
        self.logger = _logger
        self.logger.remove()
        self.logger.add(sys.stderr, format=self.formatter, level=cfg.log_level)

        # 日志文件设置
        log_dir = os.path.join(os.path.dirname(__file__), "../logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_path_all = os.path.join(log_dir, f'{time.strftime("%Y-%m-%d")}.log')
        log_path_info = os.path.join(log_dir, f'{time.strftime("%Y-%m-%d")}_info.log')
        log_path_error = os.path.join(log_dir, f'{time.strftime("%Y-%m-%d")}_error.log')
        # 添加日志文件设置
        self.logger.add(log_path_all, format=self.formatter, rotation="00:00", retention="1 days", enqueue=True)
        self.logger.add(log_path_info, format=self.formatter, rotation="00:00", retention="1 days", enqueue=True, level='INFO')
        self.logger.add(log_path_error, format=self.formatter, rotation="00:00", retention="1 days", enqueue=True, level='ERROR')

    @property
    def debug(self):
        return self.logger.debug

    @property
    def info(self):
        return self.logger.info

    @property
    def warning(self):
        return self.logger.warning

    @property
    def error(self):
        return self.logger.error

    def message(self, role, message):
        """
        打印LLM消息日志
        Args:
            role: role of the llm message
            message: message content

        Returns: None

        """
        message = message.replace("{", "{{").replace("}", "}}").replace("<", "\<")
        mes_str = f"<green>{role}</green>: <cyan>{message}</cyan>\n"
        self.logger.opt(raw=True, colors=True, record=True).info("<green>{record[time]:YYYY-MM-DD HH:mm:ss}</green>｜<cyan>{record[level]}</cyan>: " + mes_str)

    def assistant(self, message):
        """
        打印LLM消息日志
        Args:
            message: message content
        Returns: None

        """
        self.message("assistant", message)

    def prompt(self, message):
        """
        打印LLM消息日志
        Args:
            message: message content
        Returns: None

        """
        self.message("prompt", message)

    def stream(self, message):
        """
        这是一个流式输出的方法，使用 enqueue=True 使其在异步队列中排队
        """
        self.logger.opt(raw=True).info(message)
        self.logger.opt(raw=True).info("\n")


class InterceptHandler(logging.Handler):
    """
    添加自定义系统级日志处理器
    """
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = _logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        _logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


def init_config():
    """
    替换Uvicorn的日志处理器
    """
    logger_names = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

    # change handler for default uvicorn logger
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in logger_names:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]

    # 修改ppocr日志
    logging.getLogger("ppocr").handlers = [InterceptHandler()]

# 定义通用日志模块
logger = Logger()
