import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import root_mean_squared_error

from training_utils import load_data, impute_columns, build_preprocessor


DATA_PATH  = '../notebooks/car-details.csv'
MODEL_PATH = '../app/models/car_price_model.pkl'


def train():
    # load & clean
    df = load_data(DATA_PATH)

    # impute
    df = impute_columns(df, ['mileage_mpg', 'engine_cc', 'max_power_bhp', 'torque_nm', 'seats'])

    # split
    X = df.drop(columns='selling_price')
    y = np.log1p(df['selling_price'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # pipeline
    preprocessor = build_preprocessor()

    rf_pipeline = Pipeline(steps=[
        ('pre', preprocessor),
        ('reg', RandomForestRegressor(random_state=42))
    ])

    # hyperparameter tuning
    param_grid = {
        'reg__n_estimators':     [200, 300, 500],
        'reg__max_depth':        [8, 10, 15, 20],
        'reg__min_samples_split':[5, 10, 15],
        'reg__min_samples_leaf': [2, 4, 6]
    }

    search = RandomizedSearchCV(
        rf_pipeline, param_grid, n_iter=20, cv=5,
        scoring='neg_root_mean_squared_error', n_jobs=-1, random_state=42
    )
    search.fit(X_train, y_train)

    # evaluate
    y_train_pred = np.expm1(search.predict(X_train))
    y_test_pred  = np.expm1(search.predict(X_test))

    print(f'Best params : {search.best_params_}')
    print(f'Train RMSE  : {root_mean_squared_error(np.expm1(y_train), y_train_pred):,.3f}')
    print(f'Test RMSE   : {root_mean_squared_error(np.expm1(y_test),  y_test_pred):,.3f}')

    # save
    joblib.dump(search.best_estimator_, MODEL_PATH)
    print(f'Model saved to {MODEL_PATH}')


if __name__ == '__main__':
    train()
