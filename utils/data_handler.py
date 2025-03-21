import pandas as pd
import matplotlib.pyplot as plt
import os

def load_and_plot_histogram(csv_file="data/salary_data.csv"):
    """
    Reads the CSV file, creates a histogram of salaries, and saves the plot as an image.
    """
    # Ensure the file exists
    if not os.path.exists(csv_file):
        print("CSV file not found!")
        return None

    # Load data
    df = pd.read_csv(csv_file)

    # Check if the required column exists
    if "salary" not in df.columns:
        print("Missing 'salary' column in CSV file!")
        return None

    # Plot histogram
    plt.figure(figsize=(6, 4))
    plt.hist(df["salary"], bins=10, color="skyblue", edgecolor="black")
    plt.xlabel("Salary")
    plt.ylabel("Frequency")
    plt.title("Salary Distribution Histogram")
    
    # Save plot
    plot_path = "data/histogram.png"
    plt.savefig(plot_path)
    plt.close()

    return plot_path  # Return the path of the saved histogram image
