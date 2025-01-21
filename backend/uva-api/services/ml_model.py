import sqlite3
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# used to train only one time then use the dumps

def train_linear_model(db_path='../files/vitibrasil_data_v2.db'):
    # 1. Connect to sql lite
    conn = sqlite3.connect(db_path)
    
    # 2. query "commercialization"
    query = "SELECT product, type, quantity_l, year FROM commercialization WHERE year >= 1970 AND year <= 2023;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # 3. Preproccessing
    # Quantity_l to float
    df['quantity_l'] = pd.to_numeric(df['quantity_l'], errors='coerce')
    
    # remove nan
    df = df.dropna(subset=['quantity_l'])

    # 4. cat to dummies
    df_dummies = pd.get_dummies(df, columns=['product', 'type'], drop_first=True)
    
    # 5. features and target
    X = df_dummies.drop(['quantity_l'], axis=1)
    y = df_dummies['quantity_l']
    
    # 6. train test split
    # random
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 7. linear regression
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 8. evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"RMSE: {rmse:.2f}")
    print(f"R2:   {r2:.4f}")
    
    # 9. model saving
    joblib.dump(model, '../files/linear_model.joblib')
    
    # saving cols
    joblib.dump(X.columns.tolist(), '../files/model_columns.joblib')

if __name__ == '__main__':
    train_linear_model()