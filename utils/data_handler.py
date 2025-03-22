import pandas as pd
import matplotlib.pyplot as plt
import os

def _clean_data(df):
    df = df.iloc[:, 1:]
    df = df.iloc[3:, :]
    column_names = df.iloc[0]
    column_names.name = 'Index'
    column_names.index.name = 'Index'
    df.columns = column_names
    df = df.iloc[2:].reset_index(drop=True)
    df = df.rename(columns={df.columns[0]: 'Country'})

    return df

def _prepare_data(df):
    short_listed_countries = ['Australia', 'United Kingdom', 'United States', 'India', 'Canada', 'New Zealand']
    df = df[df['Country'].isin(short_listed_countries)][['Country', 'Personal income tax']]
    df['Personal Income Tax %'] = df['Personal income tax'] * 100

    # Add SL column
    sl_rate = {
        'Country': "Sri Lanka",
        'Personal income tax': 0.36,
        'Personal Income Tax %': 36
    }

    df = pd.concat([pd.DataFrame([sl_rate]), df ], ignore_index=True)
    return df

def load_and_plot_histogram(xl_file="data/new_dataset/oecd_inctax_1.xlsx"):
    """
    Reads the CSV file, creates a histogram of salaries, and saves the plot as an image.
    """
    # Ensure the file exists
    if not os.path.exists(xl_file):
        print("XLSX file not found!")
        return None

    # Load data
    df = pd.read_excel(xl_file)

    df = _clean_data(df)

    df = _prepare_data(df)

    # Check if the required column exists
    if "Personal Income Tax %" not in df.columns:
        print("Missing 'Personal Income Tax %' column in excel file!")
        return None

    # Plot histogram
    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(df["Country"], df["Personal Income Tax %"], color = ['blue', 'green', 'red', 'purple', 'orange', 'cyan'])
    # Labels and Title
    plt.xlabel("Country")
    plt.ylabel("Maximum Personal Income Tax Rate (%)")
    plt.title("Comparison of Maximum Personal Income Tax Rates by Country")
    plt.ylim(0, 70)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save plot
    plot_path = "data/histogram.png"
    plt.savefig(plot_path)
    plt.close()

    return plot_path  # Return the path of the saved histogram image
