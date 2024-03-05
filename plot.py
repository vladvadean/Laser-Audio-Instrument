import matplotlib.pyplot as plt
import pandas as pd

# Function to read values from file and generate time data
def read_data(file_name, time_interval):
    with open(file_name, 'r') as file:
        values = [int(line.strip()) for line in file]
        # Generate time data with a constant interval
        time = [i * time_interval for i in range(len(values))]
    return time, values

# Specify the time interval between data points in miliseconds
time_interval = 2.6

# Read data and generate time axis
time, values = read_data('received_values.txt', time_interval)

# Create DataFrame from the data
data = pd.DataFrame({'time': time, 'values': values})

# Store all data points
all_data_points = list(zip(time, values))

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data['time'], data['values'], marker='x')
plt.title('Time vs Values')
plt.xlabel('Time (milliseconds)')
plt.ylabel('Values')
plt.grid(True)
plt.show()

# Optionally, you can write the data points to a file
with open('data_points.txt', 'r+') as file:
            file.truncate(0) 
with open('data_points.txt', 'w') as file:
    for x, y in all_data_points:
        file.write(f'{x}, {y}\n')

print("Data points saved to data_points.txt")


