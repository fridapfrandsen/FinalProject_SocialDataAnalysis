import pandas as pd

# Load the combined dataset
df = pd.read_csv("Data/world_happiness_combined.csv")

# Convert numeric columns (some may be read as strings)
numeric_cols = ['Rank', 'Happiness Score', 'GDP per Capita', 'Social Support',
                'Healthy Life Expectancy', 'Freedom', 'Perceptions of Corruption',
                'Generosity', 'Dystopia Residual']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Basic info ---
print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Years covered: {sorted(df['Year'].unique())}")
print(f"Number of countries per year:")
print(df.groupby('Year')['Country'].nunique().to_string())

# --- Summary statistics for numeric columns ---
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(df.describe().round(3).to_string())

# --- Missing values ---
print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
missing = df.isnull().sum()
print(missing[missing > 0].to_string() if missing.any() else "No missing values!")

# --- Top 10 happiest countries (most recent year) ---
latest_year = df['Year'].max()
top10 = df[df['Year'] == latest_year].nlargest(10, 'Happiness Score')[['Country', 'Happiness Score']]
print(f"\n{'=' * 60}")
print(f"TOP 10 HAPPIEST COUNTRIES ({latest_year})")
print("=" * 60)
print(top10.to_string(index=False))

# --- Bottom 10 ---
bottom10 = df[df['Year'] == latest_year].nsmallest(10, 'Happiness Score')[['Country', 'Happiness Score']]
print(f"\n{'=' * 60}")
print(f"BOTTOM 10 LEAST HAPPY COUNTRIES ({latest_year})")
print("=" * 60)
print(bottom10.to_string(index=False))

# --- Average happiness score by year ---
print(f"\n{'=' * 60}")
print("AVERAGE HAPPINESS SCORE BY YEAR")
print("=" * 60)
print(df.groupby('Year')['Happiness Score'].mean().round(3).to_string())

# --- Correlation matrix of key factors ---
print(f"\n{'=' * 60}")
print("CORRELATION WITH HAPPINESS SCORE")
print("=" * 60)
factors = ['GDP per Capita', 'Social Support', 'Healthy Life Expectancy',
           'Freedom', 'Perceptions of Corruption', 'Generosity']
for f in factors:
    corr = df['Happiness Score'].corr(df[f])
    bar = "█" * int(abs(corr) * 30)
    print(f"  {f:<30s}  {corr:+.3f}  {bar}")
