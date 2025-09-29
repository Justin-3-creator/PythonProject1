import pandas as pd
import matplotlib.pyplot as plt
import sys

# 2) Defining the helper function
def find_col(df, keywords):
    candidates = []
    for col in df.columns:
        low = str(col).lower()
        if any(k in low for k in keywords):
            candidates.append(col)
    return candidates[0] if candidates else None

def main():
    # 1) Loading the two CSVs
    ghana_path = "data_de_Ghana.csv"
    ivory_path = "data_de_Coast.csv"

    # For loading DataFrames
    ghana_df = pd.read_csv(ghana_path)
    ivory_df = pd.read_csv(ivory_path)

    # 2) Detect columns
    year_col_ghana = find_col(ghana_df, ["year"])
    area_col_ghana = find_col(ghana_df, ["area", "harvest", "harvested"])

    year_col_ivory = find_col(ivory_df, ["year"])
    area_col_ivory = find_col(ivory_df, ["area", "harvest", "harvested"])

    # We check error
    if year_col_ghana is None or area_col_ghana is None:
        raise ValueError("Could not detect 'Year' or 'Area Harvested' columns in data_de_Ghana.csv.")
    if year_col_ivory is None or area_col_ivory is None:
        raise ValueError("Could not detect 'Year' or 'Area Harvested' columns in data_de_Coast.csv.")

    # 3) We clean and convert strings to numeric
    ghana_df[year_col_ghana] = pd.to_numeric(ghana_df[year_col_ghana], errors="coerce")
    ghana_df[area_col_ghana] = pd.to_numeric(ghana_df[area_col_ghana], errors="coerce")

    ivory_df[year_col_ivory] = pd.to_numeric(ivory_df[year_col_ivory], errors="coerce")
    ivory_df[area_col_ivory] = pd.to_numeric(ivory_df[area_col_ivory], errors="coerce")

    # 4) We drop rows with missing essential values
    ghana_clean = ghana_df.dropna(subset=[year_col_ghana, area_col_ghana])
    ivory_clean = ivory_df.dropna(subset=[year_col_ivory, area_col_ivory])

    # 5) Optional: Year has int just for nicer plots
    ghana_clean.loc[:, year_col_ghana] = ghana_clean[year_col_ghana].astype(int)
    ivory_clean.loc[:, year_col_ivory] = ivory_clean[year_col_ivory].astype(int)

    # 6) Optional: align years to common set
    ghana_years = set(ghana_clean[year_col_ghana].tolist())
    ivory_years = set(ivory_clean[year_col_ivory].tolist())
    common_years = sorted(list(ghana_years & ivory_years))

    if not common_years:
        common_years = sorted(list(ghana_years | ivory_years))

    ghana_plot = ghana_clean[ghana_clean[year_col_ghana].isin(common_years)]
    ivory_plot = ivory_clean[ivory_clean[year_col_ivory].isin(common_years)]

    plt.figure(figsize=(14, 10))
    plt.suptitle("Ghana vs Ivory Coast Comparative Analysis of Data")

    # Panel 1: Ghana — Yield by Year (scatter plot)
    ax1 = plt.subplot(2, 2, 1)
    ax1.scatter(ghana_plot[year_col_ghana], ghana_plot[area_col_ghana], color="magenta", alpha=0.9, s=40)
    ax1.set_title("Ghana — Yield by Year")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Yield")
    ax1.grid(True)

    # Panel 2: Ivory Coast — Yield by Year (scatter plot)
    ax2 = plt.subplot(2, 2, 2)
    ax2.scatter(ivory_plot[year_col_ivory], ivory_plot[area_col_ivory], color="cyan", alpha=0.9, s=40)
    ax2.set_title("Ivory Coast — Yield by Year")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Yield")
    ax2.grid(True)

    # Panel 3: Ghana — Area Harvested by Year (bar plot)
    ax3 = plt.subplot(2, 2, 3)
    ax3.bar(ghana_plot[year_col_ghana], ghana_plot[area_col_ghana], color="green", edgecolor="black")
    ax3.set_title("Ghana — Area Harvested by Year")
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Area Harvested (units)")
    ax3.grid(True, axis="y", linestyle="--", alpha=0.7)

    # Panel 4: Ivory Coast — Area Harvested by Year (bar plot)
    ax4 = plt.subplot(2, 2, 4)
    ax4.bar(ivory_plot[year_col_ivory], ivory_plot[area_col_ivory], color="blue", edgecolor="black")
    ax4.set_title("Ivory Coast — Area Harvested by Year")
    ax4.set_xlabel("Year")
    ax4.set_ylabel("Area Harvested (units)")
    ax4.grid(True, axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()

if __name__=="__main__":
         sys.exit(main())