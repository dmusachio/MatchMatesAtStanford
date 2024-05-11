import pandas as pd

# Load the CSV file into a DataFrame
data = pd.read_csv('trial.csv')
NUM_USERS = data.shape[0] - 1
NUM_QUESTIONS = data.shape[1] - 1


# Display the first few rows of the DataFrame to confirm it's loaded correctly
def get_table():

    data.set_index('Name', inplace=True)

    # Convert the DataFrame into a dictionary starting from the second row
    result = {i: data.iloc[i].tolist() for i in range(1, len(data))}
    converted_result = {int(k): [int(v) for v in values] for k, values in result.items()}

    return converted_result, NUM_USERS, NUM_QUESTIONS




