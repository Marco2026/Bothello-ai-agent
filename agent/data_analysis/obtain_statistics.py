import pandas as pd
import matplotlib.pyplot as plt

def load_final_outcomes_by_full_board(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    
    pos_cols = [c for c in df.columns if c != 'current_player_won']

    final_movements_indexes = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        values = [row[col] for col in pos_cols]
        zero_count = 0

        for v in values:
            if v == 0:
                zero_count += 1

        if zero_count == 58:
            final_movements_indexes.append(i - 1)
        
    final_movements_indexes.append(len(df) - 1)
    print(f"Final movements indexes: {final_movements_indexes}")
    selected = df.iloc[final_movements_indexes].copy()
    # print(f"Selected rows in dataframe: {selected.shape[0]}")
    # print("row X in dataframe corresponds to row X+2 in the original CSV file")

    counts = selected['current_player_won'].value_counts().reindex([-1, 0, 1], fill_value=0)
    counts.index = ['Loss', 'Draw', 'Win']

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
