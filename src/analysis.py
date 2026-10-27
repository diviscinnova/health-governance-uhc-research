from pathlib import Path
import zipfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr


# Project paths and study scope

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_TABLE_DIR = ROOT / "outputs" / "tables"
OUTPUT_FIGURE_DIR = ROOT / "outputs" / "figures"

for directory in [
    PROCESSED_DIR,
    OUTPUT_TABLE_DIR,
    OUTPUT_FIGURE_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


COUNTRIES = ["IDN", "MYS", "PHL", "THA", "VNM"]

COUNTRY_NAMES = {
    "IDN": "Indonesia",
    "MYS": "Malaysia",
    "PHL": "Philippines",
    "THA": "Thailand",
    "VNM": "Viet Nam",
}


# Find input ZIP files

def find_zip_file(indicator_code):
    """
    Find a World Bank ZIP archive in data/raw/ based on its indicator code.
    """
    matches = sorted(RAW_DIR.glob(f"*{indicator_code}*.zip"))

    if not matches:
        raise FileNotFoundError(
            f"No ZIP file found for {indicator_code}. "
            f"Place the downloaded archive in {RAW_DIR}."
        )

    if len(matches) > 1:
        print(
            f"Warning: multiple ZIP files found for {indicator_code}. "
            f"Using: {matches[0].name}"
        )

    return matches[0]


# Read an indicator from ZIP

def load_world_bank_indicator(
    zip_path,
    indicator_code,
    value_name
):
    """
    Read the non-metadata CSV for one World Bank indicator,
    convert it from wide to long format, and retain the five countries.
    """

    with zipfile.ZipFile(zip_path, "r") as archive:
        csv_candidates = [
            name
            for name in archive.namelist()
            if indicator_code in name
            and name.lower().endswith(".csv")
            and "metadata" not in name.lower()
        ]

        if not csv_candidates:
            raise FileNotFoundError(
                f"No data CSV found for {indicator_code} in {zip_path.name}."
            )

        csv_name = csv_candidates[0]

        print(f"Reading {csv_name} from {zip_path.name}")

        with archive.open(csv_name) as file:
            data_wide = pd.read_csv(file, skiprows=4)

    required_columns = [
        "Country Name",
        "Country Code",
        "Indicator Name",
        "Indicator Code",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data_wide.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in {indicator_code}: {missing_columns}"
        )

    data_long = data_wide.melt(
        id_vars=required_columns,
        var_name="year",
        value_name=value_name,
    )

    data_long["year"] = pd.to_numeric(
        data_long["year"],
        errors="coerce",
    )

    data_long[value_name] = pd.to_numeric(
        data_long[value_name],
        errors="coerce",
    )

    data_long = data_long[
        data_long["Country Code"].isin(COUNTRIES)
    ].copy()

    data_long = data_long.dropna(
        subset=["year", value_name]
    ).copy()

    return data_long


# Prepare and merge datasets

def prepare_dataset():
    """
    Load both indicators, merge them by country and year,
    remove duplicate country-year records, and select the latest
    year with complete observations for all five countries.
    """

    corruption_zip = find_zip_file("GOV_WGI_CC_SC")
    uhc_zip = find_zip_file("SH_UHC_SCI")

    corruption = load_world_bank_indicator(
        zip_path=corruption_zip,
        indicator_code="GOV_WGI_CC_SC",
        value_name="corruption_control_score",
    )

    uhc = load_world_bank_indicator(
        zip_path=uhc_zip,
        indicator_code="SH_UHC_SCI",
        value_name="uhc_service_coverage",
    )

    corruption = corruption[
        [
            "Country Name",
            "Country Code",
            "year",
            "corruption_control_score",
        ]
    ].copy()

    uhc = uhc[
        [
            "Country Code",
            "year",
            "uhc_service_coverage",
        ]
    ].copy()

    data = corruption.merge(
        uhc,
        on=["Country Code", "year"],
        how="inner",
    )

    data = data.rename(
        columns={
            "Country Name": "country",
        }
    )

    data["country"] = data["Country Code"].map(
        COUNTRY_NAMES
    ).fillna(data["country"])

    # The source files may produce identical duplicate rows.
    data = data.drop_duplicates(
        subset=["Country Code", "year"]
    ).copy()

    complete_year_counts = (
        data.groupby("year")["Country Code"]
        .nunique()
    )

    common_years = complete_year_counts[
        complete_year_counts == len(COUNTRIES)
    ].index

    if len(common_years) == 0:
        raise ValueError(
            "No year contains complete data for all five countries."
        )

    selected_year = int(max(common_years))

    final_data = data[
        data["year"] == selected_year
    ].copy()

    final_data = final_data.sort_values(
        by="corruption_control_score",
        ascending=False,
    ).reset_index(drop=True)

    expected_countries = set(COUNTRIES)
    observed_countries = set(final_data["Country Code"])

    if observed_countries != expected_countries:
        raise ValueError(
            "The selected year does not contain exactly the five "
            "expected countries."
        )

    return final_data, selected_year


# Statistical analysis

def calculate_statistics(data):
    """
    Calculate Pearson and Spearman correlations.
    """

    x = data["corruption_control_score"]
    y = data["uhc_service_coverage"]

    pearson_r, pearson_p = pearsonr(x, y)
    spearman_rho, spearman_p = spearmanr(x, y)

    statistics = pd.DataFrame(
        {
            "analysis": [
                "Pearson correlation",
                "Spearman correlation",
            ],
            "coefficient": [
                pearson_r,
                spearman_rho,
            ],
            "p_value": [
                pearson_p,
                spearman_p,
            ],
            "n": [
                len(data),
                len(data),
            ],
        }
    )

    return statistics


# Save tables

def save_tables(data, statistics, selected_year):
    """
    Save the analytical dataset and correlation results.
    """

    final_path = (
        PROCESSED_DIR
        / f"final_{selected_year}.csv"
    )

    output_table_path = (
        OUTPUT_TABLE_DIR
        / f"final_{selected_year}.csv"
    )

    statistics_path = (
        OUTPUT_TABLE_DIR
        / f"correlations_{selected_year}.csv"
    )

    data.to_csv(final_path, index=False)
    data.to_csv(output_table_path, index=False)
    statistics.to_csv(statistics_path, index=False)

    print(f"Saved processed data: {final_path}")
    print(f"Saved output table: {output_table_path}")
    print(f"Saved statistics: {statistics_path}")


# Create figures

def create_uhc_bar_chart(data, selected_year):
    """
    Create a bar chart of UHC Service Coverage by country.
    """

    plot_data = data.sort_values(
        by="uhc_service_coverage",
        ascending=False,
    )

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        plot_data["country"],
        plot_data["uhc_service_coverage"],
    )

    plt.ylabel(
        "UHC Service Coverage Index (0–100)"
    )

    plt.xlabel("Country")

    plt.title(
        f"UHC Service Coverage, {selected_year}"
    )

    plt.ylim(0, 100)
    plt.xticks(rotation=30)

    for bar in bars:
        value = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.0f}",
            ha="center",
            va="bottom",
        )

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.tight_layout()

    output_path = (
        OUTPUT_FIGURE_DIR
        / f"uhc_by_country_{selected_year}.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Saved figure: {output_path}")


def create_scatterplot(data, selected_year):
    """
    Create a scatterplot of corruption control and UHC coverage.
    """

    plt.figure(figsize=(8, 5))

    plt.scatter(
        data["corruption_control_score"],
        data["uhc_service_coverage"],
        s=120,
    )

    for _, row in data.iterrows():
        plt.annotate(
            row["country"],
            (
                row["corruption_control_score"],
                row["uhc_service_coverage"],
            ),
            xytext=(5, 5),
            textcoords="offset points",
        )

    plt.xlabel(
        "Control of Corruption score (0–100)"
    )

    plt.ylabel(
        "UHC Service Coverage Index (0–100)"
    )

    plt.title(
        "Control of Corruption and UHC Service Coverage "
        f"in Southeast Asia, {selected_year}"
    )

    plt.grid(alpha=0.3)
    plt.tight_layout()

    output_path = (
        OUTPUT_FIGURE_DIR
        / f"governance_vs_uhc_{selected_year}.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Saved figure: {output_path}")


# Main workflow

def main():
    """
    Run the complete analysis.
    """

    final_data, selected_year = prepare_dataset()

    statistics = calculate_statistics(
        final_data
    )

    print("\nFinal analytical dataset:")
    print(final_data.to_string(index=False))

    print("\nCorrelation results:")
    print(statistics.to_string(index=False))

    save_tables(
        data=final_data,
        statistics=statistics,
        selected_year=selected_year,
    )

    create_uhc_bar_chart(
        data=final_data,
        selected_year=selected_year,
    )

    create_scatterplot(
        data=final_data,
        selected_year=selected_year,
    )

    print(
        f"\nAnalysis completed successfully for {selected_year}."
    )


if __name__ == "__main__":
    main()