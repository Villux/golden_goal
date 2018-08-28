import numpy as np
import matplotlib.pyplot as plt

def plot_strategy(strategy, prefix):
    initial_capital = strategy.initial_capital
    net_returns = np.array(strategy.get_returns())
    returns = net_returns + 1
    returns[0] *= initial_capital
    costs = np.array(strategy.costs) * -1

    balance_progression = np.cumprod(returns)
    net_flows = balance_progression - np.insert(balance_progression, 0, initial_capital)[:-1]
    winnnings = np.array([value if value > 0 else 0 for value in net_flows])

    figsize = (12, 6)
    plt.subplots(figsize=figsize)
    index = np.arange(len(costs))
    plt.bar(index, winnnings, color='g')
    plt.bar(index, costs, color='r')
    plt.savefig(f"img/{prefix}_pl.png")

    plt.subplots(figsize=figsize)
    plt.plot(balance_progression)
    plt.savefig(f"img/{prefix}_progression.png")

def plot_simulation(simulation):
    plot_strategy(simulation.unit_strategy, f"unit_season_{simulation.season_id}")
    plot_strategy(simulation.kelly_strategy, f"kelly_season_{simulation.season_id}")
    plot_strategy(simulation.kelly_strategy_single, f"kelly_single_season_{simulation.season_id}")
