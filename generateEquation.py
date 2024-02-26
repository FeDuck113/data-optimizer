import json


def generate_products(num: int) -> list:
    combs = dict()
    for i in range(num):
        for j in range(num):
            new_comb = f'x{i+1}x{j+1}'
            new_comb_name = tuple(sorted((i+1, j+1)))
            if i != j and new_comb_name not in combs:
                combs[new_comb_name] = new_comb

    for i in range(1,num+1):
        new_combs = dict()
        for j in combs:
            if i not in j:
                new_comb_name = tuple(sorted(j + (i,)))
                if not new_comb_name in combs:
                    new_combs[new_comb_name] = ''.join([f'x{t}' for t in new_comb_name])
        combs.update(new_combs)

    return list(combs.values())


with open('config.json', encoding="utf-8") as f:
    config = json.load(f)

coef = eval(config['coefficients'])
combs = generate_products(len(eval(config["input_data"]["EXP_DATA"]["PARAMETERS"])[0]))


equat = str(coef[0])
for i in range(len(combs)):
    if coef[i+1] != 0:
        if coef[i+1] < 0:
            equat += str(coef[i + 1]) + combs[i]
        else:
            equat += '+' + str(coef[i+1]) + combs[i]
print(equat)
