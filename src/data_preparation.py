import pandas as pd
from typing import List
from sklearn.feature_extraction import FeatureHasher


def read_data(work_dir: str) -> List[pd.DataFrame]:
    """
    Read the data from the specified working directory.
    Parameters:
        work_dir (str): The path to the working directory.
    Returns:
        List[pd.DataFrame]: A list containing the
        main dataframe,
        the rasp data dataframe
        kilometers dataframe.
    """
    main_df = pd.read_csv(f'../{work_dir}/bsm_data_train.csv')
    rasp_data = pd.read_csv(f'../{work_dir}/flight_rasp_data.csv')
    kilometers_df = pd.read_csv(f'../{work_dir}/kilometers.csv')
    return [main_df, rasp_data, kilometers_df]


def prepare_main_dataframe(main_df: pd.DataFrame,
                           rasp_data: pd.DataFrame,
                           kilometers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the main dataframe.
    Parameters:
        main_df (pd.DataFrame): The main dataframe.
        rasp_data (pd.DataFrame): The rasp data dataframe.
        kilometers_df (pd.DataFrame): The kilometers dataframe.
    Returns:
        pd.DataFrame: The prepared main dataframe.
    """
    main_df = main_df.drop_duplicates('ident_bag', keep='first').reset_index(drop=True)
    main_df = main_df.join(rasp_data.set_index('i_id'), on='i_id')
    main_df = main_df.drop(columns=['pax_id_hash', 'm_city_rus1', 'DateEvent'])

    main_df['MessageReceivedMinutes'] = pd.to_datetime(main_df['MessageReceivedDate']).apply(
        lambda x: x.value) / 1000000000 // 60
    main_df['MessageReceivedMinutes'] = main_df['MessageReceivedMinutes'].astype(int)
    main_df['MessageReceivedMinutes'] -= main_df['MessageReceivedMinutes'].min()
    main_df = main_df.sort_values(by='MessageReceivedMinutes')

    main_df['ProcessingTime'] = (
                pd.to_datetime(main_df.MessageProcessedDate) - pd.to_datetime(main_df.MessageReceivedDate)).apply(
        lambda x: x.seconds)

    main_df = main_df.drop(columns=['ident_bag', 'i_id', 'MessageProcessedDate', 'TagNumber'], errors='ignore')
    main_df['is_dep_B'] = main_df.departure_terminal == 'B'
    main_df['is_local'] = main_df.local_or_transfer == 'L'
    main_df['departure_equals_checkin'] = (main_df['departure_terminal'] == main_df['checkin_terminal']).astype('int')
    main_df = main_df.drop(columns=['local_or_transfer', 'departure_terminal', 'checkin_terminal', 'flt_hash'])

    main_df['ProcessingTime'] /= main_df.ProcessingTime.max()

    main_df['dep_day'] = pd.to_datetime(main_df['t_st']).apply(lambda x: x.dayofweek) / 6
    main_df['dep_hour'] = pd.to_datetime(main_df['t_st']).apply(lambda x: x.hour) / 23

    main_df = main_df.drop(columns='t_st')

    # тут может быть долго
    rasp_data['t_st'] = pd.to_datetime(rasp_data.t_st).apply(lambda x: x.timestamp())
    rasp_data['t_st'] -= rasp_data.t_st.min()
    rasp_data['t_st'] //= 60

    nflights_next_3_hours = list()

    for e in main_df.MessageReceivedMinutes.unique():
        nflights_next_3_hours.append((e, (rasp_data.t_st - e).between(0, 180).sum()))

    main_df = main_df.merge(
        pd.DataFrame.from_records(nflights_next_3_hours, columns=['MessageReceivedMinutes', 'nflights_next_3_hours']),
        on='MessageReceivedMinutes')
    main_df['nflights_next_3_hours'] /= main_df.nflights_next_3_hours.max()

    hasher = FeatureHasher(n_features=10)

    hashed = hasher.transform(main_df[['airline_grouped_hash', 'cco_hash']].to_dict(orient='records')).toarray()
    main_df = pd.concat([main_df, pd.DataFrame(hashed)], axis=1)

    kilometers_df = kilometers_df.drop(columns=['Unnamed: 0']).rename(columns={'0': 'm_city_rus2'}).set_index(
        'm_city_rus2').dropna()
    main_df = main_df.join(kilometers_df, on='m_city_rus2')
    main_df.loc[main_df.km.isna(), 'km'] = main_df.km.mean()
    main_df['km'] /= main_df.km.max()

    main_df['config'] /= main_df.config.max()
    return main_df
