import numpy as np
import pandas as pd


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
