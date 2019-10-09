import numpy as np
import pandas as pd
from scipy.stats import norm


def create_sharpe_ratio(returns, periods=252):
    """
    以0利率作为基准(无风险利率), 计算夏普比率

    Parameters:
    returns - A pandas Series representing period percentage returns.  # pandas Series数据, 记录每单位(日)回报
    periods - Daily (252), Hourly (252*6.5), Minutely(252*6.5*60) etc.  # 年化区间
    """
    """
    日收益率为ri，平均后收益率为r。年波动率（平方）其实是日波动率（平方）【就是相对于均值的波动，为了去掉符号影响，记为（ri-r）^2。】的加总，
    然后年波动率（平方）为Σ[（ri-r）^2]。而Σ[（ri-r）^2]=n*σ^2。然后年波动率就等于σ*n^1/2
    当你说年波动率当平方是日波动率当平方的总和时，你有一个假设在背后，即每天的收益率是独立的（不相关的）, 所以你有VAR(r1+r2+r3+...+r245) = VAR(r1)+VAR(r2)+VAR(r3)+...+VAR(r245)
    
    “什么是战略的良好夏普比率?”务实地说，你应该忽略任何按年计算的夏普比率(扣除交易成本后)为S<1的策略。
    定量对冲基金倾向于忽略任何拥有夏普比率S<2的策略。
    我所熟悉的一家著名定量对冲基金在研究中甚至不会考虑夏普比率S<3的策略。
    作为一个零售算法交易员，如果你能达到夏普比率S>2，那么你做得很好。
    
    较低的夏普比率(低于1.0)意味着，为了获得最低的平均回报，投资者承受了巨大的回报波动性。负的夏普比率意味着，持有代表计算中使用的无风险利率的工具(通常是美国国债)会更好
    
    夏普比率通常会随着交易频率的增加而增加。一些高频策略的夏普比率为个位数(有时为两位数)，因为它们几乎每天都能盈利，当然每个月也能盈利。
    这些投资策略很少遭遇灾难性风险，因此将回报率的波动性降至最低，从而导致了如此高的夏普比率
    """
    return np.sqrt(periods) * ((np.mean(returns) - 0) / np.std(returns)) if np.std(returns) != 0 else 0  # np.std(returns)是日收益率的波动率, np.sqrt(periods)年化的过程, 平方根的原因是假设收益是正态随即过程


def create_drawdowns(equity_curve):
    """
    计算PnL曲线的最大峰 - 谷下降以及持续时间
    Parameters:
    pnl - A pandas Series representing period percentage returns.  # 单位收益率, pandas Series
    Returns:
    drawdown, duration
    """
    hwm = [0]
    eq_idx = equity_curve.index
    drawdown = pd.Series(index=eq_idx)
    duration = pd.Series(index=eq_idx)

    for t in range(1, len(eq_idx)):
        cur_hwm = max(hwm[t - 1], equity_curve[t])  # 至今为止收益率最高值
        hwm.append(cur_hwm)
        drawdown[t] = hwm[t] - equity_curve[t]  # 至今为止最高收益率 - 当前收益率
        duration[t] = 0 if drawdown[t] == 0 else duration[t - 1] + 1  # drawdown[t] == 0 表示当前收益率已经超过了历史最高收益率, 此时就不在回撤区间里面了
    return drawdown.max(), duration.max()


def var_cov_var(P, c, mu, sigma):
    """
    利用方差-协方差的方式计算VAR

    VaR(Value at Risk)按字面解释就是“在险价值”，其含义指：在市场正常波动下，某一金融资产或证券组合的最大可能损失。
    更为确切的是指，在一定概率水平（置信度）下，某一金融资产或证券组合价值在未来特定时期内的最大可能损失

    Parameters:
        P - 组合净值
        c - confidence interval  置信度
        mu - 日收益率平均值
        sigma - 日收益率标准差
    """
    alpha = norm.ppf(1 - c, mu, sigma)
    return P - P * (alpha + 1)
