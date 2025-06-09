import pandas as pd
import matplotlib.pyplot as plt

def load_final_outcomes_by_full_board(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    pos_cols = [c for c in df.columns if c != 'current_player_won']
    full_board = df[(df[pos_cols] != 0).all(axis=1)]
    resultados = {"Loss": 0, "Draw": 0, "Win": 0}
    for _, row in full_board[pos_cols].iterrows():
        count1 = (row == 1).sum()
        count2 = (row == 2).sum()
        
        if count1 == count2:
            resultados["Draw"] += 1
        elif count1 > count2:
            resultados["Loss"] += 1
        else:
            resultados["Win"] += 1

    counts = pd.Series(resultados, index=["Loss", "Draw", "Win"])
    return counts

def plot_final_outcomes(counts):
    plt.figure(figsize=(6,4))
    colors = ['#e74c3c', '#f1c40f', '#2ecc71']
    plt.bar(counts.index, counts.values, color=colors)
    plt.xlabel('Outcome')
    plt.ylabel('Number of games')
    plt.title('Game Outcomes')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_path = 'agent/training/games/BOTvsAGENT_UCT.csv'
    counts = load_final_outcomes_by_full_board(csv_path)
    print(counts)
    plot_final_outcomes(counts)
