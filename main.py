
from utils import get_top100_list

if __name__ == '__main__':
    result = get_top100_list(False)
    for item in result:
        print(item)