import numpy as np
import pandas as pd
import streamlit as st

# Function to perform linear interpolation using central difference
def linear_interpolation(x, y, angle):
    neg_side = 1
    if angle > 4*x[-1]:
        angle = angle%(4*x[-1])
    elif angle < 0:
        angle = -1 * angle
        neg_side = -1
    
    if angle >= x[0] and angle <= x[-1]:
        for i in range(len(x) - 1):
            if x[i] <= angle <= x[i + 1]:
                return neg_side * (y[i] + (angle - x[i]) * (y[i + 1] - y[i]) / (x[i + 1] - x[i]))
        
    elif angle > x[-1] and angle <= 2*x[-1]:
        angle = 2*x[-1] - angle
        for i in range(len(x) - 1):
            if x[i] <= angle <= x[i + 1]:
                return neg_side * (y[i] + (angle - x[i]) * (y[i + 1] - y[i]) / (x[i + 1] - x[i]))

    elif angle > 2*x[-1] and angle <= 3*x[-1]:
        angle = angle - 2*x[-1]
        for i in range(len(x) - 1):
            if x[i] <= angle <= x[i + 1]:
                return -1 * neg_side * (y[i] + (angle - x[i]) * (y[i + 1] - y[i]) / (x[i + 1] - x[i]))

    elif angle > 3*x[-1] and angle <= 4*x[-1]:
        angle = 4*x[-1] - angle
        for i in range(len(x) - 1):
            if x[i] <= angle <= x[i + 1]:
                return -1 * neg_side * (y[i] + (angle - x[i]) * (y[i + 1] - y[i]) / (x[i + 1] - x[i]))
    else:
        return None  # Unexpected value
    

# Function to find sine value and perform interpolation if necessary
def get_sine_value(angle, theta_equally_spaced, sine_equally_spaced, theta_skewed, sine_skewed):
    sine_eq = linear_interpolation(theta_equally_spaced, sine_equally_spaced, angle)
    sine_skew = linear_interpolation(theta_skewed, sine_skewed, angle)
    actual_value = np.sin(angle)

    error_eq = actual_value - sine_eq if sine_eq is not None else None
    relative_error_eq = error_eq / actual_value if error_eq is not None and actual_value != 0 else None

    error_skew = actual_value - sine_skew if sine_skew is not None else None
    relative_error_skew = error_skew / actual_value if error_skew is not None and actual_value != 0 else None

    return {
        'Angle': angle,
        'Sine (Equally Spaced)': sine_eq,
        'Error (Equally Spaced)': error_eq,
        'Relative Error (Equally Spaced)': relative_error_eq,
        'Sine (Skewed)': sine_skew,
        'Error (Skewed)': error_skew,
        'Relative Error (Skewed)': relative_error_skew,
        'Actual Sine': actual_value
    }

# Streamlit App
st.title("Sine Approximation with Lookup Tables")

# User input for number of values
num_values = st.number_input("Number of Values", min_value=5, max_value=100, value=20)

# Generate equally distributed theta values from 0 to pi/2
theta_equally_spaced = np.linspace(0, np.pi/2, num_values)
sine_equally_spaced = np.sin(theta_equally_spaced)

# Generate skewed distribution towards pi/2
theta_skewed = np.linspace(0, 1, num_values)**(1/2) * (np.pi / 2)  # Skewed towards pi/2
sine_skewed = np.sin(theta_skewed)

# Button to display the lookup table
if st.button("Show Lookup Table"):
    lookup_table = pd.DataFrame({
        'Theta (Equally Spaced)': theta_equally_spaced,
        'sin(Theta) Equally Spaced': sine_equally_spaced,
        'Theta (Skewed)': theta_skewed,
        'sin(Theta) Skewed': sine_skewed
    })
    st.write(lookup_table)

# User input for test angles
test_angles_input = st.text_area("Enter angles in degrees (comma-separated)", "0, 30, 45, 60, 90, 95")
test_angles = [float(angle.strip())*np.pi/180 for angle in test_angles_input.split(",")]
print(test_angles)

# Calculate results for the entered test angles
results = []
for angle in test_angles:
    result = get_sine_value(angle, theta_equally_spaced, sine_equally_spaced, theta_skewed, sine_skewed)
    results.append(result)

# Create a DataFrame for results
results_df = pd.DataFrame(results)

# Display results in a neat table
st.subheader("Results")
st.write(results_df)
