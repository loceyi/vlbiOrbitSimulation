from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import PIL
def sat_orbit_plot():

    bm = PIL.Image.open('globe_east_540.jpg')

    bm = np.array(bm.resize([d/1 for d in bm.size]))/256.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 6371000 * np.outer(np.cos(u), np.sin(v))
    y = 6371000* np.outer(np.sin(u), np.sin(v))
    z = 6371000 * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the surface
    plt.axis('off')
    ax.plot_surface(x, y, z, rstride = 1,   # row 行步长
                     cstride = 2,cmap=plt.cm.CMRmap)



    plt.show()

def test():




    sat_orbit_plot()



if __name__ == "__main__":

    test()