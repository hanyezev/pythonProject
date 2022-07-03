import logging


# 配置日志,输出控制台
def loadLogConfig() -> None:
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# 配置日志,输出log文件
def loadLogConfigOutput(path='./data/test.log', filemode="a") -> None:
    LOG_FORMAT_str = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_FORMAT = logging.Formatter(LOG_FORMAT_str)
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT_str)

    # 创建一个 logging 实例
    logger = logging.getLogger()
    
    # logger添加 FileHandler，可以将日志同时也输出到控制台上（同时日志文件也会保存）
    fh = logging.FileHandler(path, mode=filemode, encoding='utf-8', delay=False)
    fh.setLevel(logging.INFO)      # 设置在控制台上输出信息的等级
    fh.setFormatter(LOG_FORMAT)
    logger.addHandler(fh)

if __name__=="__main__":
    loadLogConfigOutput(path='./data/test.log', filemode="w")
    logging.info("测试日志!")