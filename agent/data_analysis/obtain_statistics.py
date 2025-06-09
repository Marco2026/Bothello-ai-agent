import pandas as pd
import matplotlib.pyplot as plt

def load_final_outcomes_by_full_board2(csv_path):
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

def load_final_outcomes_by_full_board3(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    
    df = df.iloc[2:].reset_index(drop=True)

    last_row = df.iloc[-1]
    
    pos_cols = [c for c in df.columns if c != 'current_player_won']

    final_movements_indexes = []

    for i in range(len(df)):
        row = df.iloc[i]
        values = [row[col] for col in pos_cols]
        zero_count = sum(1 for v in values if v == 0)

        if zero_count == 58 and i > 0: 
            final_movements_indexes.append(i - 1)

    selected = df.iloc[final_movements_indexes].copy()

    if not last_row.equals(selected.iloc[-1]):
        selected = pd.concat([selected, last_row.to_frame().T], ignore_index=True)

    counts = selected['current_player_won'].value_counts().reindex([-1, 0, 1], fill_value=0)
    counts.index = ['Loss', 'Draw', 'Win']

    return counts

def load_final_outcomes_by_full_board(csv_path):
    df = pd.read_csv(csv_path, delimiter=';')
    df = df.iloc[2:].reset_index(drop=True)
    
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
    print(f"Selected rows: {selected.shape[0]}")

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
    csv_path = 'agent/training/games/AGENT_UCTvsAGENT_UCT.csv'
    counts = load_final_outcomes_by_full_board2(csv_path)
    print(counts)
    plot_final_outcomes(counts)
