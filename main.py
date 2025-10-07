import parsing

from parsing import (
    parse_player_team_data,
    parse_all_data,
    clean_players,
    clean_players_teams,
    clean_awards_players,
    clean_coaches,
    clean_teams_post,
    clean_series_post,
    clean_teams
)

if __name__ == "__main__":
    base_path = "C:\\Users\\up201\Documents\\AC\\basketballPlayoffs"

    # Load everything
    data = parse_all_data(base_path)

    # Clean data
    data["players"] = clean_players(data["players"], data["players_teams"])
    data["players_teams"] = clean_players_teams(data["players_teams"])
    data["awards_players"] = clean_awards_players(data["awards_players"])
    data["coaches"] = clean_coaches(data["coaches"])
    data["teams_post"] = clean_teams_post(data["teams_post"])
    data["series_post"] = clean_series_post(data["series_post"])
    data["teams"] = clean_teams(data["teams"])

    # Example: derived metric
    data["teams"]["O_PPG"] = data["teams"]["o_pts"] / data["teams"]["GP"]

    for year in sorted(data["teams"]["year"].unique()):
        print(f"\n=== Year {year} ===")
        year_teams = data["teams"][data["teams"]["year"] == year]
        teams_sorted = year_teams.sort_values(by="O_PPG", ascending=False)
        print(teams_sorted[["tmID", "name", "year", "O_PPG"]].head())

    print("\n Parsing and cleaning complete.")


teams["O_PPG"] = teams["o_pts"] / teams["GP"]

for year in range(10):
    print(f"Year: {year}")
    year_teams = teams[teams["year"] == year]
    teams_points = year_teams.sort_values(by="O_PPG", ascending=False)
    print(teams_points[["tmID", "name", "year", "O_PPG"]])
    print("////////////////////--------------------------------/////////////////////////////////")


def clean_players():
    players.drop('firstseason', axis='columns') # all players with first and last season 0
    players.drop('lastseason', axis='columns')
    players = players[players["bioID"].isin(players_teams["playerID"])]

def clean_players_teams():
    players_teams.drop('lgID', axis='columns') # same lgID

def clean_awards_players():
    awards_players.drop("lgID", axis="columns")

def clean_coaches():
    coaches.drop("lgID", axis="columns")

def clean_teams_post():
    teams_post.drop("lgID", axis="columns")

def clean_series_post():
    series_post.drop("lgIDWinner", axis="columns")
    series_post.drop("lgIDLoser", axis="columns")

def clean_teams():
    teams.drop("tmID", axis="columns")
    teams.drop("arena", axis="columns")
    teams.drop("attend", axis="columns")
    teams.drop("min", axis="columns")
    teams.drop("seeded", axis="columns")
    teams.drop("name", axis="columns")

dead_players = players[players['deathDate'] != '0000-00-00'] # players that are dead


