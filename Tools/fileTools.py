

# 加载数据为字符串
def load_data(path) -> str:
    s = ""
    with open(path,'r') as f:
        for line in f:
            s += line
    f.close
    return s

# 写入数据
def write_data(path, key):
    s = ""
    with open(path,'a') as f:
        f.write(str(key) + "\n")
    f.close

# 解析字符串为json数组
def parse_data(s):
    globals = {
        "false": False,
        "true": True,
    }
    jsonList = eval(s, globals)
    return jsonList