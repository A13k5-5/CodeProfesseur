import sys


def get_sum(a):
    return a


if __name__ == "__main__":
    if len(sys.argv) > 1:
        value = int(sys.argv[1])
        print(get_sum(value))
    else:
        print(get_sum(5))
