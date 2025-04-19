import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig=plt.figure()
data, = plt.plot(x, y)
plt.ylim(-15,15)
plt.plot(x, 5*np.cos(x)) # Just to bear witness that other curves in the graph are kept

def animate(i):
    data.set_data(x, y * (i + 1))
    return [data] # Return what has been modified

theAnim = animation.FuncAnimation(fig, animate, frames=10, interval=500, blit=True, repeat=False) # Note the needed `theAnim` variable. Without it, the garbarge collector would destroy the animation before it is over
plt.show()

## https://stackoverflow.com/questions/78805800/how-can-i-use-plt-ion