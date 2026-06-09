from statistics import mission_statistics

stats = mission_statistics()

print("\nTEMPERATURE\n")
print(stats["temperature"])

print("\nENERGY\n")
print(stats["energy"])

print("\nCOMMUNICATION\n")
print(stats["communication"])