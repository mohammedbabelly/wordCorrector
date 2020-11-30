import os
from multiprocessing import Process, current_process, cpu_count


def square(number):
    result = number * number
    print(f'process name: {current_process().name}')
    print(f'{number} --> {result}')


if __name__ == '__main__':
    print(f'My CPU has {cpu_count()} cores')
    processes = []
    numbers = [1, 2, 3, 4]

    for number in numbers:
        currentProcess = Process(target=square, args=(number,))
        processes.append(currentProcess)

        currentProcess.start()
    for process in processes:
        process.join()
    print('Multiprocessing completed')
