# 快捷键/代码片段

## 待实现

1.自动执行项目

## VSCode快捷键

1.打开设置
`Ctrl + ,`

2.搜索框
`Ctrl + P`

3.编辑器拆分
`Ctrl + \`

4.快捷键设置面板
`Ctrl + S`

## git命令

1.github上传文件
```
git username/password配置成功
git init
git add .
git commit -am "[提交信息备注]]."
git remote add origin [git项目ssh地址]
git push -u origin master
```

2.github在vscode切换分支

```
git status
查看远程: git branch -a
切换分支master: git checkout master
```

## OS

1.判断路径是否存在,没有则创建
```
if not os.path.exists(Model_dir):
    os.makedirs(Model_dir)
```

## Time

1.当前时间戳
```
time.time() # 秒级
```

2.时间戳转换为时间字符串(只支持10位)
```
# 当前时间
time.localtime()
# 时间戳对应的struct_time
struct_time = time.localtime([时间戳]) 
out = time.strftime("%Y-%m-%d %H:%M:%S.%f",struct_time)
```

## datatime
1.获取当前时间戳和当前时间字符串
```
datetime.datetime.now().timestamp()
datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
```

2.字符串转datetime格式,在转时间戳
```
date = datetime.datetime.strptime('2022-07-03 10:40:44.782489', '%Y-%m-%d %H:%M:%S.%f') # 生成datetime格式
out = date.timestamp()
```

2.时间戳转换为时间字符串(16位)
```
# 输入16位时间戳, 生成字符串或datetime格式
def fromTimestamp(timestamp, returnType="str"):
    firstTimestamp  = timestamp / 1000000
    secondTimestamp  = timestamp % 1000000
    date = datetime.datetime.fromtimestamp(firstTimestamp)
    out = date.strftime("%Y-%m-%d %H:%M:%S" + "."+ str(secondTimestamp).zfill(6))
    if returnType == "str":
        return out
    elif returnType == "datetime":
        return datetime.datetime.strptime(out, '%Y-%m-%d %H:%M:%S.%f')
    return None
```

## 博客记录

1.超详细Anaconda安装教程 
https://blog.csdn.net/qq_45344586/article/details/124028689

2.