import matplotlib.pyplot as plt

# First dataset
x_values = [1, 2, 3, 4, 5]
y_values = [1, 2, 3, 4, 5]

# Plot the first dataset as a line graph
plt.plot(x_values, y_values, label='Line 1', marker='o')

# Plot the same data as a scatter plot
plt.scatter(x_values, y_values, color='red', label='Scatter 1')

# Second dataset
x_values2 = [1, 2, 3, 4, 5]
y_values2 = [5, 3, 4, 2, 1]

# Plot the second dataset as a line graph
plt.plot(x_values2, y_values2, label='Line 2', linestyle='--', marker='s')

# Add title and axis labels
plt.title('My first plot')
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.legend()
plt.grid(True)
plt.show()
