import ranking_matching
import pandas as pd


def main():
    final_with_nums = ranking_matching.mains()
    df = pd.read_csv('trial.csv')
    names = df['Name'].tolist()[1:]
    mapped_data = {key: [names[val - 1] for val in values] for key, values in final_with_nums.items()}

    print(mapped_data)
    return mapped_data

if __name__ == "__main__":
    main()