## Project Overview

This project aims to forecast the forces experienced by robots within a system, comprising two main components:

Jupyter notebooks for data analysis and model training to predict force.
A Python dotnet API for real-time force prediction.
The subsequent sections in this readme will detail the structure of component 2. For a comprehensive explanation of the model methodology and results, refer to the notebooks in the `Jupyter/` directory.

## API Functions

This API encompasses two functions: `create` for adding new records to our database and `predict` for making real-time predictions based on a fresh set of features. These functions have been deployed to Azure, operating on the free tier API.

The decision to develop these APIs was made to showcase that once the model is finalized, it can be instantly queried on demand. Additionally, newly created data can be posted to Azure and added to a Cosmos DB, enabling future querying for retraining our model, creating a circular pipeline.

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

## Future Work

Unfortunately, due to the limitations of the Azure free tier, I was unable to deploy my actual model to the service. The free tier has certain capacity restrictions, and I would need to upgrade to a paid plan to scale up my service. In the future, I plan to scale out my function app to accommodate this larger model.