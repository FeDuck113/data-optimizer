import config as c

def calculate_variance(data):
    n_exp = len(data)
    n_param = len(data[0]) - 1

    #рассчёт средних значений для каждого параметра
    means = list()
    for i in range(n_param):
        means.append(sum(exp[i] for exp in data)/n_exp)

    #расчёт дисперсии для каждого значения параметра
    variances = list()
    for i in range(n_exp):
        variances_exp = list()
        for j in range(n_param):
            variances_exp.append((data[i][j] - means[j]) ** 2 / (n_exp - 1))
        variances.append(list(variances_exp))

    return variances, means

def cochrans_test(variances):    #добавить рассчёт дисперсии адекватности
    n_exp = len(variances)

    max_variances = max(max(var) for var in variances)
    sum_variances = sum(sum(var) for var in variances)

    G = max_variances / sum_variances       #calculation of Cochran coefficient
    exp_variances = sum_variances/n_exp     #calculation of variance of the experiment

    return G, exp_variances

def F_test(data, means, exp_variance):
    n_exp = len(data)
    n_param = len(data[0]) - 1

    f = n_exp * n_param - n_exp     #число степеней свободы

    # расчёт дисперсии адекватности
    adeq_variences = 0
    for j in range(n_param):
        adeq_variences += (sum((means[j]-data[i][j])**2 / f for i in range(n_exp)))

    F = adeq_variences / exp_variance       #calculation of F-test

    return F

#расчёт коэффициентов регрессии
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
        j.insert(0, 1)                      #adding x0

        product_num = 1
        for i in j[1:len(j)-1]:
            product_num *= i

        j.insert(len(j)-2, product_num)     #adding x1*x2

    variances, means = calculate_variance(data)

    #comparison with tabular data
    G, exp_variance = cochrans_test(variances)

    if G > c.G_STANDART:  #если больше табличного значения, то ряд дисперсий неоднородный
        raise ValueError(f'The dispersion is non-uniform. G = {G}')

    F = F_test(data, means, exp_variance)
    if F > c.F_STANDART:
        raise ValueError(f'F is more than the table value. F = {F}')

    regression_coefficients = calculate_regression_coefficients(data)

    return regression_coefficients


def linear_regression(data, coefficients):
    result = coefficients[0]                        # начинаем с константного члена
    for i in range(len(data)):
        result += coefficients[i + 1] * data[i]     # добавляем остальные члены
    return result


if c.CALCULATE_COEFFICIENTS:
    coef = calculate_coefficients(c.EXP_DATA)
    with open(c.COEF_FILE, 'w') as f:
        f.write(str(coef))

if c.PREDICT_RESULT:
    with open(c.COEF_FILE) as f:
        coef = f.readline()

    coef = eval(coef)

    print(linear_regression(c.PRED_DATA, coef))