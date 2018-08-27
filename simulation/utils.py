import numpy as np

def plot_bank_and_bets(strategy):
    initial_capital = strategy.initial_capital
    net_returns = np.array(strategy.get_returns())
    returns = net_returns + 1
    returns[0] *= initial_capital
    costs = np.array(strategy.costs) * -1

    balance_progression = np.cumprod(returns)
    bar_labels = [1 if value > 0 else 0 for value in net_returns]

    net_flows = balance_progression - np.insert(balance_progression, 0, initial_capital)[:-1]
    winnnings = np.array([value if value > 0 else 0 for value in net_flows])

    figsize = (12, 6)
    colors = {0: 'r', 1: 'g'}
    fig, ax = plt.subplots(figsize=figsize)
    index = np.arange(len(costs))
    ax.bar(index, winnnings, color='g')
    ax.bar(index, costs, color='r')

    ax.set_xticks(np.arange(0, len(net_returns)))
    plt.xticks(rotation='vertical')

    plt.subplots(figsize=figsize)
    plt.xticks(np.arange(0, len(net_returns)))
    plt.xticks(rotation='vertical')
    plt.plot(balance_progression)