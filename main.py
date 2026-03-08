import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots(figsize = (16, 9))
    fig.set_facecolor('lightgrey')
    fig.suptitle("this is a whole name")
    ax.set_title("this is a plot name")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.show()

if __name__ == "__main__":
    main()