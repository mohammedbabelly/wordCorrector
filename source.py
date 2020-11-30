import time
from multiprocessing import Process, current_process, Manager
from textblob import TextBlob, Word


def correctMisspelledWords(line, passedData):
    processName = current_process().name
    passedData['numProcesses'] += 1
    originLine = line.split()
    fixedLine = TextBlob(line).correct()
    splittedFixedLine = fixedLine.split()
    for i in range(len(originLine)):
        if (originLine[i] != splittedFixedLine[i]):
            passedData["misspelledWordsCount"] += 1
            passedData["correctedWords"][originLine[i]] = splittedFixedLine[i]

    passedData["finalFileText"] += (str(fixedLine))


def main():
    processes = []
    manager = Manager()
    passedData = manager.dict()
    passedData["correctedWords"] = manager.dict()
    passedData["misspelledWordsCount"] = 0
    passedData['numProcesses'] = 0
    passedData["finalFileText"] = ""

    # start opening the file
    # fileName = input('Your file path: ')
    fileName = "files/1.txt"
    sourceFile = open(fileName, "r")  # r: read
    startTime = time.time()
    for line in sourceFile:
        currentProcess = Process(target=correctMisspelledWords, args=(
            line, passedData))
        processes.append(currentProcess)
        currentProcess.start()

    # make sure that all the processes are done
    for process in processes:
        process.join()

    sourceFile.close()  # closing the sourceFile
    writeCorrectedFile(passedData["finalFileText"])
    printResult(passedData)
    print('==================Excution time==================')
    print(f'{time.time() - startTime} sec')


def printResult(data):
    print('==================num of misspelledWords==================')
    print(f'{data["misspelledWordsCount"]} words')

    print('==================num of processes==================')
    print(f'{data["numProcesses"]} process')

    print('==================Words before & after==================')
    words = data["correctedWords"]
    for w1, w2 in words.items():
        print(f'{w1} --> {w2}')


def writeCorrectedFile(text):
    path = "files/1_afterCorrection.txt"
    finalFile = open(path, "w")
    finalFile.write(text)
    finalFile.close()
    print(f'File created at {path}')


if __name__ == '__main__':
    main()
