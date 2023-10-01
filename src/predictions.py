import pandas as pd
import numpy as np
from src.data_preparation import read_data, prepare_main_dataframe


def prepare_data(start: int, stop: int) -> pd.DataFrame:
    """
    Prepare the scoring data by selecting relevant columns.
    Parameters:
    - data: A pandas DataFrame containing the data to be prepared.
    Returns:
    - data: A pandas DataFrame with only the relevant columns for scoring.
    """
    # main_df, rasp_data, kilometers_df = read_data('given_data')
    # main_df = prepare_main_dataframe(main_df, rasp_data, kilometers_df)
    # X = main_df.drop(columns=['MessageReceivedDate', 'airline_grouped_hash', 'cco_hash', 'm_city_rus2']).groupby(
    #     'MessageReceivedMinutes').mean()
    # target = main_df.MessageReceivedMinutes.value_counts().sort_index().rename('target')
    #
    # for i in set(np.arange(X.index.max())) - set(X.index):
    #     X.loc[i] = X.mean()
    #     target.loc[i] = target.mean()
    #
    # X = X.sort_index()
    # y = pd.DataFrame(target.sort_index(), columns=['target'])
    #
    # rolls = [5, 15, 30, 60, 120]
    # columns_to_roll = ['ProcessingTime', 'config', 'is_dep_B', 'is_local', 'departure_equals_checkin']
    # rolled = [X]
    #
    # for roll in rolls:
    #     rolled.append(
    #         X[columns_to_roll].rolling(roll).mean().rename(columns={c: c + f'_{roll}' for c in columns_to_roll}))
    #     rolled.append(y.rolling(roll).mean().rename(columns={'target': f'target_{roll}'}))
    #
    # X = pd.concat(rolled, axis=1)
    # X /= X.max(axis=0)
    #
    # X = X.iloc[max(rolls):]
    # y = y.iloc[max(rolls):]
    #
    # X.to_csv('x_v1.csv', index=False)
    # y.to_csv('y_v1.csv', index=False)

    X = pd.read_csv('computed_data/x_v1.csv').iloc[start:stop]
    y = pd.read_csv('computed_data/y_v1.csv').iloc[start:stop]
    return X.to_numpy(), y.to_numpy()


def get_predictions(model, start: int, stop: int) -> np.ndarray:
    """Predictions generation.

    Args:
        data (pd.DataFrame): Pandas dataframe.
        model (sklearn.linear_model.LinearRegression): Model object.

    Returns:
        pd.DataFrame: Pandas dataframe with predictions column.
    """

    X, y = prepare_data(start, stop)
    predictions = model.predict(X)
    # TODO: save predictions
    return predictions, [x[0] for x in y]


def save_predictions(predictions: pd.DataFrame) -> None:
    """Save predictions to *rofl* database.
    Look: fastapi/utils/ROFLDatabase
    Args:
        predictions (pd.DataFrame): Pandas dataframe with predictions column.
    """
    pass

    # raise NotImplementedError('src/save_predictions not implemented do smth about it (or dont)')
