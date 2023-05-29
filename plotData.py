import pandas as pd
import matplotlib.pyplot as plt
import argparse

def load_data(input_file, fill_na=False):
    """Load data from a CSV file and perform initial preprocessing.

    Parameters:
    input_file (str): Path to the input CSV file.
    fill_na (bool): Whether to fill NA values with forward fill.

    Returns:
    pd.DataFrame: The loaded and preprocessed data.
    """
    try:
        df = pd.read_csv(input_file, na_values='NA')
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

    if fill_na:
        df.fillna(method='ffill', inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True)
    df.set_index("timestamp", inplace=True)

    return df

def plot_data(df):
    """Plot the data in the given DataFrame.

    Parameters:
    df (pd.DataFrame): The data to plot.
    """
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 1, 1)
    plt.plot(df.index, df["ping_avg"], label="Average Ping", alpha=0.7)
    plt.scatter(df.index, df["ping_avg"], label="Ping data points", alpha=0.7)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.scatter(df.index, df["download_speed"], label="Download Speed data points", alpha=0.7)
    plt.scatter(df.index, df["upload_speed"], label="Upload Speed data points", alpha=0.7)
    plt.legend()

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot network data.')
    parser.add_argument('--input', default='network_data.csv', type=str, help='Path to the input CSV file')
    parser.add_argument('--fill_na', action='store_true', help='Whether to fill NA values with forward fill')

    args = parser.parse_args()

    df = load_data(args.input, args.fill_na)
    if df is not None:
        plot_data(df)

if __name__ == "__main__":
    main()
