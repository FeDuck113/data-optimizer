def calculate_variance(data):
    n_exp = len(data)
    n_param = len(data[0]) #мэйби -1, чтоб не учитывать результат

    #рассчёт средних значений для ка
    mean = list()
    for i in range(n_param):
        mean.append(sum(exp[i] for exp in data)/n_exp)

    #расчёт дисперсии для каждого значения параметра
    variances = list()
    for i in range(n_exp):
        variances_exp = list()
        for j in range(n_param):
            variances_exp.append((data[i][j] - mean[j]) ** 2 / (n_exp - 1))
        variances.append(list(variances_exp))

    return variances


def cochrans_test(variances):
    G = max(variances)/sum(s for s in variances)
    return G



a = [[3, 9, 7, 67], [1, 7, 5, 12], [10, 17, 25, 800]]



print((calculate_variance(a)))


