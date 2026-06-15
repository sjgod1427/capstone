import pandas as pd
import numpy as np
from typing import List
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.drop(columns=['name', 'model', 'edition'])
    df = df.drop_duplicates()
    return df


def impute_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    list(map(
        lambda col: df.__setitem__(
            col,
            df.groupby('company')[col].transform(
                lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else df[col].mode().iloc[0])
                if df[col].dtype == 'object'
                else x.fillna(x.median() if pd.notna(x.median()) else df[col].median())
            )
        ),
        columns
    ))
    return df


def build_preprocessor() -> ColumnTransformer:
    num_cols_to_log = ['km_driven', 'torque_nm', 'max_power_bhp']
    num_cols_no_log = ['year', 'mileage_mpg', 'engine_cc', 'seats']
    cat_cols        = ['company', 'owner', 'fuel', 'seller_type', 'transmission']

    log_num_pipe = Pipeline([
        ('log',     FunctionTransformer(np.log1p)),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler',  StandardScaler())
    ])

    num_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler',  StandardScaler())
    ])

    cat_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    return ColumnTransformer(transformers=[
        ('log_num', log_num_pipe, num_cols_to_log),
        ('num',     num_pipe,     num_cols_no_log),
        ('cat',     cat_pipe,     cat_cols)
    ])
