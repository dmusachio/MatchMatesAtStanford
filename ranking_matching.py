"""
    Large picture of what this program does. Assume we have some algorithm that, given preferences of users,
    creates some ranking of all other users. So if we have 20 users, each user has ranking of other 19, (1-19):

    1. Determine Number of groups (Currently 4-5 per group)

    2. Pick random person (person 1) to be in group 1, then assign least-compatible user with person_1 to be in group 2
    and assign least compatible user between 1 and 2 to be in group 3 etc. until there is one person in each group.

    3. Use Gale-Shipley algorithm to match each group with 1 new partner. We will have to create group rankings for each
    non-group member and vice-versa. After first round, there will be 2 members in each group

    4. Recalculate rankigns and run G-S algo. Now there will be 3 people per group

    5. Recalculate rankigns and run G-S algo. Now there will be 4 people per group

    6. Recalculate group rankings and run G-S algo. There will be less non-group members than groups so after the last
    round, some groups will have 4 and some will have 5 but every user will be matched to a group

"""

import random

NUM_PEOPLE = 802
PREFFERED_SIZE_OF_GROUP = 4
NUM_GROUPS = NUM_PEOPLE // PREFFERED_SIZE_OF_GROUP
users_not_in_group = [i for i in range(1, NUM_PEOPLE + 1)]

ranking = {i: {} for i in range(1, NUM_PEOPLE + 1)}
groups = {i: [] for i in range(1, NUM_GROUPS + 1)}

def init(): #initialize rankings of each user with random values (eventually will be replaced with meaningful values)
    for i in range(1, NUM_PEOPLE + 1):
        people_to_rank = list(range(1, NUM_PEOPLE + 1))
        people_to_rank.remove(i)  # dont rank yourself
        random.shuffle(people_to_rank)
        rankings = {person_being_ranked: rank for rank, person_being_ranked in enumerate(people_to_rank, start=1)}
        ranking[i] = rankings
def find_least_compatible(list_of_users): #given a list of users, returns SEPERATE user who is least compatible with the users on the list
    sum_of_scores = {}
    for i in range(NUM_PEOPLE):
        sum_of_scores[i+1] = 0
    for user in list_of_users:
        user_ranking = ranking[user]
        for ranked_user in user_ranking.keys():
            ranking_by_user = user_ranking[ranked_user]
            if ranked_user != user:
                sum_of_scores[ranked_user] += ranking_by_user
    filtered_scores = {user: score for user, score in sum_of_scores.items() if user not in list_of_users}
    if filtered_scores:
        return max(filtered_scores, key=filtered_scores.get)
    else:
        raise Exception("OH NO! SOMETHING DID NOT GO RIGHT!")
def remove_own_rating_in_group_ratings(groups, new_group_rankings): #makes sure user doesn't rank himself
    all_members = set()
    for group_members in groups.values():
        all_members.update(group_members)
    for group in new_group_rankings.keys():
        for member in all_members:
            new_group_rankings[group].pop(member, None)
    return new_group_rankings

def get_least_compatible_users(): #finds num_people users who are least compatible with one another and puts them in seperate groups
    non_compatible_users = []
    first_user = random.randint(1,NUM_PEOPLE)
    non_compatible_users.append(first_user)
    users_not_in_group.remove(first_user)
    for i in range(NUM_GROUPS - 1):
        new_least_compatible_user = find_least_compatible(non_compatible_users)
        non_compatible_users.append(new_least_compatible_user)
        users_not_in_group.remove(new_least_compatible_user)
    for i in range(NUM_GROUPS):
        groups[i+1].append(non_compatible_users[i])
    return non_compatible_users

def group_rankings(groups): #finds overall group preferences for members in group of non-grouped members
    group_ratings = {}
    for i in range(NUM_GROUPS):
        group_ratings[i + 1] = {j + 1: 0 for j in range(NUM_PEOPLE)}
    for group in groups.keys():
        for user in groups[group]:
            for ranked_user in ranking[user].keys():
                get_ranking = ranking[user][ranked_user]
                group_ratings[group][ranked_user] += get_ranking

    remove_own_rating_in_group_ratings(groups, group_ratings)
    final_rankings = {}
    for group, ratings in group_ratings.items():
        sorted_items = sorted(ratings.items(), key=lambda item: item[1])
        final_rankings[group] = {key: rank for rank, (key, value) in enumerate(sorted_items, start=1)}
    return final_rankings

def find_score(user, group): #finds score of how much a user likes a group (higher score means less compatible)
    score = 0
    for group_member in group:
        score += ranking[user][group_member]
    return score

def rankings_of_groups(users_not_in_group): #updates the group preference of all users not in groups
    user_ranking_of_groups = {}
    user_scores_of_groups = {}
    for user in users_not_in_group:
        user_ranking_of_groups[user] = {}
        user_scores_of_groups[user] = {}
        for group in groups.keys():
            group_users = groups[group]
            user_scores_of_groups[user][group] = find_score(user, group_users)
        sorted_keys = sorted(user_scores_of_groups[user], key=user_scores_of_groups[user].get)
        user_ranking_of_groups[user] = {key: rank + 1 for rank, key in enumerate(sorted_keys)}
    return user_ranking_of_groups

"""
Gale-Shipley Algorithm (slightly modified): Imagine the Group is it's own entity with it's own rankings. 
It proposes to it's highest ranked student to join the group. If the user has no better offer, it joins
that group. Else, it joins another group and the group proposes to it's next favorite user in the next
round. Eventually, each group will get exactly 1 student (there will always be students left over)
"""
def gs_algo(groups, users_not_in_group, group_rankings, rankings_of_groups):
    free_users = set(users_not_in_group)
    proposals = {}
    successful_groups = set()
    while free_users and len(successful_groups) < len(groups):
        for group in groups.keys():
            if group not in successful_groups:
                for user in sorted(group_rankings[group], key=group_rankings[group].get):
                    if user in free_users:
                        proposals[group] = user
                        break
        for user in free_users.copy():
            preferred_group = None
            for group, proposed_user in list(proposals.items()):
                if proposed_user == user:
                    if preferred_group is None or rankings_of_groups[user][group] < rankings_of_groups[user][
                        preferred_group]:
                        preferred_group = group

            if preferred_group:
                groups[preferred_group].append(user)
                free_users.remove(user)
                successful_groups.add(preferred_group)
                break
    for group in groups.keys():
        if group not in successful_groups:
            proposals.pop(group, None)
    users_not_in_group = list(free_users)
    return groups, users_not_in_group


def run_iterations(groups, users_not_in_groups, group_rankings_func, rankings_of_groups_func): #runs GS algorithm PREFFERED_SIZE_OF_GROUP times
    for _ in range(PREFFERED_SIZE_OF_GROUP - 1):
        groups, users_not_in_groups = gs_algo(groups, users_not_in_groups, group_rankings_func(groups),
                                              rankings_of_groups_func(users_not_in_groups))
    return groups, users_not_in_groups

def assign_remaining_group_members(remaining_users_rankings_of_groups): #assigns remaining group members to their favorite groups
    assigned_groups = set()
    updated_users_not_in_group = list(remaining_users_rankings_of_groups)
    sorted_users = sorted(remaining_users_rankings_of_groups.keys(),
                          key=lambda user: len(remaining_users_rankings_of_groups[user]))
    for user in sorted_users:
        possible_groups = sorted(remaining_users_rankings_of_groups[user].items(), key=lambda item: item[1])
        for group, rank in possible_groups:
            if group not in assigned_groups:
                groups[group].append(user)
                assigned_groups.add(group)
                if user in updated_users_not_in_group:
                    updated_users_not_in_group.remove(user)
                break
    return groups, updated_users_not_in_group

def main():
    init()

    get_least_compatible_users()
    group_rankings(groups)
    rankings_of_groups(users_not_in_group)

    final_full_groups, final_users_not_in_group = run_iterations(groups, users_not_in_group, group_rankings, rankings_of_groups)

    remaining_users_ranking_of_groups = rankings_of_groups(final_users_not_in_group)
    final_set_of_groups, final_set_of_users_not_in_group = assign_remaining_group_members(remaining_users_ranking_of_groups)

    if final_set_of_users_not_in_group == []:
        print("ALL MEMBERS MATCHED")

    print(final_set_of_groups)
    return final_set_of_groups

if __name__ == "__main__":
    main()