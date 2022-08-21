def get_cup_rule_b(cup):
    b = {"hellmouth": [3], "pseudo": [3, 5, 7], "toroidal": [3], "star": [2], "klein": [3]}
    return b[cup]


def get_cup_rule_s(cup):
    s = {
        "hellmouth": [2, 3],
        "pseudo": [2, 3, 8],
        "toroidal": [2, 3],
        "star": [3, 4, 5],
        "klein": [2, 3],
    }
    return s[cup]

def get_cup_rule_c(cup):
    c = {
        "star": 4
    }
    return c[cup]

