user = "a"
age = 19
gender = "male"
if user == 'admin' or age > 18 and gender == 'male':
    print("You are an admin")
else:
    print("You are not an admin")


user = "admin"
age = 18
gender = "male"
if user == 'admin' or age > 18 and gender == 'male':
    print("You are an admin")
else:
    print("You are not an admin")


user = "a"
age = 18
gender = "male"
if user == 'admin' or age > 18 and gender == 'male':
    print("You are an admin")
else:
    print("You are not an admin")


user = "a"
age = 19
gender = "female"
if user == 'admin' or age > 18 and gender == 'male':
    print("You are an admin")
else:
    print("You are not an admin")

import numpy as np
print(list(np.linspace(0.6, 2.0, 30)))


step_deg = 36
start_angle = 0
circle_deg = 360
num_steps = int(circle_deg / step_deg)
angles_deg = np.linspace(start_angle+0.1, start_angle+circle_deg, num_steps, endpoint=True)  # 不包含360°
angles_rad = np.deg2rad(angles_deg)
print("len(angles_deg)",len(angles_deg))
print("angles_deg",angles_deg)
print("angles_rad",angles_rad)