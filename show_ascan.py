import sys
from scan import Scan
import matplotlib.pyplot as plt

def main():
    scan = Scan()
    width = 10000
    scan.load_data(sys.argv[1])
    scan.find_peaks(width)
    scan.create_polar_views()
    # scan.find_circles(width)
    scan.interpolation_polar_view(scan.polar_views[1], 3)


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
