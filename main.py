import config as c
import sys

def calculate_variance(data):
    n_exp = len(data)
    n_param = len(data[0]) - 1 #мэйби -1, чтоб не учитывать результат

    #рассчёт средних значений для ка
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

    G = max_variances / sum_variances       #Коэффициент Кохрена
    exp_variances = sum_variances/n_exp     #дисперсия экспиримента

    return G, exp_variances

def F_test(data, means, exp_variance):
    n_exp = len(data)
    n_param = len(data[0]) - 1

    f = n_exp * n_param - n_exp     #число степеней свободы

    # расчёт дисперсии адекватности
    adeq_variences = 0
    for j in range(n_param):
        adeq_variences += (sum((means[j]-data[i][j])**2 / f for i in range(n_exp)))

    #расчёт критерия Фишера
    F = adeq_variences / exp_variance

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

def linear_regression(data, coefficients):
    predicted_result = coefficients[0]
    for i in range(len(data)):
        predicted_result += coefficients[i + 1] * data[i]
    return predicted_result


def calculate_coefficients(data):
    variances, means = calculate_variance(data)
    G, exp_variance = cochrans_test(variances)

    if G > c.G_STANDART:  #если больше табличного значения, то ряд дисперсий неоднородный
        print(f'The dispersion is non-uniform. G = {G}')
        sys.exit()

    F = F_test(data, means, exp_variance)
    if F > c.F_STANDART:
        print(f'F is more than the table value. F = {F}')
        sys.exit()

    regression_coefficients = calculate_regression_coefficients(data)

    return regression_coefficients


if c.CALCULATE_COEFFICIENTS:
    coef = calculate_coefficients(c.EXP_DATA)
    with open(c.COEF_FILE, 'w') as f:
        f.write(str(coef))
    f.close()

if c.PREDICT_RESULT:
    with open(c.COEF_FILE) as f:
        coef = f.readline()
    f.close()
    coef = coef.replace('[','').replace(']','')
    coef = list(map(float, coef.split(', ')))
    print(linear_regression(c.PRED_DATA, coef))





