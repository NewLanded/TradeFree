import time

import pandas as pd

from risk_management.performance import create_sharpe_ratio, create_drawdowns
from utils.exception_util import EventTypeError
from utils.plot_util import plot_one_symbol_result_future
from .abs_brain import AbsBrain
from ..execution import FutureExecutionHandler
from ..portfolio import FuturePortfolio

"""
利润, 现金, 持仓等计算需要乘以百分比
"""


class FutureBrain(AbsBrain):
    def __init__(self):
        super().__init__()

    def add_bars(self, bars, start_date=None, end_date=None):
        """
        :param bars:  DataHandler instance, 需要实现 update_bars 和 get_latest_bars 方法, 需实现register_event_queue方法
        :param start_date:  datetime.datetime  开始时间
        :param end_date:  datetime.datetime  结束时间
        """
        self.bars = bars
        self.bars.register_event_queue(self.event_queue)
        self.bars.init_data(start_date, end_date)

        self.start_date = self.bars.min_index_date

    def add_portfolio(self, initial_capital=100000):
        """
        :param initial_capital:  初始现金
        """
        self.portfolio = FuturePortfolio(self.start_date, self.event_queue, self.bars, initial_capital)

    def add_execution_handler(self):
        self.broker = FutureExecutionHandler(self.event_queue, self.bars, self.portfolio)

    def add_Strategy(self, Strategy, strategy_min_days):
        self.strategy = Strategy(self.bars, self.event_queue, self.portfolio.current_positions, self.portfolio.current_holdings, strategy_min_days)

    def start(self):
        while True:
            # Update the bars (specific backtest code, as opposed to live trading)
            try:
                self.bars.update_bars()
            except StopIteration:
                break

            execute_event_type_flag = True  # 逻辑是在策略依据tick触发订单后, 订单要依据下一个tick的价格执行, 所以现在在每个tick开始时先处理上一个tick遗留的订单
            while True:
                try:
                    event = self.event_queue.pop()

                    if event.type == 'ORDER' and execute_event_type_flag is False:
                        raise EventTypeError
                except IndexError as e:
                    self.portfolio.update_timeindex()  # 以最新的价格更新持仓信息
                    break
                except EventTypeError as e:
                    self.event_queue.put(event, put_left_flag=True)
                    self.portfolio.update_timeindex()
                    break

                else:
                    if event:
                        if event.type == 'MARKET':  # 处理市场数据, 触发策略
                            execute_event_type_flag = False
                            self.strategy.calculate_signals(event)

                        elif event.type == 'SIGNAL':  # 策略执行, 触发订单
                            execute_event_type_flag = False
                            self.portfolio.update_signal(event)

                        elif event.type == 'ORDER':  # portfolio对象对订单的头寸, 风险等进行评估, 若通过, 则下单
                            self.broker.execute_order(event)

                        elif event.type == 'FILL':  # 更新持仓
                            self.portfolio.update_fill(event)

                        else:
                            raise ValueError("未知的event, event.type={0}".format(event.type))

            time.sleep(0)
            # 保证金不够强制平仓这个先不搞, 需要引入结算价格, 需要单独列出结算的tick(只在日终结算), 比较麻烦

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
        plot_one_symbol_result_future(self.equity_curve, self.portfolio.bs_data, symbol)
