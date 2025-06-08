import pandas as pd
import matplotlib.pyplot as plt

def load_final_outcomes_by_full_board(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    pos_cols = [c for c in df.columns if c != 'current_player_won']
    full_board = df[(df[pos_cols] != 0).all(axis=1)]
    counts = full_board['current_player_won'].value_counts().reindex([-1, 0, 1], fill_value=0)
    counts.index = ['Loss', 'Draw', 'Win']
    return counts

def plot_final_outcomes(counts):
    plt.figure(figsize=(6,4))
    colors = ['#e74c3c', '#f1c40f', '#2ecc71']
    plt.bar(counts.index, counts.values, color=colors)
    plt.xlabel('Outcome')
    plt.ylabel('Number of games')
    plt.title('Game Outcomes (Full Board States)')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_path = 'agent/training/games/AGENT_UCTvsBOT.csv'
    counts = load_final_outcomes_by_full_board(csv_path)
    print(counts)
    plot_final_outcomes(counts)
