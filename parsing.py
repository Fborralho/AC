import os
import pandas as pd
from collections import defaultdict


# =========================================================
#                   Load All CSVs
# =========================================================
def parse_all_data(base_path):
    """
    Loads all basketball CSV datasets into pandas DataFrames and returns them
    as a dictionary. Then parses key files (players, teams, series, etc.)
    into structured Python dicts for deeper analysis.
    """
    csv_files = {
        "awards_players": "awards_players.csv",
        "coaches": "coaches.csv",
        "players": "players.csv",
        "players_teams": "players_teams.csv",
        "series_post": "series_post.csv",
        "teams": "teams.csv",
        "teams_post": "teams_post.csv"
    }

    data = {}
    for name, filename in csv_files.items():
        filepath = os.path.join(base_path, filename)
        if not os.path.exists(filepath):
            print(f"Missing file: {filepath}")
            continue
        df = pd.read_csv(filepath)
        df.columns = [c.strip() for c in df.columns]
        df.fillna(0, inplace=True)
        data[name] = df
        print(f" Loaded {name}: {len(df)} records.")

    print("\n All data loaded successfully.")

    # Parse key structures
    structured_data = {
        "players": parse_players(data["players"]),
        "teams": parse_teams(data["teams"]),
        "players_teams": parse_players_teams(data["players_teams"]),
        "series_post": parse_series_post(data["series_post"]),
        "coaches": parse_coaches(data["coaches"]),
        "awards_players": parse_awards_players(data["awards_players"]),
        "teams_post": parse_teams_post(data["teams_post"])
    }

    return {"raw": data, "structured": structured_data}


# =========================================================
#    PARSING FUNCTIONS — turn CSVs into structured dicts
# =========================================================

def parse_players(df):
    """
    Parses players.csv → {playerID: {nameFirst, nameLast, college, birthDate, deathDate, ...}}
    """
    players = {}
    for _, row in df.iterrows():
        players[row["bioID"]] = {
            "firstName": row.get("nameFirst", ""),
            "lastName": row.get("nameLast", ""),
            "college": row.get("college", ""),
            "birthDate": row.get("birthDate", ""),
            "deathDate": row.get("deathDate", ""),
            "height": row.get("height", 0),
            "weight": row.get("weight", 0),
            "position": row.get("pos", ""),
            "firstSeason": row.get("firstseason", 0),
            "lastSeason": row.get("lastseason", 0)
        }
    return players


def parse_teams(df):
    """
    Parses teams.csv → {year: {teamID: {stats}}}
    """
    teams_by_year = defaultdict(dict)
    for _, row in df.iterrows():
        year, tmID = int(row["year"]), row["tmID"]
        teams_by_year[year][tmID] = {
            "name": row.get("name", ""),
            "confID": row.get("confID", ""),
            "divID": row.get("divID", ""),
            "rank": row.get("rank", 0),
            "playoff": row.get("playoff", ""),
            "won": row.get("won", 0),
            "lost": row.get("lost", 0),
            "GP": row.get("GP", 0),
            "O_PPG": row.get("o_pts", 0) / row["GP"] if row["GP"] else 0,
            "D_PPG": row.get("d_pts", 0) / row["GP"] if row["GP"] else 0,
            "margin": (row.get("o_pts", 0) - row.get("d_pts", 0)) / row["GP"] if row["GP"] else 0,
        }
    return teams_by_year


def parse_players_teams(df):
    """
    Parses players_teams.csv → 
      players[playerID] = [{year, teamID, stats}]
      teams_by_year[year][teamID] = [playerStats...]
    """
    players = defaultdict(list)
    teams_by_year = defaultdict(lambda: defaultdict(list))

    for _, row in df.iterrows():
        playerID = row["playerID"]
        teamID = row["tmID"]
        year = int(row["year"])

        stats = {col: row[col] for col in df.columns if col not in ["playerID", "tmID", "lgID", "year", "stint"]}
        record = {
            "year": year,
            "teamID": teamID,
            "league": row["lgID"],
            "stint": row["stint"],
            **stats
        }

        players[playerID].append(record)
        teams_by_year[year][teamID].append(record)

    return {"players": players, "teams_by_year": teams_by_year}


def parse_series_post(df):
    """
    Parses series_post.csv → {year: [ {round, tmIDWinner, tmIDLoser, ...}, ... ]}
    """
    series_by_year = defaultdict(list)
    for _, row in df.iterrows():
        year = int(row["year"])
        series_by_year[year].append({
            "round": row["round"],
            "tmIDWinner": row["tmIDWinner"],
            "tmIDLoser": row["tmIDLoser"],
            "wins": row["wins"],
            "losses": row["losses"]
        })
    return series_by_year


def parse_coaches(df):
    """
    Parses coaches.csv → {coachID: [{year, teamID, won, lost, ...}, ...]}
    """
    coaches = defaultdict(list)
    for _, row in df.iterrows():
        coachID = row["coachID"]
        record = {col: row[col] for col in df.columns if col not in ["coachID"]}
        coaches[coachID].append(record)
    return coaches


def parse_awards_players(df):
    """
    Parses awards_players.csv → {playerID: [ {award, year, note}, ... ]}
    """
    awards = defaultdict(list)
    for _, row in df.iterrows():
        playerID = row["playerID"]
        awards[playerID].append({
            "award": row["award"],
            "year": row["year"],
            "note": row.get("note", "")
        })
    return awards


def parse_teams_post(df):
    """
    Parses teams_post.csv → {year: {teamID: {wins, losses, o_pts, d_pts, etc.}}}
    """
    teams_post_by_year = defaultdict(dict)
    for _, row in df.iterrows():
        year, tmID = int(row["year"]), row["tmID"]
        teams_post_by_year[year][tmID] = {
            "wins": row.get("wins", 0),
            "losses": row.get("losses", 0),
            "o_pts": row.get("o_pts", 0),
            "d_pts": row.get("d_pts", 0),
            "GP": row.get("GP", 0),
            "O_PPG": row.get("o_pts", 0) / row["GP"] if row["GP"] else 0,
            "D_PPG": row.get("d_pts", 0) / row["GP"] if row["GP"] else 0,
        }
    return teams_post_by_year


# =========================================================
#           Optional Cleaning Utilities
# =========================================================
def clean_players(players_df, players_teams_df):
    players_df = players_df.drop(['firstseason', 'lastseason'], axis='columns', errors='ignore')
    return players_df[players_df["bioID"].isin(players_teams_df["playerID"])]

def clean_players_teams(players_teams_df):
    return players_teams_df.drop('lgID', axis='columns', errors='ignore')

def clean_awards_players(awards_players_df):
    return awards_players_df.drop("lgID", axis="columns", errors='ignore')

def clean_coaches(coaches_df):
    return coaches_df.drop("lgID", axis="columns", errors='ignore')

def clean_teams_post(teams_post_df):
    return teams_post_df.drop("lgID", axis="columns", errors='ignore')

def clean_series_post(series_post_df):
    return series_post_df.drop(["lgIDWinner", "lgIDLoser"], axis="columns", errors='ignore')

def clean_teams(teams_df):
    return teams_df.drop(["arena","attend","min","seeded","name"], axis="columns", errors='ignore')
