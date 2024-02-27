# %%
import matplotlib.pyplot as plt

# Open a csv using pandas
import pandas as pd
df = pd.read_csv('surgeData/Harvey_Gulf.csv', delimiter='\t', header=0, names=['time', 'surge'])
df
# %%
# Convert the time column to a datetime object.
df['time'] = pd.to_datetime(df['time'])
# Remove rows beyond the end time of the wind data = 31-08-2017 00:00
df = df[df['time'] <= '31-08-2017 00:00']
df

# %%
# Plot df
fig, ax = plt.subplots()
ax.plot(df['time'], df['surge'])
# make x-axis labels not overlap
plt.xticks(rotation=45)
# Make x-axis labels more sparse.
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
# Move the y-axis to the right side
ax.yaxis.tick_right()
ax.set_title('Surge (m)')
plt.show()
# %%
# Use matplotlib to animate a time series where the animation draws the plot across the x-axis through time.
# animate
import matplotlib.animation as animation
import numpy as np

# line plot animation
fig, ax = plt.subplots(1, 1, figsize = (6, 6))
ax.set_xlim(df['time'].iat[0], df['time'].iat[-1])
ax.set_ylim([1.1*np.min(df['surge']), 1.1*np.max(df['surge'])])
ax.yaxis.tick_right()
plt.xticks(rotation=45)
# Make x-axis labels more sparse.
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
# Set title
ax.set_title('Surge (m)')


# Turn off x-axis label
# ax.set_xticklabels([])

def animate(i):
    ax.cla() # clear the previous image
    ax.plot(df['time'].iloc[:i], df['surge'].iloc[:i]) # plot the line
    ax.set_xlim(df['time'].iat[0], df['time'].iat[-1]) # fix the x axis
    ax.set_ylim([1.1*np.min(df['surge']), 1.1*np.max(df['surge'])]) # fix the y axis
    ax.set_title(f"Surge (m) {str(df['time'].iat[i])}")

anim = animation.FuncAnimation(fig, animate, frames = len(df['time']), interval = 50, blit = False)
plt.show()

# %%
# save anim
anim.save('surge.mp4', writer='ffmpeg', fps=20)

# %%