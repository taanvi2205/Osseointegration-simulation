import pandas as pd

# Example data
data = {
    "B (mT)": [100, 110, 120, 130],
    "sunran": [0.01, 0.02, 0.04, 0.03],
    "biomed": [0.02, 0.03, 0.05, 0.04],
    "adin":   [0.01, 0.01, 0.01, 0.01],
    "osstem": [0.01, 0.01, 0.01, 0.01]
}

df = pd.DataFrame(data)
df.to_csv("epr_data.csv", index=False)
