import numpy as np
from math import pi, atan

# 2 arrays (ndvi and day of the year)
ndvi = np.array([200, 300, 450, 700, 700, 600, 450, 200, 200])
doy = np.array([1, 45, 90, 135, 170, 215, 250, 295, 340])

# Convert doy to decimal day
decimal_doy = doy / 365

# Compute harmonic regressors
harmon_regressor = np.array([np.sin(2 * pi * decimal_doy),
                            np.cos(2 * pi * decimal_doy),
                            np.ones((9))])
print(harmon_regressor)

# Fit model
fit = np.linalg.lstsq(harmon_regressor.T, ndvi)
sin_coeff, cos_coeff, intercept = fit[0]
print(intercept, sin_coeff, cos_coeff)

# Timing of local extremum
t = atan(sin_coeff / cos_coeff)
# Amplitude (twice absolute value of local extremums)
amplitude = abs(2*(cos_coeff*np.cos(t) +
                   sin_coeff*np.sin(t)))
print(amplitude)
