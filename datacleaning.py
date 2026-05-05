import pandas as pd
import os

# Define the common column mapping for each year
# Maps original column names -> standardized names
column_mappings = {
    2015: {
        'Country': 'Country',
        'Region': 'Region',
        'Happiness Rank': 'Rank',
        'Happiness Score': 'Happiness Score',
        'Economy (GDP per Capita)': 'GDP per Capita',
        'Family': 'Social Support',
        'Health (Life Expectancy)': 'Healthy Life Expectancy',
        'Freedom': 'Freedom',
        'Trust (Government Corruption)': 'Perceptions of Corruption',
        'Generosity': 'Generosity',
        'Dystopia Residual': 'Dystopia Residual',
    },
    2016: {
        'Country': 'Country',
        'Region': 'Region',
        'Happiness Rank': 'Rank',
        'Happiness Score': 'Happiness Score',
        'Economy (GDP per Capita)': 'GDP per Capita',
        'Family': 'Social Support',
        'Health (Life Expectancy)': 'Healthy Life Expectancy',
        'Freedom': 'Freedom',
        'Trust (Government Corruption)': 'Perceptions of Corruption',
        'Generosity': 'Generosity',
        'Dystopia Residual': 'Dystopia Residual',
    },
    2017: {
        'Country': 'Country',
        'Happiness.Rank': 'Rank',
        'Happiness.Score': 'Happiness Score',
        'Economy..GDP.per.Capita.': 'GDP per Capita',
        'Family': 'Social Support',
        'Health..Life.Expectancy.': 'Healthy Life Expectancy',
        'Freedom': 'Freedom',
        'Trust..Government.Corruption.': 'Perceptions of Corruption',
        'Generosity': 'Generosity',
        'Dystopia.Residual': 'Dystopia Residual',
    },
    2018: {
        'Country or region': 'Country',
        'Overall rank': 'Rank',
        'Score': 'Happiness Score',
        'GDP per capita': 'GDP per Capita',
        'Social support': 'Social Support',
        'Healthy life expectancy': 'Healthy Life Expectancy',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Perceptions of Corruption',
        'Generosity': 'Generosity',
    },
    2019: {
        'Country or region': 'Country',
        'Overall rank': 'Rank',
        'Score': 'Happiness Score',
        'GDP per capita': 'GDP per Capita',
        'Social support': 'Social Support',
        'Healthy life expectancy': 'Healthy Life Expectancy',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Perceptions of Corruption',
        'Generosity': 'Generosity',
    },
    2020: {
        'Country name': 'Country',
        'Regional indicator': 'Region',
        'Ladder score': 'Happiness Score',
        'Logged GDP per capita': 'GDP per Capita',
        'Social support': 'Social Support',
        'Healthy life expectancy': 'Healthy Life Expectancy',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Perceptions of Corruption',
        'Generosity': 'Generosity',
        'Dystopia + residual': 'Dystopia Residual',
    },
    2021: {
        'Country name': 'Country',
        'Regional indicator': 'Region',
        'Ladder score': 'Happiness Score',
        'Logged GDP per capita': 'GDP per Capita',
        'Social support': 'Social Support',
        'Healthy life expectancy': 'Healthy Life Expectancy',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Perceptions of Corruption',
        'Generosity': 'Generosity',
        'Dystopia + residual': 'Dystopia Residual',
    },
    2022: {
        'Country': 'Country',
        'RANK': 'Rank',
        'Happiness score': 'Happiness Score',
        'Explained by: GDP per capita': 'GDP per Capita',
        'Explained by: Social support': 'Social Support',
        'Explained by: Healthy life expectancy': 'Healthy Life Expectancy',
        'Explained by: Freedom to make life choices': 'Freedom',
        'Explained by: Perceptions of corruption': 'Perceptions of Corruption',
        'Explained by: Generosity': 'Generosity',
        'Dystopia (1.83) + residual': 'Dystopia Residual',
    },
}

# Read, rename, and combine all years
folder = "/Users/karenstentoft/Desktop/Social Data/Final projekt"
all_dfs = []

for year in range(2015, 2023):
    filepath = os.path.join(folder, f"{year}.csv")
    # 2022 uses commas as decimal separators (European format)
    if year == 2022:
        df = pd.read_csv(filepath, encoding='utf-8-sig', decimal=',')
    else:
        df = pd.read_csv(filepath, encoding='utf-8-sig')

    # Rename columns to standard names
    mapping = column_mappings[year]
    df = df.rename(columns=mapping)

    # Keep only the standardized columns that exist
    standard_cols = list(mapping.values())
    df = df[[col for col in standard_cols if col in df.columns]]

    # Add the Year column
    df['Year'] = year

    # Remove trailing asterisks from country names (footnote markers)
    df['Country'] = df['Country'].str.strip('*').str.strip()

    all_dfs.append(df)

# Combine all into one DataFrame
combined = pd.concat(all_dfs, ignore_index=True)

# Fill missing Rank by ranking within each year by Happiness Score (highest = 1)
combined['Rank'] = combined.groupby('Year')['Happiness Score'].rank(ascending=False, method='min')
combined['Rank'] = combined['Rank'].astype('Int64')

# Reorder columns so Year is first
cols = ['Year'] + [c for c in combined.columns if c != 'Year']
combined = combined[cols]

# Save to CSV
output_path = os.path.join(folder, "world_happiness_combined.csv")
combined.to_csv(output_path, index=False)

print(f"Combined {len(combined)} rows across {len(all_dfs)} years")
print(f"Saved to: {output_path}")
print(f"\nColumns: {list(combined.columns)}")
print(f"\nPreview:")
print(combined.head(10))