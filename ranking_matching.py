import random
NUM_PEOPLE = 16
NUM_GROUPS = NUM_PEOPLE // 4

ranking = {i: {} for i in range(1, 17)}
groups = {i: [] for i in range(1, NUM_GROUPS + 1)}

def init():
    for i in range(1, 17):
        rankings = {}
        # Assign rankings: start from i+1 to 16, then 1 to i-1
        rank = 1
        for j in range(1, 16):
            person_being_ranked = (i + j) % 16
            person_being_ranked = 16 if person_being_ranked == 0 else person_being_ranked  # Adjust for zero index
            if person_being_ranked != i:  # Exclude ranking themselves
                rankings[person_being_ranked] = rank
                rank += 1
        ranking[i] = rankings


def find_least_compatible(list_of_users):
    sum_of_scores = {}
    for i in range(16):
        sum_of_scores[i+1] = 0


    for user in list_of_users:
        user_ranking = ranking[user]
        for ranked_user in user_ranking.keys():
            ranking_by_user = user_ranking[ranked_user]
            if ranked_user != user:
                sum_of_scores[ranked_user] += ranking_by_user

    filtered_scores = {user: score for user, score in sum_of_scores.items() if user not in list_of_users}

    if filtered_scores:  # Check if filtered_scores is not empty
        return max(filtered_scores, key=filtered_scores.get)

    else:
        print("No eligible users found.")


def get_least_compatible_users(num_people):
    num_groups = num_people // 4
    non_compatible_users = []
    non_compatible_users.append(random.randint(1,num_people))
    for i in range(num_groups - 1):
        new_least_compatible_user = find_least_compatible(non_compatible_users)
        non_compatible_users.append(new_least_compatible_user)
    for i in range(NUM_GROUPS):
        groups[i+1].append(non_compatible_users[i])

    return non_compatible_users

def group_rankings(groups):

    group_ratings = {}
    for i in range(NUM_GROUPS):
        group_ratings[i + 1] = {}

    for group in groups.keys():
        for j in range(NUM_PEOPLE):
            group_ratings[group][j+1] = 0

        for user in groups[group]:
            for ranked_user in ranking[user].keys():
                get_ranking = ranking[user][ranked_user]
                group_ratings[group][ranked_user] += get_ranking


    return group_ratings


def rankings_of_group:
    




def main():
    init() # initialize rankings
    non_compatible_users = get_least_compatible_users(NUM_PEOPLE)
    new_groups = group_rankings(groups)
    print(groups)
    print(new_groups)
    print(groups)






if __name__ == "__main__":
    main()