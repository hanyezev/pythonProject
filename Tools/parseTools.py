import argparse

# 配置参数解析
def startParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", required=True, help="必需参数: 地域英文名, ap-guangzhou")
    parser.add_argument("-c", "--cluster", default="barad", help="集群名,默认barad")
    parser.add_argument("-iId", "--instanceId", default="", help="实例id,默认为空,存在多个时需指定")
    parser.add_argument("-sId", "--setId", default="", help="set集群id,默认为空,存在多个时需指定")
    parser.add_argument("-n", "--namespace", required=True, help="必需参数: namespace")
    parser.add_argument("-p", "--parallelism", default=8, help="flink并行度,默认为8")
    parser.add_argument("-t", "--startTime", help="拉取指标的起始时间")
    parser.add_argument("-g", "--groupId", default="flinkpre", help="kafka消费组id,默认flinkpre,必须和当前现网flink流的id不同")
    parser.add_argument("-kt", "--kafkaType", required=True, choices=['up', 'down'], help="必需参数: 指定拉取kafka是上游还是下游")

    # 过滤参数
    parser.add_argument("-fn", "--fieldName", help="flink-capture过滤参数: fieldName")
    parser.add_argument("-ms", "--measurement", help="flink-capture过滤参数: measurement")
    parser.add_argument("-tw", "--timeWindow", help="flink-capture过滤参数: timeWindow")
    parser.add_argument("-tk", "--tagKeys", help="flink-capture过滤参数: tagKeys")
    parser.add_argument("-tv", "--tagValues", help="flink-capture过滤参数: tagValues")
    parser.add_argument("-km", "--kafkaTime", help="flink-capture过滤参数: kafkaTime")
    parser.add_argument("-lt", "--latenessTime", help="flink-capture过滤参数: latenessTime")
    parser.add_argument("-cs", "--compareSignal", choices=['greater', 'less'], help="flink-capture过滤参数: compareSignal")

    return parser.parse_args()

if __name__ == "__main__":
    args = startParse()