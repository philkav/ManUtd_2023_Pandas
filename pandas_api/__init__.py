"""
>> df
Data columns (total 17 columns):
 #   Column          Non-Null Count  Dtype
---  ------          --------------  -----
 0   Date            28 non-null     object
 1   Competition     28 non-null     category
 2   GW              28 non-null     int64
 3   Venue           28 non-null     object
 4   Opponent        28 non-null     object
 5   Man Utd Score   28 non-null     int64
 6   Opponent Score  28 non-null     int64
 7   W/L             28 non-null     object
 8   Rating          28 non-null     object
 9   Scorers         25 non-null     object
 10  PL Position     28 non-null     int64
 11  Shots MUFC      28 non-null     int64
 12  Shots Opponent  28 non-null     int64
 13  Possession      28 non-null     int64
 14  MOTM            26 non-null     object
 15  Score           28 non-null     object
 16  Goal Margin     28 non-null     int64
dtypes: category(1), int64(8), object(8)
memory usage: 3.9+ KB

>> competitions
competitions = {
    'All' : <df>,
    'Europa League Group E': <df>,
    'FA Cup': <df>,
    'League Cup': <df>,
    'Premier League': <df>
}

"""
import pandas as pd 
import pdb

def sanitize(df):
    sanitized_df = df.copy()
    sanitized_df.fillna("")
    sanitized_df["Competition"] = sanitized_df["Competition"].str.strip()
    sanitized_df["Competition"] = sanitized_df["Competition"].astype("category")
    sanitized_df["Scorers"] = sanitized_df["Scorers"].str.rstrip()
    sanitized_df["Opponent"] = sanitized_df["Opponent"].str.rstrip()
    sanitized_df["Score"] = (
        sanitized_df["Man Utd Score"].astype(str)
        + "-"
        + sanitized_df["Opponent Score"].astype(str)
    )
    sanitized_df["Goal Margin"] = (
        sanitized_df["Man Utd Score"] - sanitized_df["Opponent Score"]
    )
    return sanitized_df

def split_df_by_competition(df):
    comp_df = {"All": df}
    for competition in df["Competition"].cat.categories.to_list():
        comp_df[competition] = df[df["Competition"] == competition]
    return comp_df



def get_top_scorers(df, limit=10):
    return (
        pd.Series(
            [
                x.replace("(P)", "").strip()
                for _list in df["Scorers"].dropna().str.split(",")
                for x in _list
            ]
        )
        .value_counts()
        .head(limit)
    )


def get_goalscorer_data(player, df):
    return df[df["Scorers"].str.contains(player).fillna(False)]


def get_matches_by_opponent(opponent, df):
    return df[df["Opponent"] == opponent]

def get_wdl_percentage(df):
    df = df.copy()
    df = df[df["Venue"] == "Old Trafford"]["W/L"].value_counts()
    return df /  df.sum() * 100


