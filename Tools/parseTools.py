import argparse

# 配置参数解析
def startParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", required=True, help="必需参数: 地域英文名, ap-guangzhou")
    parser.add_argument("-c", "--cluster", default="barad", help="集群名,默认barad")
    parser.add_argument("-t", "--startTime", help="拉取指标的起始时间")
    parser.add_argument("-kt", "--kafkaType", required=True, choices=['up', 'down'], help="必需参数: 指定拉取kafka是上游还是下游")
    return parser.parse_args()

if __name__ == "__main__":
    args = startParse()