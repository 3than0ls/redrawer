from math import sqrt
from palette import RGB


def color_distance(source: RGB, compare: RGB) -> int:
    """Utilizes the low-cost approximation algorithm found here:
    https://www.compuphase.com/cmetric.htm

    This algorithm will run for every pixel in the image, for every palette color (20 or 30). 
    Since the palette color is a constant... technically the whole process is only O(n) where n is the number of pixels...
    Yeah... funny... in reality there's a HUGE amount of pixels (width x height).
    We're iterating over every row, and then over every column, and then over every column, and then, applying this algorithm to every color pixel.
    """
    mean_red = (source.red + compare.red) / 2
    red_diff = source.red - compare.red
    green_diff = source.green - compare.green
    blue_diff = source.blue - compare.blue
    return int(sqrt(
        (512 + mean_red) * red_diff * red_diff +
        4 * green_diff * green_diff +
        (767-red_diff) * blue_diff * blue_diff
    ))


def is_near_color(source: RGB, compare: RGB, max_distance=50) -> bool:
    return color_distance(source, compare) < max_distance


# maybe do ti like this using numpy arrays
# load image into numpy
# run the numpy array through color_distance, creating a new matrix representing the color distance for each one
# create a final matrix where each element is the color correlated with the lowest color distance value
# image matrix   -->   30x color distance matrices  -->  final color image matrix
# final color image amtrix element format to be decided

if __name__ == '__main__':
    # one = RGB(255, 255, 255)
    # two = RGB(0, 0, 0)
    # value = color_distance(one, two)
    # print(value)

    for i in range(0, 1):
        one = RGB(10, 7, 10)
        two = RGB(0, 0, 0)
        value = color_distance(one, two)
        print(value)
        print(f"base color {one} is similar to {two}:\t{value < 50}")
