import sys
from scan import Scan
import matplotlib.pyplot as plt

def main():
    scan = Scan()
    scan.load_data(sys.argv[1])
    scan.find_peaks(10000)
    scan.create_polar_views()


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
