import numpy
import pandas

awards_players = pandas.read_csv("basketballPlayoffs/awards_players.csv")
coaches = pandas.read_csv("basketballPlayoffs/coaches.csv")
players_teams = pandas.read_csv("basketballPlayoffs/players_teams.csv")
players = pandas.read_csv("basketballPlayoffs/players.csv")
series_post = pandas.read_csv("basketballPlayoffs/series_post.csv")
teams_post = pandas.read_csv("basketballPlayoffs/teams_post.csv")
teams = pandas.read_csv("basketballPlayoffs/teams.csv")

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


