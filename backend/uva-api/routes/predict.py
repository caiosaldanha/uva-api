from fastapi import APIRouter, HTTPException
import sqlite3
import pandas as pd

router = APIRouter()

model = joblib.load("./files/linear_model.joblib")
model_columns = joblib.load("./files/model_columns.joblib")

@router.get("/predict/commercialization")
def predict_2024():

    db_path = "./files/vitibrasil_data_v2.db"
    conn = sqlite3.connect(db_path)
    query = """
        SELECT DISTINCT product, type
        FROM commercialization
        WHERE year >= 1970 AND year <= 2023
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['year'] = 2024
    
    df_dummies = pd.get_dummies(df, columns=['product', 'type'])
    
    df_model = pd.DataFrame(columns=model_columns)
    
    for col in df_dummies.columns:
        if col in df_model.columns:
            df_model[col] = df_dummies[col]
    
    df_model = df_model.fillna(0)

    preds = model.predict(df_model)

    df_result = df.copy()
    df_result['predicted_quantity_l'] = preds

    result = df_result.to_dict(orient="records")
    return {"data": result}