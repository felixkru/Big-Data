import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns

from src import mongoConnection

visualization_data_x = []
visualization_data_y = []
query_result = mongoConnection.read_data_from_mongo({},
                                                    "asian_dolphins")
try:
    for dataset in query_result:
        try:
            for datapoint in dataset["magnetization_straightened_clean"]:
                visualization_data_y.append(datapoint)
        except Exception as e:
            print(f"Exception occurred: {e}")
            continue
        try:
            for datapoint in dataset["wall_thickness_clean"]:
                visualization_data_x.append(datapoint)
        except Exception as e:
            print(f"Exception occurred: {e}")
            continue
except Exception as e:
    print(f"Exception: {e}")

visualization_data_x = np.array(visualization_data_x)
visualization_data_y = np.array(visualization_data_y)

indices = np.argsort(visualization_data_x)

visualization_data_x = visualization_data_x[indices]
visualization_data_y = visualization_data_y[indices]

indices_to_delete = np.where(visualization_data_x < 0)
visualization_data_x = np.delete(visualization_data_x, indices_to_delete)
visualization_data_y = np.delete(visualization_data_y, indices_to_delete)

indices_to_delete = np.where(visualization_data_x > 35)
visualization_data_x = np.delete(visualization_data_x, indices_to_delete)
visualization_data_y = np.delete(visualization_data_y, indices_to_delete)

indices_to_delete = np.where(visualization_data_y > 20)
visualization_data_x = np.delete(visualization_data_x, indices_to_delete)
visualization_data_y = np.delete(visualization_data_y, indices_to_delete)


# counter = -1
# for datapoint in visualization_data_x:
#     if datapoint < 0:
#         visualization_data_x[counter] = datapoint * -1
#         counter += 1


# Die Funktion, die an die Daten angepasst werden soll
def modell_funktion_polynom(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d


def modell_funktion_sinus(x, a, b):
    return a * np.sin(b * x)

def quadratische_funktion(x, a, b, c):
    return a * x**2 + b * x + c


# curve_fit benutzen, um die Parameter a und b zu finden
parameter, parameter_kovarianz = curve_fit(modell_funktion_polynom, visualization_data_x, visualization_data_y)

y_vorhersage = modell_funktion_polynom(visualization_data_x, *parameter)

ss_res = np.sum((visualization_data_y - y_vorhersage)**2)
ss_tot = np.sum((visualization_data_y - np.mean(visualization_data_y))**2)
r2 = 1 - (ss_res / ss_tot)

print(f"R^2: {r2}")

print("Gefundene Parameter:", parameter)
# Die gefundene Kurve zeichnen
# plt.scatter(visualization_data_x, visualization_data_y, label='Daten')
plot = sns.jointplot(x=visualization_data_x, y=visualization_data_y, kind='hex', gridsize=30, cmap="plasma", marginal_kws=dict(bins=50))
plt.plot(visualization_data_x, modell_funktion_polynom(visualization_data_x, *parameter), label='Quadratische Funktion', color='red')
plot.set_axis_labels("Wandstärke", "Magnetisierung")
plt.legend()
plt.tight_layout()
plt.show()
