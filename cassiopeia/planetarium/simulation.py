import matplotlib.pyplot as plt

from calculation import Calculation

c = Calculation()
coord_list = c.cal_uni_new_pos((365 * 24))

x_sun, y_sun = c.planets[0]["Pos"]
plt.scatter(x_sun, y_sun, s=500, facecolor='yellow', alpha=0.5)
plt.plot([coord[0] for coord in coord_list], [coord[1] for coord in coord_list])
plt.show()
