import time

import pandas as pd

from risk_management.performance import create_sharpe_ratio, create_drawdowns
from utils.plot_util import plot_one_symbol_result, plot_multi_symbol_result
from .abs_brain import AbsBrain
from ..execution import SimulatedExecutionHandler
from ..portfolio import SimplePortfolio


class BaseBrain(AbsBrain):
    def __init__(self, bars, start_date, end_date, initial_capital):
        """
        :param bars:  DataHandler instance, 需要实现 update_bars 和 get_latest_bars 方法, 需实现register_event_queue方法
        :param start_date:  datetime.datetime  开始时间
        :param end_date:  datetime.datetime  结束时间
        :param initial_capital:  初始现金
        """
        super().__init__()
        self.bars = bars
        self.bars.register_event_queue(self.event_queue)
        self.bars.init_data(start_date, end_date)

        self.portfolio = SimplePortfolio(start_date, self.event_queue, self.bars, initial_capital)
        self.broker = SimulatedExecutionHandler(self.event_queue)

    def add_Strategy(self, Strategy):
        self.strategy = Strategy(self.bars, self.event_queue, self.portfolio.current_positions, self.portfolio.current_holdings)

    def start(self):
        while True:
            # Update the bars (specific backtest code, as opposed to live trading)
            try:
                self.bars.update_bars()
            except StopIteration:
                break

            while True:
                try:
                    event = self.event_queue.pop()
                except IndexError as e:
                    self.portfolio.update_timeindex()  # 以最新的价格更新持仓信息
                    break
                else:
                    if event:
                        if event.type == 'MARKET':  # 处理市场数据, 触发策略
                            self.strategy.calculate_signals(event)  # 回测的时候, 资金管理在这里比较方便(下单总是成功), 因为策略可能和可用资金有关联, 实盘的时候, 是否可以在update_fill处理, 或者新加一个strategy中的方法, 更新策略数据中的持仓

                        elif event.type == 'SIGNAL':  # 策略执行, 触发订单
                            self.portfolio.update_signal(event)

                        elif event.type == 'ORDER':  # portfolio对象对订单的头寸, 风险等进行评估, 若通过, 则触发 下单
                            self.broker.execute_order(event)

                        elif event.type == 'FILL':  # 处理交易费用等并真实下单
                            self.portfolio.update_fill(event)

                        else:
                            raise ValueError("未知的event, event.type={0}".format(event.type))

            time.sleep(0)

        self.create_equity_curve_dataframe()

    def create_equity_curve_dataframe(self):
        """
        创建一个数据体, 记录holding, 对后面数据分析有用
        """
        curve = pd.DataFrame(self.portfolio.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0 + curve['returns']).cumprod()
        self.equity_curve = curve

    def output_summary_stats(self):
        """
        展示收益统计信息
        """
        total_return = self.equity_curve['equity_curve'][-1]
        returns = self.equity_curve['returns']
        pnl = self.equity_curve['equity_curve']

        sharpe_ratio = create_sharpe_ratio(returns)
        max_dd, dd_duration = create_drawdowns(pnl)

        avg_hold_cost_percent = sum([i["total"] - i["cash"] for i in self.portfolio.all_holdings]) / sum([i["total"] for i in self.portfolio.all_holdings])  # 平均持仓成本比例

        stats = [("Total Return", "%0.2f%%" % ((total_return - 1.0) * 100.0)),
                 ("Sharpe Ratio", "%0.2f" % sharpe_ratio),
                 ("Max Drawdown", "%0.2f%%" % (max_dd * 100.0)),
                 ("Drawdown Duration", "%d" % dd_duration),
                 ("avg_hold_cost_percent", "{0:.2}".format(avg_hold_cost_percent))]
        print(stats)
        return stats

    def plot_one_symbol(self, symbol):
        plot_one_symbol_result(self.equity_curve, self.portfolio.bs_data, symbol)

    def plot_multi_symbol(self, symbol_list):
        plot_multi_symbol_result(self.equity_curve, self.portfolio.bs_data, symbol_list)
