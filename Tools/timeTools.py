import datetime

# 16位时间戳转时间字符串
def fromTimestamp(timestamp, returnType="str"):
    firstTimestamp  = timestamp / 1000000
    secondTimestamp  = timestamp % 1000000
    date = datetime.datetime.fromtimestamp(firstTimestamp)
    out = date.strftime("%Y-%m-%d %H:%M:%S" + "."+ str(secondTimestamp).zfill(6))
    if returnType == "str":
        return out
    elif returnType == "datetime":
        return datetime.datetime.strptime(out, '%Y-%m-%d %H:%M:%S.%f')
    return "输入参数returnType错误!"

if __name__=="__main__":
    print(fromTimestamp(1656816044782489))
    print(fromTimestamp(1656816044782489, "datetime"))