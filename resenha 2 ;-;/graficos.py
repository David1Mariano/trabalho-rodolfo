import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "mission.db"


def load_data():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        """
        SELECT *
        FROM telemetry
        ORDER BY id
        """,
        conn
    )

    conn.close()

    return df


def generate_graphs():

    df = load_data()

    # ==========================
    # TEMPERATURA
    # ==========================

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["id"],
        df["temperature"],
        marker="o"
    )

    plt.title(
        "Temperature Monitoring"
    )

    plt.xlabel(
        "Reading Number"
    )

    plt.ylabel(
        "Temperature (°C)"
    )

    plt.grid(True)

    plt.savefig(
        "temperature_graph.png"
    )

    plt.close()

    # ==========================
    # ENERGIA
    # ==========================

    plt.figure(figsize=(10, 5))

    plt.bar(
        df["id"],
        df["energy"]
    )

    plt.title(
        "Energy Monitoring"
    )

    plt.xlabel(
        "Reading Number"
    )

    plt.ylabel(
        "Energy (%)"
    )

    plt.savefig(
        "energy_graph.png"
    )

    plt.close()

    print("Graphs generated successfully.")