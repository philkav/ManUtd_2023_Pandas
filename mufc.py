import pandas as pd
import pandas_api
# import polars as pl
# import polars_api

api = pandas_api
api_name = "pandas"


## MAIN DECLARATIONS
pandas_df = pandas_api.sanitize(pd.read_csv("dataframe.csv"))
pandas_competitions = pandas_api.split_df_by_competition(pandas_df)

# polars_df = polars_api.sanitize(pl.read_csv('dataframe.csv'))
# polars_competitions = polars_api.split_df_by_competition(polars_df)


def pandas_samples(df, competitions):
    ## Pick some cols we want to display on output
    short_cols = ["Date", "Competition", "Opponent", "Score", "W/L", "Scorers"]

    ## Show top scorer in each competition
    for comp, comp_df in competitions.items():
        print(f"\n=== Top Scorer in {comp} ===")
        print(api.get_top_scorers(comp_df, limit=5).to_string())

    ## Most MOTM
    print("\n=== Most MOTM awards ===")
    print(df['MOTM'].value_counts())

    ## Show all of Rashfords Goals
    print(f"\n=== Rashfords Goals ===")
    print(
        api.get_goalscorer_data("Rashford", competitions["All"])[short_cols].to_string(
            index=False
        )
    )

    print(f"\n=== Rashfords Goals PL ===")
    print(
        api.get_goalscorer_data("Rashford", competitions["Premier League"])[
            short_cols
        ].to_string(index=False)
    )

    """
    print(f"\n=== Man City Results ===")
    print(
        api.get_matches_by_opponent("Man City", competitions["All"])[short_cols].to_string(
            index=False
        )
    )
    """

    print(f"\n=== Home v Away Results ===")
    home_dict = df[df["Venue"] == "Old Trafford"]["W/L"].value_counts().to_dict()
    away_dict = df[df["Venue"] != "Old Trafford"]["W/L"].value_counts().to_dict()
    print(
        f"[Home Form]: Played: {sum(home_dict.values()):>2}, Wins: {home_dict['W']:>2}, Draws: {home_dict['D']:>2}, Losses: {home_dict['L']:>2}"
    )
    print(
        f"[Away Form]: Played: {sum(away_dict.values()):>2}, Wins: {away_dict['W']:>2}, Draws: {away_dict['D']:>2}, Losses: {away_dict['L']:>2}"
    )

    print(f"\n=== Best Win ===")
    print(
        competitions["All"][
            competitions["All"]["Goal Margin"]
            == competitions["All"]["Goal Margin"].max()
        ][short_cols].to_string(index=False)
    )

    print(f"\n=== Worst Defeat ===")
    print(
        competitions["All"][
            competitions["All"]["Goal Margin"]
            == competitions["All"]["Goal Margin"].min()
        ][short_cols].to_string(index=False)
    )

    ## Order results from worst to best
    """
    print(f"\n=== Results from Worst to Best ===")
    print(
        competitions["All"]
        .sort_values(by=["Goal Margin", "Man Utd Score"])[short_cols + ["Rating"]]
        .to_string(index=False)
    )
    """

    ## Get Wins v Draws v Losses as a pct
    print(f"\n=== W/D/L Percentage ===")
    wdl_pct = api.get_wdl_percentage(df)
    print(f"Win: {wdl_pct['W']:>.2f}%, Draw: {wdl_pct['D']:>.2f}%, Loss: {wdl_pct['L']:>.2f}%")

    ## Show Draws
    print("\n=== Draws ===")
    print(df[df['W/L'] == 'D'][short_cols + ["Rating"]])

    ## Show matches v the 5 other Top 6 teams
    """
    print(f"\n=== Versus Top 6 ===")
    top_6 = ['Arsenal', 'Man City', 'Liverpool', 'Spurs', 'Chelsea']
    top_6_df = df[df['Opponent'].isin(top_6)][short_cols]
    print(top_6_df.to_string(index=False))
    """

if __name__ == "__main__":
    """
    If mufc.py is executed; it will show some sample outputs
    """
    if api_name == "pandas":
        pandas_samples(pandas_df, pandas_competitions)
