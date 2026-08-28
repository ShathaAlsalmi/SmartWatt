import numpy as np
import pandas as pd

def prepare_daily_features(df_raw: pd.DataFrame, target_date_str: str):
    df = df_raw.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    df_daily = df.groupby('date')['load_kwh'].sum().reset_index()
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    df_daily = df_daily.sort_values('date').reset_index(drop=True)
    
    loads = df_daily['load_kwh'].values
    target_dt = pd.to_datetime(target_date_str)
    
    lag_1 = float(loads[-1])
    lag_2 = float(loads[-2])
    lag_3 = float(loads[-3])
    lag_7 = float(loads[-7])
    lag_14 = float(loads[-14])
    lag_30 = float(loads[-30])
    
    roll_3 = float(np.mean(loads[-3:]))
    roll_7 = float(np.mean(loads[-7:]))
    roll_30 = float(np.mean(loads[-30:]))
    
    rolling_std_7 = float(np.std(loads[-7:], ddof=1))
    rolling_std_30 = float(np.std(loads[-30:], ddof=1))
    
    month = target_dt.month
    dayofweek = target_dt.dayofweek
    day_of_year = target_dt.dayofyear
    isweekend = 1 if dayofweek in [5, 6] else 0
    
    season_map = {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}
    season = season_map[month]
    
    features_df = pd.DataFrame([[
        month, dayofweek, isweekend, season,
        lag_1, lag_2, lag_3, lag_7, lag_14, lag_30,
        roll_3, roll_7, roll_30, rolling_std_7, rolling_std_30,
        day_of_year
    ]], columns=[
        "month", "dayofweek", "isweekend", "season",
        "lag_1", "lag_2", "lag_3", "lag_7", "lag_14", "lag_30",
        "roll_3", "roll_7", "roll_30", "rolling_std_7", "rolling_std_30",
        "day_of_year"
    ])
    return features_df

def prepare_monthly_features(df_raw: pd.DataFrame, target_month_str: str):
    df = df_raw.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year_month'] = df['timestamp'].dt.to_period('M')
    
    df_monthly = df.groupby('year_month')['load_kwh'].sum().reset_index()
    df_monthly = df_monthly.sort_values('year_month').reset_index(drop=True)
    
    loads = df_monthly['load_kwh'].values
    target_dt = pd.to_datetime(target_month_str)
    
    month = target_dt.month
    season_map = {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}
    season = season_map[month]
    
    month_sin = float(np.sin(2 * np.pi * month / 12))
    month_cos = float(np.cos(2 * np.pi * month / 12))
    
    lag_1 = float(loads[-1])
    lag_3 = float(loads[-3])
    lag_12 = float(loads[-12])
    
    roll_3 = float(np.mean(loads[-3:]))
    roll_12 = float(np.mean(loads[-12:]))
    
    features_df = pd.DataFrame([[
        month, season, month_sin, month_cos,
        lag_1, lag_3, lag_12, roll_3, roll_12
    ]], columns=[
        "month", "season", "month_sin", "month_cos",
        "lag_1", "lag_3", "lag_12", "roll_3", "roll_12"
    ])
    return features_df