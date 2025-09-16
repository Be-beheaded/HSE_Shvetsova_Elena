import random


def main():
    # создание массива из целых чисел
    random_list = []
    for i in range(100000):
        random_list.append(random.randint(1, 1000000))

    #bubble_sort(random_list) Очень долго выполняется

    # создание массива из словарей
    random_dict_list = []
    for i in range(100000):
        random_dict_list.append({"num_1": random.randint(1, 1000000), "num_2": random.randint(1, 1000000)})

    # сортировка .sort() и лямбда-функции
    random_dict_list.sort(key=lambda n: n["num_1"])
    random_dict_list.sort(key=lambda n: n["num_2"])

# создание алгоритма сортировки пузырьком
def bubble_sort(random_list):
    length = len(random_list) - 1
    for i in range(length):
        for j in range(length - i):
            if random_list[j] > random_list[j + 1]:
                random_list[j], random_list[j + 1] = random_list[j + 1], random_list[j]


if __name__ == "__main__":
    main()
