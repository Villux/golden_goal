import numpy as np
import matplotlib.pyplot as plt
from utils import write_as_json

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

def plot_probabilities_against_market(simulation_probabilities, market_probabilities, filename):
    for k, label in enumerate(["home", "draw", "away"]):
        simu_prob = [prob[k] for prob in simulation_probabilities]
        market_prob = [prob[k] for prob in market_probabilities]

        figsize = (12, 6)
        plt.subplots(figsize=figsize)
        plt.plot(simu_prob, label="Simulation", alpha=0.7)
        plt.plot(market_prob, label="Market", alpha=0.7)
        plt.legend()
        plt.ylim(0, 1)
        plt.ylabel('Probability')
        plt.xlabel('Match')
        plt.savefig(f'img/{label}_{filename}.svg')

        data = {
            "simulation_avg": np.mean(simu_prob),
            "simulation_std": np.std(simu_prob),
            "market_avg": np.mean(market_prob),
            "market_std": np.std(market_prob),
            "corr": np.corrcoef(simu_prob, market_prob).tolist()
        }

        write_as_json(data, f"img/meta/{label}_{filename}_probability_comparison")
