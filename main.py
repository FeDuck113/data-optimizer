import config as c
import json


def calculate_variance(data):
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


def cochrans_test(variances):
    n_exp = len(variances)

    max_variances = max(max(var) for var in variances)
    sum_variances = sum(sum(var) for var in variances)

    G = max_variances / sum_variances       # calculation of Cochran coefficient
    exp_variances = sum_variances/n_exp     # calculation of variance of the experiment

    return G, exp_variances


# calculation of F-test
def F_test(data, means, exp_variance):
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
def calculate_regression_coefficients(data):
    n_exp = len(data)
    n_param = len(data[0]) - 1

    regression_coefficients = list()
    for i in range(n_param):
        numerator = sum(data[j][-1]*data[j][i] for j in range(n_exp))
        denominator = sum(data[j][i] ** 2 for j in range(n_exp))

        regression_coefficients.append(numerator/denominator)

    return regression_coefficients


def calculate_coefficients(data):
    for j in data:
        j.insert(0, 1)                      # adding x0

        product_num = 1
        for i in j[1:len(j)-1]:
            product_num *= i

        j.insert(len(j)-2, product_num)     # adding x1*x2

    variances, means = calculate_variance(data)     # getting variances and mean values for each parameter

    G, exp_variance = cochrans_test(variances)      # getting Cochran coefficient and variance of experiment

    # comparison with tabular data.
    # if the value is greater than the tabular ones, then the variances is non-uniform
    if G > c.G_STANDART:
        raise ValueError(f'The dispersion is non-uniform. G = {G}')

    F = F_test(data, means, exp_variance)
    if F > c.F_STANDART:
        raise ValueError(f'F is more than the table value. F = {F}')

    regression_coefficients = calculate_regression_coefficients(data)   # getting regression coefficients

    return regression_coefficients


def linear_regression(data, coefficients):
    result = coefficients[0]                        # начинаем с константного члена
    for i in range(len(data)):
        result += coefficients[i + 1] * data[i]     # добавляем остальные члены
    return result


with open('config.json', encoding="utf-8") as f:
    config = json.load(f)

    CALCULATE_COEFFICIENTS = config['operating_mode']['CALCULATE_COEFFICIENTS']
    PREDICT_RESULT = config['operating_mode']['PREDICT_RESULT']

if CALCULATE_COEFFICIENTS:
    coef = calculate_coefficients(eval(config['input_data']['EXP_DATA']))
    with open('config.json', 'r+', encoding='utf-8') as f:
        config['coefficients'] = str(coef)
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

if PREDICT_RESULT:
    coef = eval(config['coefficients'])
    print(linear_regression(eval(config['input_data']['PRED_DATA']), coef))
