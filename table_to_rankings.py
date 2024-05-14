import random
def get_score(question_tuple, user1_response, user2_response):
    if question_tuple[1] == 1: # score 1-5
        dif = abs(user1_response - user2_response)
        if dif == 4:
            return question_tuple[2]
        elif dif == 3:
            return question_tuple[2] * .75
        elif dif == 2:
            return question_tuple[2] * .5
        elif dif == 1:
            return question_tuple[2] * .25
        else:
            return 0
    elif question_tuple[1] == 2: # score 0 or 1
        if user1_response != user2_response:
            return question_tuple[2]
        else:
            return 0
    elif question_tuple[1] == 3:
        if user1_response == user2_response:
            return question_tuple[2]
        else:
            return 0


def sim_score(user1, user2, question_types_and_values, num_questions, answers):
    score = 0
    for i in range(1, num_questions + 1):
        test = get_score(question_types_and_values[i - 1], answers[user1][i - 1], answers[user2][i - 1])
        score += test
    return score


def remap(d):
    items = list(d.items())
    random.shuffle(items)

    items.sort(key=lambda x: x[1])

    ranks = {}
    current_rank = 1
    for key, value in items:
        if value not in ranks:
            ranks[value] = current_rank
        else:
            current_rank = ranks[value] + 1
            ranks[value] = current_rank
        d[key] = current_rank
        current_rank += 1

    return d



def get_user_rankings(num_questions, num_users, answers, question_types_and_values):
    scores = {}
    for i in range(1, num_users + 1):
        scores[i] = {}
        for j in range(1, num_users + 1):

            if i != j:
                scores[i][j] = sim_score(i, j, question_types_and_values, num_questions, answers)
        remap(scores[i])

    return scores