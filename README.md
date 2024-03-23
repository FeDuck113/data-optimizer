![dataOptimizer](https://github.com/FeDuck113/data-optimizer/assets/71590602/f495b98b-cba4-4552-b1f9-64a0ec79b854)
# Data optimizer

This program is designed for the analysis of experimental data, calculation of regression coefficients, and prediction of experiment results  
  
The program is developed in Python without the use of third-party libraries except for the standard json library for working with JSON files. It includes methods for statistical data analysis, tests for homogeneity of variance and model adequacy and linear regression

## Getting started

1. Install Python and download the source code of the program

2. Put your data and work parameters into a [json-file](##Json-file)

3. Run main.py

4. Obtain the results of data analysis, regression coefficients and predicted values of experiments

## Json-file
The json file includes input data, regression coefficients and job settings.
### Operating mode
In "operating_mode" select the necessary operating modes of the program:
* **"CALCULATE_COEFFICIENTS"** is responsible for calculating the regression coefficients based on the ***experimental data*** ("EXP_DATA")
* **"PREDICT_RESULT"** is responsible for predicting the result based on the ***parameters*** ("PRED_DATA") and ***regression coefficients***

### Input data
* **"EXP_DATA"** contains experimental data
  * "PARAMETERS" - array of parameters for each experiment
  * "RESULTS" - array of results for each experiment. It can contain several values for each experiment if several experiments were conducted with the same values. But the number of results for each experiment **has to be the same** 
* **"PRED_DATA"** contains the parameters for which the result will be predicted

### Coefficients
The array contains the linear regression coefficients, which are recorded here after they have been calculated

### Consts
* **"G_STANDART"** - the tabular value of the Cochran criterion
* **"F_STANDART"** - the tabular value of the Fisher criterion
* **"OPTIMIZE_COEF"** - responsible for removing insignificant coefficients (which are included in the confidence interval)
* **"T_TEST"** - the tabular value of the Student's t-test
* **"COEF_ACCURACY"** - the number of decimal places in the coefficients
* **"RESULT_ACCURACY"** - the number of decimal places in the result

### Example
```json
{
    "operating_mode": {
        "CALCULATE_COEFFICIENTS": true,
        "PREDICT_RESULT": false
    },
    "input_data": {
        "EXP_DATA": {
            "PARAMETERS": "[[-1,-1,-1,-1], [-1,-1,-1,1], [-1,1,-1,1], [-1,1,-1,-1], [-1,1,1,1], [-1,1,1,-1], [1,1,-1,-1], [1,1,-1,1], [1,1,1,-1],[1,1,1,1],[-1,-1,1,-1], [-1,-1,1,1], [1,-1,-1,-1], [1,-1,-1,1],[1,-1,1,-1],[1,-1,1,1]]",
            "RESULTS": "[[0.87,0.86,0.85], [0.75,0.75,0.76], [0.84,0.82,0.83], [0.87,0.88,0.88], [0.38,0.36,0.35], [0.75,0.77,0.77], [0.93,0.95,0.92], [0.88,0.87,0.87], [0.87,0.88,0.87], [0.87,0.88,0.86], [0.29,0.32,0.30], [0.16,0.14,0.15], [0.86,0.87,0.87], [0.83,0.84,0.82], [0.80,0.78,0.77], [0.74,0.73,0.75]]"
        },
        "PRED_DATA": "[-1,-1,-1,-1]"
    },
    "coefficients": "[0.729375, 0.116875, 0.068542, -0.123542, -0.027292, 0.093958, 0.035208, 0.043125, 0, -0.021875, -0.029375, 0, 0.028125, 0, 0.023125, -0.053125]",
    "consts": {
        "G_STANDART": 0.33,
        "F_STANDART": 3.63,
        "OPTIMIZE_COEF": true,
        "T_TEST": 5.841,
        "COEF_ACCURACY": 6,
        "RESULT_ACCURACY": 2
    }
}
```
## Add-ons
### Equation generator
Can write a linear regression equation. For this you need to have the coefficients and "PRED_DATA" to determine the number of parameters (x).
The coefficients equal to zero are not taken into account
```
y = 0.729375+0.116875x1x2+0.068542x1x3-0.123542x1x4-0.027292x2x3+0.093958x2x4+0.035208x3x4+0.043125x1x2x3-0.021875x1x3x4-0.029375x2x3x4
```

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).


