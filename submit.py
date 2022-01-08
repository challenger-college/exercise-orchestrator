from sys import argv

def sum_two_number(a, b):
    return a + b

if __name__ == "__main__":
    print(sum_two_number(int(argv[1]), int(argv[2])))