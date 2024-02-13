import json


def generate_products(data: list) -> dict:
    products = dict()
    for i in range(len(data)):
        for j in range(len(data)):
            new_comb = tuple(sorted((i, j)))
            if i != j and not new_comb in products:
                products[i, j] = data[i]*data[j]

    for i in range(len(data)):
        b2 = dict()
        for j in products:
            if not i in j:
                new_comb = tuple(sorted(j + (i,)))
                if new_comb not in products:
                    b2[new_comb] = products[j] * data[i]
        products.update(b2)

    return products


# calculation of variances and mean values
def calculate_variance(data: list) -> (list, list):
    n_exp = len(data)
    n_param = len(data[0]) - 1

    # calculation of the mean values for each parameter
    means = list()
    for i in range(n_param):
        means.append(sum(exp[i] for exp in data)/n_exp)

    # calculation of the variances for each parameter
    variances = list()
    for i in range(n_exp):
        variances_exp = list()
        for j in range(n_param):
            variances_exp.append((data[i][j] - means[j]) ** 2 / (n_exp - 1))
        variances.append(list(variances_exp))

    return variances, means


# calculation of cochrans_test and variance of experiment
def cochrans_test(variances: list) -> (float, float):
    n_exp = len(variances)

    max_variances = max(max(var) for var in variances)
    sum_variances = sum(sum(var) for var in variances)

    G = max_variances / sum_variances       # calculation of Cochran coefficient
    exp_variances = sum_variances/n_exp     # calculation of variance of the experiment

    return G, exp_variances


# calculation of F-test
def F_test(data: list, means: list, exp_variance: float) -> float:
    n_exp = len(data)
    n_param = len(data[0]) - 1

    f = n_exp * n_param - n_exp             # Degrees of freedom

    # calculation of the variance of adequacy
    adeq_variances = 0
    for j in range(n_param):
        adeq_variances += (sum((means[j]-data[i][j])**2 / f for i in range(n_exp)))

    F = adeq_variances / exp_variance       # calculation of F-test

    return F


# calculation of the regression coefficient
def calculate_regression_coefficients(data: list) -> list:
    n_exp = len(data)
    n_param = len(data[0]) - 1

    regression_coefficients = list()
    for i in range(n_param):
        numerator = sum(data[j][-1]*data[j][i] for j in range(n_exp))
        denominator = sum(data[j][i] ** 2 for j in range(n_exp))

        regression_coefficients.append(numerator/denominator)

    return regression_coefficients


def calculate_coefficients(data: list, G_STANDART: float, F_STANDART: float) -> list:
    for j in data:
        j.insert(0, 1)                      # adding x0

        products_num = generate_products(j[1:-1])
        for i in products_num:
            j.insert(len(j)-2, products_num[i])     # adding product of parameters

    variances, means = calculate_variance(data)     # getting variances and mean values for each parameter

    G, exp_variance = cochrans_test(variances)      # getting Cochran coefficient and variance of experiment

    # comparison with tabular data.
    # if the value is greater than the tabular ones, then the variances is non-uniform
    if G > G_STANDART:
        raise ValueError(f'The dispersion is non-uniform. G = {G}')

    F = F_test(data, means, exp_variance)
    if F > F_STANDART:
        raise ValueError(f'F is more than the table value. F = {F}')

    regression_coefficients = calculate_regression_coefficients(data)   # getting regression coefficients

    return regression_coefficients


def linear_regression(data: list, coefficients: list) -> float:
    result = coefficients[0]                        # start with a constant value
    for i in range(len(data)):
        result += coefficients[i + 1] * data[i]     # adding the remaining members
    return result


with open('config.json', encoding="utf-8") as f:
    config = json.load(f)

    CALCULATE_COEFFICIENTS = config['operating_mode']['CALCULATE_COEFFICIENTS']
    PREDICT_RESULT = config['operating_mode']['PREDICT_RESULT']

if CALCULATE_COEFFICIENTS:
    EXP_DATA = eval(config['input_data']['EXP_DATA'])

    if not EXP_DATA:
        raise ValueError('Experimental data are missing')

    coef = calculate_coefficients(EXP_DATA, config['const']['G_STANDART'], config['const']['F_STANDART'])
    with open('config.json', 'r+', encoding='utf-8') as f:
        config['coefficients'] = str(coef)
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()


if PREDICT_RESULT:
    coef = eval(config['coefficients'])
    PRED_DATA = eval(config['input_data']['PRED_DATA'])

    products_num = generate_products(PRED_DATA)
    print(PRED_DATA)
    print(products_num)
    for i in products_num:
        PRED_DATA.insert(len(PRED_DATA)-1, products_num[i])     # adding product of parameters

    print(PRED_DATA)

    if not coef:
        raise ValueError('Regression coefficients are missing')
    if not PRED_DATA:
        raise ValueError('Prediction data are missing')

    result = linear_regression(PRED_DATA, coef)
    result = round(result, config["const"]["RESULT_ACCURACY"])
    print(result)
