import sys
import numpy as np
from scan import Scan
import matplotlib.pyplot as plt
from skimage import filters


def main():
    scan = Scan(5000)
    scan.load_data(sys.argv[1])
    scan.find_peaks()
    scan.mark_inner_surface()
    scan.plot_cut_matrix()
    scan.create_polar_views()
    # scan.find_circles()
    # scan.debug = True
    # scan.interpolation_polar_view(scan.polar_views[3], 3)
    b = scan.polar_views[1]
    scan.interpolation_polar_view(b, 3)
    # plt.figure(), plt.imshow(b)

    # plt.figure(), plt.hist(scan.polar_views[1])


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
