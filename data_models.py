from pydantic import BaseModel
import typing

class DBData(BaseModel):
    id : str
    a_enc_1 : float
    b_enc_1 : float 
    c_enc_1 : float 
    x_enc_1 : float
    y_enc_1 : float	
    z_enc_1 : float 	
    a_enc_2 : float 	
    b_enc_2 : float 	
    c_enc_2 : float 	
    x_enc_2 : float 	
    y_enc_2 : float 	
    z_enc_2 : float 
    fx_1 : float 
    fy_1 : float	
    fz_1 : float 	
    fx_2 : float 	
    fy_2 : float 	
    fz_2 : float 

class TestDataX(BaseModel):
    a_enc_1 : float
    b_enc_1 : float 
    c_enc_1 : float 
    x_enc_1 : float
    y_enc_1 : float	
    z_enc_1 : float 	
    a_enc_2 : float 	
    b_enc_2 : float 	
    c_enc_2 : float 	
    x_enc_2 : float 	
    y_enc_2 : float 	
    z_enc_2 : float 	

class TestDataY(BaseModel):
    fx_1 : float 
    fy_1 : float	
    fz_1 : float 	
    fx_2 : float 	
    fy_2 : float 	
    fz_2 : float 
