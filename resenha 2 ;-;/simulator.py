import random

temperature = 25.0
energy = 80.0
communication = 90.0


def generate_telemetry():
    global temperature, energy, communication

    temperature += random.uniform(-2.0, 2.0)
    energy += random.uniform(-1.0, 1.0)
    communication += random.uniform(-2.0, 2.0)

    temperature = max(18, min(40, temperature))
    energy = max(30, min(100, energy))
    communication = max(50, min(100, communication))

    if temperature > 35:
        status = "CRITICAL"
    elif temperature > 30:
        status = "WARNING"
    else:
        status = "NOMINAL"

    return {
        "temperature": round(temperature, 2),
        "energy": round(energy, 1),
        "communication": round(communication, 1),
        "status": status
    }