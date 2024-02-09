## Overview  

The goal of this project is to predict forces experienced by Robots in a system. There are two major components to this project. 

1. Jupyter notebooks to analyse data and train our model to predict force. 
2. A Python dotnet API to make a prediction in realtime 

The follow text in this readme will describe the make up of component 2. For a detalied explationation of model methodology and results see notebooks in `Jupyter/` directory. 

## API Functions 
This API contains two functions `create` to add new records to our database and `predict` to make a realtime prediction for a fresh set of features. These functions have been deployed to Azure running on the free tier API. 

I chose to make these API's in order to demonstarate that when the model is completed it can be queried on demand instantly. Additianlly, when a new data is created it can be posted to Azure and added to a cosmos db. This data can then be queried later in order to retrain our model. In a kind of ciricualr pipline. 

### Create

`POST https://machina-labs-ml.azurewebsites.net/api/Create` 

example body:
```json
{
    "data" : {
        "id": "038a1002-e861-4a19-8db7-184cc6780539",
        "a_enc_1": -4.9511,
        "b_enc_1": 0.0183,
        "c_enc_1": -0.0719,
        "x_enc_1": 213.6337,
        "y_enc_1": 324.1015,
        "z_enc_1": 895.3528,
        "a_enc_2": -154.9772,
        "b_enc_2": 0.2023,
        "c_enc_2": -179.8798,
        "x_enc_2": 22.3221,
        "y_enc_2": 783.1761,
        "z_enc_2": -772.5771,
        "fx_1": -2.326357,					
        "fy_1": 9.639795,
        "fz_1": -32.645949,
        "fx_2": 11.805614,
        "fy_2": 18.656085,
        "fz_2": -12.831012
    }
}
```

### Predict 

`POST https://machina-labs-ml.azurewebsites.net/api/Predict` 

example body:
```json
{
    "X_test": 
    [
        {									
            "a_enc_1" : -4.9511,
            "b_enc_1" : 0.0183,
            "c_enc_1" : -0.0719, 
            "x_enc_1" : 213.6337,
            "y_enc_1" : 324.1015,	
            "z_enc_1" : 895.3528,	
            "a_enc_2" : -154.9772, 	
            "b_enc_2" : 0.2023, 	
            "c_enc_2" : -179.8798, 	
            "x_enc_2" : 22.3221, 	
            "y_enc_2" : 783.1761, 	
            "z_enc_2" : -772.5771
        },
        {									
            "a_enc_1" : -4.9511,
            "b_enc_1" : 0.0183,
            "c_enc_1" : -0.0719, 
            "x_enc_1" : 213.6337,
            "y_enc_1" : 324.1015,	
            "z_enc_1" : 895.3528,	
            "a_enc_2" : -154.9772, 	
            "b_enc_2" : 0.2023, 	
            "c_enc_2" : -179.8798, 	
            "x_enc_2" : 22.3221, 	
            "y_enc_2" : 783.1761, 	
            "z_enc_2" : -772.5771
        }
    ]
}
```

## Function App code deployment 

```
az login
func azure functionapp publish machina-labs-ml
```