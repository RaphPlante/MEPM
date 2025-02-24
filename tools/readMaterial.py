import pandas as pd


def readMaterial(file, sheet):
    # Read data from Excel file into DataFrame
    df = pd.read_excel(file, sheet_name=sheet, header=None, usecols="B")

    # Extract material properties from DataFrame
    rho = df.iloc[0, 0]
    w = df.iloc[1, 0]
    f = df.iloc[2, 0]
    n = df.iloc[3, 0]
    k = df.iloc[4, 0]
    eta_inf = df.iloc[5, 0]
    eta_0 = df.iloc[6, 0]
    tau_0 = df.iloc[7, 0]
    lmbda = df.iloc[8, 0]
    a = df.iloc[9, 0]

    return rho, w, f, n, k, eta_inf, eta_0, tau_0, lmbda, a


"""# Example usage:
file = "material_database.xlsx"
sheet = "material"

rho, w, f, n, k, eta_inf, eta_0, tau_0, lmbda, a = read_material(file, sheet)
print("rho:", rho)
print("w:", w)
print("f:", f)
print("n:", n)
print("k:", k)
print("eta_inf:", eta_inf)
print("eta_0:", eta_0)
print("tau_0:", tau_0)
print("lambda:", lmbda)
print("a:", a)
"""
