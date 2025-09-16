
import random
import time

def main():
    #создание массива, содержащего отсортированные числа от 10 до 250 млн.
    step = random.randint(3, 5)
    random_list = []
    for i in range(10, 250000000, step):
        random_list.append(i)

    # создание массива, содержащего 10 случайных чисел

    random_numbers = [random.randint(10, 250000000) for i in range(10)]
    print(f"Числа, которые будем искать: {random_numbers}")

    # проверка времени линейного поиска
    start = time.time()
    linear_search(random_list, random_numbers)
    end = time.time()
    print("Линейный поиск занял:", end - start, "секунд")

    # проверка времени бинарного поиска
    start = time.time()
    binary_search(random_list,random_numbers)
    end = time.time()
    print("Бинарный поиск занял:", end - start, "секунд")

# создание линейного поиска
def linear_search(random_list, random_numbers):
    results = {}
    for t in random_numbers:
        for i, val in enumerate(random_list):
            if val == t:
                results[t] = i
                break
            else:
                results[t] = -1
        if results[t] == -1:
            print(f"Число {t} не найдено")
        else:
            print(f"Число {t} найдено, под индексом {i}")
    return results

# создание бинарного поиска
def binary_search(random_list, random_numbers):
    results = {}
    for t in random_numbers:
        left, right = 0, len(random_list) - 1
        index = -1
        while left <= right:
            mid = (left + right) // 2
            if random_list[mid] == t:
                index = mid
                break
            elif random_list[mid] < t:
                left = mid + 1
            else:
                right = mid - 1
        results[t] = index
        if results[t] == -1:
            print(f"Число {t} не найдено")
        else:
            print(f"Число {t} найдено, под индексом {index}")
    return results

if __name__ == "__main__":
    main()