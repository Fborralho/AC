import pandas as pd
from collections import defaultdict

def parse_player_team_data(filepath):
    """
    Parses the player-team-season dataset into structured Python dictionaries
    for further analysis and championship prediction.
    """
    # Step 1: Load and clean CSV
    df = pd.read_csv(filepath)
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
            "league": row["lgID"],
            "stint": row["stint"],
            **season_stats,
            **postseason_stats
        }

        # Store in both structures
        players[playerID].append(record)
        teams_by_year[year][teamID].append(record)

    print(f"Parsed {len(players)} players across {len(teams_by_year)} seasons.")
    return {"players": players, "teams_by_year": teams_by_year}


if __name__ == "__main__":
    filepath = "C:\\Users\\up201\\Documents\\AC\\basketballPlayoffs\\players_teams.csv"

    data = parse_player_team_data(filepath)

    
    for year, teams in data["teams_by_year"].items():
        print(f"\n=== {year} ===")
        for team, players in teams.items():
            total_points = sum(p["points"] for p in players)
            print(f"{team}: {total_points:.0f} total points")


