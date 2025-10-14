import pandas as pd

def get_coaches_test_data(year : int, coaches: pd.DataFrame):
    test_coaches = coaches[coaches["year"] == year]
    return test_coaches.drop(["won","lost","post_wins","post_losses"], axis='columns')

def get_players_teams_test_data(year : int, players_teams : pd.DataFrame):
    test_players_teams = players_teams[players_teams["year"] == year]
    return test_players_teams.drop(
        ["GP","GS","minutes","points","oRebounds","dRebounds","rebounds",
         "assists","steals","blocks","turnovers","PF","fgAttempted","fgMade",
         "ftAttempted","ftMade","threeAttempted","threeMade","dq","PostGP","PostGS",
         "PostMinutes","PostPoints","PostoRebounds","PostdRebounds","PostRebounds",
         "PostAssists","PostSteals","PostBlocks","PostTurnovers","PostPF",
         "PostfgAttempted","PostfgMade","PostftAttempted","PostftMade",
         "PostthreeAttempted","PostthreeMade","PostDQ"
        ],
        axis="columns",
    )

def get_teams_test_data(year : int, teams : pd.DataFrame):
    test_teams = teams[teams["year"] == year]
    return test_teams.drop(
        ["rank","playoff","seeded","firstRound","semis","finals","o_fgm","o_fga",
         "o_ftm","o_fta","o_3pm","o_3pa","o_oreb","o_dreb","o_reb","o_asts","o_pf",
         "o_stl","o_to","o_blk","o_pts","d_fgm","d_fga","d_ftm","d_fta","d_3pm","d_3pa",
         "d_oreb","d_dreb","d_reb","d_asts","d_pf","d_stl","d_to","d_blk","d_pts","tmORB",
         "tmDRB","tmTRB","opptmORB","opptmDRB","opptmTRB","won","lost","GP","homeW",
         "homeL","awayW","awayL","confW","confL"
        ],
        axis="columns",
    )


def create_test_set_data(year : int, coaches, teams, players_teams):
    test_players_teams = get_players_teams_test_data(year, players_teams)
    test_teams = get_teams_test_data(year, teams)
    test_coaches = get_coaches_test_data(year, coaches)
    return test_players_teams, test_teams, test_coaches


