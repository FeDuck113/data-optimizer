import config
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
    n_param = len(data[0])

    f = n_exp * n_param - n_exp     #число степеней свободы

    # расчёт дисперсии адекватности
    adeq_variences = 0
    for j in range(n_param):
        adeq_variences += (sum((means[j]-data[i][j])**2 / f for i in range(n_exp)))

    #расчёт критерия Фишера
    F = adeq_variences / exp_variance

    return F


a = [[3, 9, 7, 67], [1, 7, 5, 12], [10, 17, 25, 800]]



variances, means = calculate_variance(a)
G, exp_variance = cochrans_test(variances)
print(G, exp_variance)

if G > config.G_STANDART:  #если больше табличного значения, то ряд дисперсий неоднородный
    sys.exit()

F_test(a, means, exp_variance)




