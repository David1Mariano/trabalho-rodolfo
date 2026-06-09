import sqlite3
import pandas as pd
import numpy as np

DB_NAME = "mission.db"


def load_data():

    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT
        temperature,
        energy,
        communication
    FROM telemetry
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


def calculate_statistics(series):

    mean = series.mean()

    median = series.median()

    mode = series.mode()

    minimum = series.min()

    maximum = series.max()

    amplitude = maximum - minimum

    variance = series.var()

    std_dev = series.std()

    cv = (std_dev / mean) * 100

    q1 = series.quantile(0.25)

    q2 = series.quantile(0.50)

    q3 = series.quantile(0.75)

    return {
        "mean": float(round(mean, 2)),
        "median": float(round(median, 2)),
        "mode": float(round(mode.iloc[0], 2)),
        "minimum": float(round(minimum, 2)),
        "maximum": float(round(maximum, 2)),
        "amplitude": float(round(amplitude, 2)),
        "variance": float(round(variance, 2)),
        "std_dev": float(round(std_dev, 2)),
        "cv": float(round(cv, 2)),
        "q1": float(round(q1, 2)),
        "q2": float(round(q2, 2)),
        "q3": float(round(q3, 2)),
    }


def mission_statistics():

    df = load_data()

    return {
        "temperature":
            calculate_statistics(
                df["temperature"]
            ),

        "energy":
            calculate_statistics(
                df["energy"]
            ),

        "communication":
            calculate_statistics(
                df["communication"]
            )
    }