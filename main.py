import json


def generate_products(data: list) -> dict:
    products = dict()
    for i in range(len(data)):
        for j in range(len(data)):
            new_comb = tuple(sorted((i, j)))
            if i != j and not new_comb in products:
                products[i, j] = data[i]*data[j]

    for i in range(len(data)):
        new_products = dict()
        for j in products:
            if not i in j:
                new_comb = tuple(sorted(j + (i,)))
                if new_comb not in products:
                    new_products[new_comb] = products[j] * data[i]
        products.update(new_products)

    return products


# calculation of variances and mean values
def calculate_variance(PARAMS: list, RESULTS: list) -> list:
    n_exp = len(PARAMS)

    variances = list()
    for i in range(n_exp):
        var = 0.0
        for j in range(len(RESULTS[0])):
            var += (PARAMS[i][-1]-RESULTS[i][j])**2
        variances.append(var/2)

    return variances


# calculation of cochrans_test and variance of experiment
def cochrans_test(variances: list) -> (float, float):
    n_exp = len(variances)

    max_variances = max(variances)
    sum_variances = sum(variances)
    G = max_variances / sum_variances       # calculation of Cochran coefficient
    exp_variances = sum_variances/n_exp     # calculation of variance of the experiment

    return G, exp_variances


# calculation of F-test
def F_test(data: list, n_params: int, variances: list, exp_variance: float) -> float:
    n_exp = len(data)

    f = n_exp - (n_params + 1)                # calculation of degrees of freedom

    adeq_variances = sum(variances) / f     # calculation of variance of adequacy
    F = adeq_variances / exp_variance       # calculation of F-test

    return F


# calculation of the regression coefficient
def calculate_regression_coefficients(data: list, COEF_ACCURACY: int) -> list:
    n_exp = len(data)
    n_param = len(data[0]) - 1

    regression_coefficients = list()
    for i in range(n_param):
        numerator = sum(data[j][-1]*data[j][i] for j in range(n_exp))
        denominator = sum(data[j][i] ** 2 for j in range(n_exp))

        regression_coefficients.append(round(numerator/denominator, COEF_ACCURACY))

    return regression_coefficients


def optimize_coefficients(coef: list, exp_variance: float, T_TEST: float, n_exp: int) -> list:
    confidence_interval = (T_TEST*(exp_variance**0.5))/(n_exp**0.5)
    print('interval', confidence_interval)
    for i in range(len(coef)):
        if -1 * confidence_interval < coef[i] < confidence_interval:
            coef[i] = 0
    return coef


def calculate_coefficients(PARAMS: list, RESULTS: list, G_STANDART: float, F_STANDART: float, OPTIMIZE_COEF: bool,
                           T_TEST: float, COEF_ACCURACY: int) -> list:
    n_params = len(PARAMS[0])
    for j in range(len(PARAMS)):
        PARAMS[j].insert(0, 1)                              # adding x0
        PARAMS[j].append(sum(RESULTS[j])/len(RESULTS[j]))   # adding average result

        products_num = generate_products(PARAMS[j][1:-1])   # getting all products of parameters
        for i in products_num:                              # adding products of parameters
            PARAMS[j].insert(len(PARAMS[j])-2, products_num[i])

    variances = calculate_variance(PARAMS, RESULTS)     # getting variances and mean values for each parameter

    G, exp_variance = cochrans_test(variances)      # getting Cochran coefficient and variance of experiment

    # comparison with tabular data.
    # if the value is greater than the tabular ones, then the variances is non-uniform
    if G > G_STANDART:
        raise ValueError(f'The dispersion is non-uniform. G = {G}')

    F = F_test(PARAMS, n_params, variances, exp_variance)
    if F > F_STANDART:
        raise ValueError(f'F is more than the table value. F = {F}')

    regression_coefficients = calculate_regression_coefficients(PARAMS, COEF_ACCURACY)   # getting regression coefficients

    if OPTIMIZE_COEF:
        print(regression_coefficients)
        regression_coefficients = optimize_coefficients(regression_coefficients, exp_variance,
                                                        T_TEST, len(PARAMS))
    return regression_coefficients


def linear_regression(data: list, coefficients: list) -> float:
    products_num = generate_products(data)     # getting all products of parameters
    for i in products_num:                          # adding products of parameters
        data.insert(len(data) - 1, products_num[i])

    result = coefficients[0]                        # start with a constant value
    for i in range(len(data)):
        result += coefficients[i + 1] * data[i]     # adding the remaining parameters
    return result


def calc_coef(config: dict) -> list:
    p = config['input_data']['EXP_DATA']['PARAMETERS']
    r = config['input_data']['EXP_DATA']['RESULTS']

    PARAMS = eval(p) if isinstance(p, str) else p
    RESULTS = eval(r) if isinstance(p, str) else r

    if not PARAMS or not RESULTS:
        raise ValueError('Experimental data are missing')

    consts = config['consts']
    coef = calculate_coefficients(PARAMS, RESULTS, consts['G_STANDART'], consts['F_STANDART'], consts['OPTIMIZE_COEF'],
                                  consts['T_TEST'], consts['COEF_ACCURACY'])
    return coef

def predict_result(config: dict) -> float:
    c = config['coefficients']
    pr_data = config['input_data']['PRED_DATA']

    coef = eval(c) if isinstance(c, str) else c
    PRED_DATA = eval(pr_data) if isinstance(pr_data, str) else pr_data

    if not coef:
        raise ValueError('Regression coefficients are missing')
    if not PRED_DATA:
        raise ValueError('Prediction data are missing')

    result = linear_regression(PRED_DATA, coef)
    result = round(result, config['consts']['RESULT_ACCURACY'])
    return result


with open('config.json', encoding="utf-8") as f:
    config = json.load(f)

    CALCULATE_COEFFICIENTS = config['operating_mode']['CALCULATE_COEFFICIENTS']
    PREDICT_RESULT = config['operating_mode']['PREDICT_RESULT']

if CALCULATE_COEFFICIENTS:
    coef = calc_coef(config)
    with open('config.json', 'r+', encoding='utf-8') as f:
        config['coefficients'] = str(coef)
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

if PREDICT_RESULT:
    predict_result(config)