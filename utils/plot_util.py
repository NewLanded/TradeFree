import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils.constant_util import BUY, SELL, LONG, SHORT, CLONG, CSHORT


def plot_one_symbol_result(holding, bs_data, symbol):
    """

    :param holding: pd.DataFrame
                    "cash", "commission", "total", "returns", "equity_curve", "symbol_market_value_1", "symbol_close_point_1", ...
        "trade_date"
        2016-01-01   现金    手续费        总资产   当日收益   收益             个券1净值               个券1收盘价
        2016-01-02
        2016-01-03

    :param bs_data:  list
        [
            {"bs_date": datetime.datetime, "direction": BUY SELL, "quantity": 100, "price": 10.1, "symbol": "000001.SZ"}
            ...
        ]
    """
    """
    首先要创建各个子图的坐标轴，
    传入一个四元列表参数：[x,y,width,height]，用来表示这个子图坐标轴原点的x坐标、y坐标，以及宽和高。
    值得注意的是，这四个值的取值范围都是[0,1]，我们约定整个大图的左下端为原点(0,0)，右上端为(1,1)。
    那么x,y的取值就表示该子图坐标原点的横坐标值和纵坐标值占大图整个长宽的比例。而width和height则表示子图的宽和高占整个大图的宽和高的比例。
    如果不传入参数则表示选取默认坐标轴，即大图的坐标轴。
    """
    sns.set()
    sns.set_palette(sns.color_palette('dark'))

    fig = plt.figure(figsize=(12, 9))

    bs_data = pd.DataFrame(bs_data)
    if bs_data.empty:
        raise ValueError("未找到买卖数据")

    buy_data = bs_data.loc[(bs_data["direction"] == BUY) & (bs_data["symbol"] == symbol)]
    sell_data = bs_data.loc[(bs_data["direction"] == SELL) & (bs_data["symbol"] == symbol)]

    ax1 = plt.axes([0.1, 0.2, 0.8, 0.5])
    ax1.plot(holding.index, holding[symbol + "_close"], ls="-", lw=1, color='y')
    ax1.plot(buy_data["bs_date"], buy_data["price"], "o", color='r', markersize=3)
    ax1.plot(sell_data["bs_date"], sell_data["price"], "o", color='g', markersize=3)
    labels = ['close point', 'buy', "sell"]
    ax1.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title="color meaning", shadow=True, fancybox=True, labels=labels)

    ax2 = plt.axes([0.1, 0.75, 0.8, 0.2], sharex=ax1)
    ax2.plot(holding.index, holding["total"], ls="-", lw=1)
    ax2.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title="color meaning", shadow=True, fancybox=True, labels=['property'])

    ax1.grid(axis="y")
    ax2.grid(axis="y")
    plt.show()


def plot_one_symbol_result_future(holding, bs_data, symbol):
    """

    :param holding: pd.DataFrame
                    "cash", "commission", "total", "returns", "equity_curve", "symbol_market_value_1", "symbol_close_point_1", ...
        "trade_date"
        2016-01-01   现金    手续费        总资产   当日收益   收益             个券1净值               个券1收盘价
        2016-01-02
        2016-01-03

    :param bs_data:  list
        [
            {"bs_date": datetime.datetime, "direction": BUY SELL, "quantity": 100, "price": 10.1, "symbol": "000001.SZ"}
            ...
        ]
    """
    """
    首先要创建各个子图的坐标轴，
    传入一个四元列表参数：[x,y,width,height]，用来表示这个子图坐标轴原点的x坐标、y坐标，以及宽和高。
    值得注意的是，这四个值的取值范围都是[0,1]，我们约定整个大图的左下端为原点(0,0)，右上端为(1,1)。
    那么x,y的取值就表示该子图坐标原点的横坐标值和纵坐标值占大图整个长宽的比例。而width和height则表示子图的宽和高占整个大图的宽和高的比例。
    如果不传入参数则表示选取默认坐标轴，即大图的坐标轴。
    """
    sns.set()
    sns.set_palette(sns.color_palette('dark'))

    fig = plt.figure(figsize=(12, 9))

    bs_data = pd.DataFrame(bs_data)
    if bs_data.empty:
        raise ValueError("未找到买卖数据")

    long_data = bs_data.loc[(bs_data["direction"] == LONG) & (bs_data["symbol"] == symbol)]
    short_data = bs_data.loc[(bs_data["direction"] == SHORT) & (bs_data["symbol"] == symbol)]
    clong_data = bs_data.loc[(bs_data["direction"] == CLONG) & (bs_data["symbol"] == symbol)]
    cshort_data = bs_data.loc[(bs_data["direction"] == CSHORT) & (bs_data["symbol"] == symbol)]

    ax1 = plt.axes([0.1, 0.2, 0.8, 0.5])
    ax1.plot(holding.index, holding[symbol + "_close"], ls="-", lw=1, color='y')
    ax1.plot(long_data["bs_date"], long_data["price"], "o", color='r', markersize=3)
    ax1.plot(short_data["bs_date"], short_data["price"], "o", color='hotpink', markersize=3)
    ax1.plot(clong_data["bs_date"], clong_data["price"], "o", color='g', markersize=3)
    ax1.plot(cshort_data["bs_date"], cshort_data["price"], "o", color='c', markersize=3)
    labels = ['close point', 'buy', "sell"]
    ax1.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title="color meaning", shadow=True, fancybox=True, labels=labels)

    ax2 = plt.axes([0.1, 0.75, 0.8, 0.2], sharex=ax1)
    ax2.plot(holding.index, holding["total"], ls="-", lw=1)
    ax2.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title="color meaning", shadow=True, fancybox=True, labels=['property'])

    ax1.grid(axis="y")
    ax2.grid(axis="y")
    plt.show()


def plot_multi_symbol_result(holding, bs_data, symbol_list):
    """

    :param holding: pd.DataFrame
                    "cash", "commission", "total", "returns", "equity_curve", "symbol_market_value_1", "symbol_close_point_1", ...
        "trade_date"
        2016-01-01   现金    手续费        总资产   当日收益   收益             个券1净值               个券1收盘价
        2016-01-02
        2016-01-03

    :param bs_data:  list
        [
            {"bs_date": datetime.datetime, "direction": BUY SELL, "quantity": 100, "price": 10.1, "symbol": "000001.SZ"}
            ...
        ]
    """
    """
    首先要创建各个子图的坐标轴，
    传入一个四元列表参数：[x,y,width,height]，用来表示这个子图坐标轴原点的x坐标、y坐标，以及宽和高。
    值得注意的是，这四个值的取值范围都是[0,1]，我们约定整个大图的左下端为原点(0,0)，右上端为(1,1)。
    那么x,y的取值就表示该子图坐标原点的横坐标值和纵坐标值占大图整个长宽的比例。而width和height则表示子图的宽和高占整个大图的宽和高的比例。
    如果不传入参数则表示选取默认坐标轴，即大图的坐标轴。
    """
    sns.set()
    sns.set_palette(sns.color_palette('dark'))

    fig = plt.figure(figsize=(12, 9))

    bs_data = pd.DataFrame(bs_data)
    if bs_data.empty:
        raise ValueError("未找到买卖数据")

    ax1 = plt.axes([0.1, 0.2, 0.8, 0.5])
    for symbol in symbol_list:
        buy_data = bs_data.loc[(bs_data["direction"] == BUY) & (bs_data["symbol"] == symbol)]
        sell_data = bs_data.loc[(bs_data["direction"] == SELL) & (bs_data["symbol"] == symbol)]

        ax1.plot(holding.index, holding[symbol + "_close"], ls="-", lw=1)
        ax1.plot(buy_data["bs_date"], buy_data["price"], "o", color='r', markersize=3)
        ax1.plot(sell_data["bs_date"], sell_data["price"], "o", color='g', markersize=3)
    labels = ['close point', 'buy', "sell"]
    ax1.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title="color meaning", shadow=True, fancybox=True, labels=labels)

    ax2 = plt.axes([0.1, 0.75, 0.8, 0.2], sharex=ax1)
    ax2.plot(holding.index, holding["total"], ls="-", lw=1)
    ax2.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), ncol=3, title="color meaning", shadow=True, fancybox=True, labels=['property'])

    ax1.grid(axis="y")
    ax2.grid(axis="y")
    plt.show()
