# 导入需要的模块
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import time
import datetime
import os

# 处理乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False


def get_html(code, start_date, end_date, page=1, per=20):
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&page={1}&sdate={2}&edate={3}&per={4}'.format(
        code, page, start_date, end_date, per)
    rsp = requests.get(url)
    html = rsp.text
    return html


def get_fund(code, start_date, end_date, page=1, per=20):
    # 获取html
    html = get_html(code, start_date, end_date, page, per)
    soup = BeautifulSoup(html, 'html.parser')
    # 获取总页数
    pattern = re.compile('pages:(.*),')
    result = re.search(pattern, html).group(1)
    total_page = int(result)
    # 获取表头信息
    heads = []
    for head in soup.findAll("th"):
        heads.append(head.contents[0])

    # 数据存取列表
    records = []
    # 获取每一页的数据
    current_page = 1
    while current_page <= total_page:
        html = get_html(code, start_date, end_date, current_page, per)
        soup = BeautifulSoup(html, 'html.parser')
        # 获取数据
        for row in soup.findAll("tbody")[0].findAll("tr"):
            row_records = []
            for record in row.findAll('td'):
                val = record.contents
                # 处理空值
                if val == []:
                    row_records.append(np.nan)
                else:
                    row_records.append(val[0])
            # 记录数据
            records.append(row_records)
        # 下一页
        current_page = current_page + 1

    # 将数据转换为Dataframe对象
    np_records = np.array(records)
    fund_df = pd.DataFrame()
    for col, col_name in enumerate(heads):
        fund_df[col_name] = np_records[:, col]

    # 按照日期排序
    fund_df['净值日期'] = pd.to_datetime(fund_df['净值日期'], format='%Y/%m/%d')
    fund_df = fund_df.sort_values(by='净值日期', axis=0, ascending=True).reset_index(drop=True)
    fund_df = fund_df.set_index('净值日期')

    # 数据类型处理
    fund_df['单位净值'] = fund_df['单位净值'].astype(float)
    fund_df['累计净值'] = fund_df['累计净值'].astype(float)
    fund_df['日增长率'] = fund_df['日增长率'].str.strip('%').astype(float)
    return fund_df


def get_today_fund(code):
    url = f"http://fundgz.1234567.com.cn/js/{code}.js"
    rsp = requests.get(url)
    html = rsp.text
    out = re.search(".*({.*\}).*", html)[1]
    dict = eval(out)
    return dict


def save_pic(fund_df, end_date, today_rate, name):
    # 绘图
    pic_path = "./pic"
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)

    today_danwei_val = fund_df["单位净值"][-1] * (1 + today_rate / 100)
    today_leiji_val = fund_df["累计净值"][-1] * (1 + today_rate / 100)

    fund_df.index.append(pd.Index([end_date]))
    fund_df.loc[end_date, '单位净值'] = [today_danwei_val]
    fund_df.loc[end_date, '累计净值'] = [today_leiji_val]
    fund_df.loc[end_date, '日增长率'] = [today_rate]
    fund_df.loc[end_date, '申购状态'] = [fund_df["申购状态"][-2]]
    fund_df.loc[end_date, '赎回状态'] = [fund_df["赎回状态"][-2]]
    fund_df.loc[end_date, '分红送配'] = [fund_df["分红送配"][-2]]
    fund_df.index = pd.to_datetime(fund_df.index).date
    # print(fund_df)
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex="col")
    fund_df['单位净值'][-15:].plot(title="Average NAV", ax=axes[0], rot=30)
    fund_df['累计净值'][-15:].plot(title="Accumulated Net", ax=axes[1], rot=30)
    plt.savefig("{}/{}.jpg".format(pic_path, name))
    plt.show()


def compute_rate(code, start_date, end_date):
    """
    计算从买入日期到当前的增长率
    """
    # 字符串转时间戳
    # time_stamp = time.mktime(time.strptime(start_date, '%Y-%m-%d'))
    # 时间戳加上10天转字符串==>end_date
    # end_date = time.strftime("%Y-%m-%d", time.localtime(time_stamp + offset))
    # 获取起始基金DataFrame
    fund_df = get_fund(code, start_date=start_date, end_date=end_date)
    # print(fund_df)

    # 获取起步净值
    first_val = float(fund_df["单位净值"][0])  # 刚买时的净值
    three_day_val = float(fund_df["单位净值"][-3])  # 3天前的净值
    seven_day_val = float(fund_df["单位净值"][-7])  # 7天前的净值
    bmonth_day_val = float(fund_df["单位净值"][-15])  # 15天前的净值
    # print("First's fund is:", first_val)
    # 获取当前值
    get_msg = get_today_fund(code)
    # print(get_msg)
    end_val = float(get_msg["gsz"])
    # print("Today's fund is:", end_val)
    # 获取增长率
    cha_rate = round((end_val - first_val) / first_val * 100, 2)
    cha_rate_3 = round((end_val - three_day_val) / three_day_val * 100, 2)
    cha_rate_7 = round((end_val - seven_day_val) / seven_day_val * 100, 2)
    cha_rate_15 = round((end_val - bmonth_day_val) / bmonth_day_val * 100, 2)
    # print(f'增长率计算: ({end_val}-{first_val})/{first_val} * 100 = {cha_rate}%')
    # 获取今天的涨跌幅
    today_rate = float(get_msg["gszzl"])
    # name = get_msg["name"]

    # 绘图
    save_pic(fund_df, end_date, today_rate, code)

    return cha_rate, cha_rate_3, cha_rate_7, cha_rate_15, today_rate


def Caltime(date1, date2):
    """
    计算两个日期的相差的天数
    """
    date1 = time.strptime(date1, '%Y-%m-%d')
    date2 = time.strptime(date2, '%Y-%m-%d')

    date1 = datetime.date(date1[0], date1[1], date1[2])
    date2 = datetime.date(date2[0], date2[1], date2[2])
    return (date2 - date1).days


def main():
    # 更改基金信息即可
    my_msg = {
        "华夏能源革新股票A": ("003834", "2020-11-10"),
        "天弘中证银行ETF联接C": ("001595", "2020-06-05"),
        "华安沪深300量化增强A": ("000312", "2020-05-08"),
        "招商中证白酒指数A": ("161725", "2020-07-24"),
        "招商安心收益债券": ("217011", "2020-08-09"),
        "嘉实稳华纯债债券A": ("004544", "2020-12-21"),
        "嘉实中证锐联基本面50指数A": ("160716", "2020-06-29"),
    }
    # offset = 10 * 24 * 60 * 60  # 10天

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    email_msg = []
    i = 0
    keys = []
    for k in my_msg.keys():
        try:
            i += 1
            rate, rate_3, rate_7, rate_15, t_rate = compute_rate(my_msg[k][0], my_msg[k][1], today)
            if t_rate > 2.5 or t_rate < -1:
                s = f"{i}.<font color='#FF0000'>{k}%</font>: 购入后增长率 {rate}%, 购入时长: {my_msg[k][1]}~{today} ==> {Caltime(my_msg[k][1], today)}" \
                    f"天, 今天的涨幅: <font color='#FF0000'>{t_rate}%, 3天: {rate_3}%, 7天: {rate_7}%, " \
                    f"15天: {rate_15}%, 请注意!</font>"
            else:
                s = f"{i}.{k}: 购入后增长率 {rate}%, 购入时长: {my_msg[k][1]}~{today} ==> {Caltime(my_msg[k][1], today)}" \
                    f"天, 今天的涨幅: {t_rate}%, 3天: {rate_3}%, 7天: {rate_7}%, 15天: {rate_15}%"
            email_msg.append(s)
            keys.append(my_msg[k][0])
        except Exception as e:
            print(e)
        # break

    from send_email import send_mail

    body_content = """
    <html><p>
    购买基金信息:
    <br>&nbsp;&nbsp;&nbsp;&nbsp;{}
    <img src="cid:{}" alt="{}" height="600" width="750">
    <br>&nbsp;&nbsp;&nbsp;&nbsp;{}
    <img src="cid:{}" alt="{}" height="600" width="750">
    <br>&nbsp;&nbsp;&nbsp;&nbsp;{}
    <img src="cid:{}" alt="{}" height="600" width="750">
    <br>&nbsp;&nbsp;&nbsp;&nbsp;{}
    <img src="cid:{}" alt="{}" height="600" width="750">
    <br>&nbsp;&nbsp;&nbsp;&nbsp;{}
    <img src="cid:{}" alt="{}" height="600" width="750">
    <br>&nbsp;&nbsp;&nbsp;&nbsp;{}
    <img src="cid:{}" alt="{}" height="600" width="750">
    <br>&nbsp;&nbsp;&nbsp;&nbsp;{}
    <img src="cid:{}" alt="{}" height="600" width="750">
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    <br><hr>
    By Chalor<br>
    </p><html>
    """.format(email_msg[0], keys[0], keys[0],
               email_msg[1], keys[1], keys[1],
               email_msg[2], keys[2], keys[2],
               email_msg[3], keys[3], keys[3],
               email_msg[4], keys[4], keys[4],
               email_msg[5], keys[5], keys[5],
               email_msg[6], keys[6], keys[6])

    send_mail("每日基金NEWS", body_content, my_msg)
    print(f"***** {today} 基金日志 *****")
    for i in email_msg:
        print(i)
    print("\n")


if __name__ == '__main__':
    # 1.定时方案1
    # while True:
    #     hour = datetime.datetime.now().hour
    #     minute = datetime.datetime.now().minute
    #     if hour == 6 and minute == 50:
    #         main()
    #         time.sleep(100)
    #         continue
    #     else:
    #         pass
    # 2.定时方案2
    main()
    print("Over")
    # 画图
    # fig, axes = plt.subplots(nrows=2, ncols=1)
    # fund_df[['单位净值', '累计净值']].plot(ax=axes[0])
    # fund_df['日增长率'].plot(ax=axes[1])
    # plt.show()
