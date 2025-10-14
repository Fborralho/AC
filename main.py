import pandas as pd
from collections import defaultdict

def clean_players(players: pd.DataFrame):
    players = players.drop(['firstseason','lastseason'], axis='columns') # all players with first and last season 0
    players = players[players["bioID"].isin(players_teams["playerID"])]
    return players

def clean_players_teams(players_teams: pd.DataFrame):
    return players_teams.drop('lgID', axis='columns') # same lgID

def clean_awards_players(awards_players: pd.DataFrame):
    return awards_players.drop("lgID", axis="columns")

def clean_coaches(coaches: pd.DataFrame):
    return coaches.drop("lgID", axis="columns")

def clean_teams_post(teams_post : pd.DataFrame):
    return teams_post.drop("lgID", axis="columns")

def clean_series_post(series_post : pd.DataFrame):
    return series_post.drop(["lgIDLoser", "lgIDWinner"], axis="columns")

def clean_teams(teams : pd.DataFrame):
    return teams.drop(["lgID", "franchID", "divID", "arena", "attend", "min", "seeded", "name"], axis="columns")

def parse_player_team_data(df):
    """
    Parses the player-team-season dataset into structured Python dictionaries
    for further analysis and championship prediction.
    """
    # Step 1: Clean CSV
    df.columns = [c.strip() for c in df.columns]  # Clean column names
    df.fillna(0, inplace=True)

    # Step 2: Initialize structures
    players = defaultdict(list)        # {playerID: [{year, teamID, stats...}, ...]}
    teams_by_year = defaultdict(lambda: defaultdict(list))  # {year: {teamID: [player_stats...]}}
    
    for _, row in df.iterrows():
        playerID = row["playerID"]
        teamID = row["tmID"]
        year = int(row["year"])
        
        # Regular season stats
        season_stats = {
            "GP": row["GP"],
            "GS": row["GS"],
            "minutes": row["minutes"],
            "points": row["points"],
            "oRebounds": row["oRebounds"],
            "dRebounds": row["dRebounds"],
            "rebounds": row["rebounds"],
            "assists": row["assists"],
            "steals": row["steals"],
            "blocks": row["blocks"],
            "turnovers": row["turnovers"],
            "PF": row["PF"],
            "fgAttempted": row["fgAttempted"],
            "fgMade": row["fgMade"],
            "ftAttempted": row["ftAttempted"],
            "ftMade": row["ftMade"],
            "threeAttempted": row["threeAttempted"],
            "threeMade": row["threeMade"],
            "dq": row["dq"],
        }

        # Postseason stats
        postseason_stats = {
            "PostGP": row["PostGP"],
            "PostGS": row["PostGS"],
            "PostMinutes": row["PostMinutes"],
            "PostPoints": row["PostPoints"],
            "PostoRebounds": row["PostoRebounds"],
            "PostdRebounds": row["PostdRebounds"],
            "PostRebounds": row["PostRebounds"],
            "PostAssists": row["PostAssists"],
            "PostSteals": row["PostSteals"],
            "PostBlocks": row["PostBlocks"],
            "PostTurnovers": row["PostTurnovers"],
            "PostPF": row["PostPF"],
            "PostfgAttempted": row["PostfgAttempted"],
            "PostfgMade": row["PostfgMade"],
            "PostftAttempted": row["PostftAttempted"],
            "PostftMade": row["PostftMade"],
            "PostthreeAttempted": row["PostthreeAttempted"],
            "PostthreeMade": row["PostthreeMade"],
            "PostDQ": row["PostDQ"],
        }

        # Combined player record
        record = {
            "year": year,
            "teamID": teamID,
            "stint": row["stint"],
            **season_stats,
            **postseason_stats
        }

        # Store in both structures
        players[playerID].append(record)
        teams_by_year[year][teamID].append(record)

    print(f"Parsed {len(players)} players across {len(teams_by_year)} seasons.")
    return {"players": players, "teams_by_year": teams_by_year}

def create_points_per_game_column():
    teams["O_PPG"] = teams["o_pts"] / teams["GP"]
    return teams


if __name__ == "__main__":

    awards_players = clean_awards_players(pd.read_csv("basketballPlayoffs/awards_players.csv"))
    coaches = clean_coaches(pd.read_csv("basketballPlayoffs/coaches.csv"))
    players_teams = clean_players_teams(pd.read_csv("basketballPlayoffs/players_teams.csv"))
    players = clean_players(pd.read_csv("basketballPlayoffs/players.csv"))
    series_post = clean_series_post(pd.read_csv("basketballPlayoffs/series_post.csv"))
    teams_post = clean_teams_post(pd.read_csv("basketballPlayoffs/teams_post.csv"))
    teams = clean_teams(pd.read_csv("basketballPlayoffs/teams.csv"))

    dead_players = players[players['deathDate'] != '0000-00-00'] # players that are dead
    players_teams_data = parse_player_team_data(players_teams)

    teams = create_points_per_game_column()
    
    # for year, teams in players_teams_data["teams_by_year"].items():
    #     print(f"\n=== {year} ===")
    #     for team, players in teams.items():
    #         total_points = sum(p["points"] for p in players)
    #         print(f"{team}: {total_points:.0f} total points")




# players_teams_Y1 = players_teams[players_teams["year"] == 1]

# players_points = players_teams_Y1[players_teams_Y1["GP"] > 0]
# players_teams["PPG"] = (players_points["points"] / players_points["GP"]).round(1)

# ppg_sorted = players_teams.sort_values(by="PPG", ascending=False)

# print(ppg_sorted[["playerID", "PPG", "GP", "year"]].head(10))
# print(ppg_sorted)
# print("///////////////////--------------------------------/////////////////////////////////")

# all_teams = teams[teams["year"] == 1]
# all_teams_sorted = all_teams.sort_values(by="won", ascending=False)
# print(all_teams_sorted[["tmID", "rank", "playoff", "won", "lost"]])

# print("///////////////////--------------------------------/////////////////////////////////")

# winner = series_post[series_post["round"] == "F"]
# print(winner[["year", "tmIDWinner"]])

# teams_1 = teams[teams["year"] == 1]

# print(teams_1[["confID"]])

    # for year in range(10):
    #     print(f"Year: {year}")
    #     year_teams = teams[teams["year"] == year]
    #     teams_points = year_teams.sort_values(by="O_PPG", ascending=False)
    #     print(teams_points[["tmID", "name", "year", "O_PPG"]])
    #     print("////////////////////--------------------------------/////////////////////////////////")


