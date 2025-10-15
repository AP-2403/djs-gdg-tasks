import itertools

squad_data = {
    'Virat Kohli': {'S': ['Chase_master', 'fast_bowling_destroyer', 'fielding'], 'W': ['left_arm_spin']},
    'Rahul': {'S': ['opener', 'power_play', 'wicketkeeping'], 'W': ['pressure', 'death_bowling']},
    'Bumrah': {'S': ['death_bowling', 'yorkers', 'economy'], 'W': ['batting']},
    'Jadeja': {'S': ['power_hitting', 'off_spin', 'fielding'], 'W': []},
    'Maxwell': {'S': ['spin_bowling', 'fielding', 'finisher'], 'W': ['pace_bounce', 'consistency']},
    'Siraj': {'S': ['swing_bowling', 'new_ball'], 'W': ['batting']},
    'Shreyas': {'S': ['middle_order', 'spin_hitter'], 'W': ['express_pace', 'short_ball']},
    'Chahal': {'S': ['leg_spin', 'wicket_taker'], 'W': ['fielding', 'batting', 'expensive']},
    'DK': {'S': ['finisher', 'wicketkeeping', 'experience'], 'W': ['poor_wicketkeeping']},
    'Faf': {'S': ['opener', 'experience', 'fielding'], 'W': ['slow_starter']}
}


def calculate_score(team_names):
    all_strengths = set()
    all_weaknesses = set()

    for player in team_names:
        profile = squad_data.get(player, {'S': [], 'W': []})
        all_strengths.update(profile['S'])
        all_weaknesses.update(profile['W'])

    total_unique_strengths = len(all_strengths)
    total_unique_weaknesses = len(all_weaknesses)
    net_score = total_unique_strengths - total_unique_weaknesses

    return {
        'net_score': net_score,
        'unique_strengths': all_strengths,
        'unique_weaknesses': all_weaknesses
    }

def find_team(k):

    players = list(squad_data.keys())
    best_score = -float('inf')
    best_teams = []

    for team_tuple in itertools.combinations(players, k):
        team = list(team_tuple)
        score_data = calculate_score(team)
        current_score = score_data['net_score']

        if current_score > best_score:
            best_score = current_score
            best_teams = [team]
        elif current_score == best_score:
            best_teams.append(team)

    return best_teams, best_score


print("--- IPL Dream Team Challenge Solver ---")
num=int(input("Enter Team size: "))

best_teams_num, best_score_num = find_team(num)
score_data_num = calculate_score(best_teams_num[0])

print(f"\n Best Team(s) Found for k = {num}:")
print(f"   Net Score: {best_score_num}")
print(f"   One Optimal Team: {best_teams_num[0]}")
print(f"   Total Unique Strengths: {len(score_data_num['unique_strengths'])}")
print(f"   Total Unique Weaknesses: {len(score_data_num['unique_weaknesses'])}")

