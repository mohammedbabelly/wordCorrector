import time
from multiprocessing import Process, current_process, Manager, cpu_count
from textblob import TextBlob, Word


def correctMisspelledWords(block, passedData):
    processName = current_process().name  # Process-2
    processNumber = (processName[-1])  # take the last char of the name
    passedData['numProcesses'] += 1
    passedData["finalFileText"][processNumber] = ""
    for line in block:
        originLine = line.split()
        fixedLine = TextBlob(line).correct()
        splittedFixedLine = fixedLine.split()
        for i in range(len(originLine)):
            if (originLine[i] != splittedFixedLine[i]):
                passedData["misspelledWordsCount"] += 1
                passedData["correctedWords"][originLine[i]
                                             ] = splittedFixedLine[i]

        passedData["finalFileText"][processNumber] += str(fixedLine)


def main():
    processes = []
    manager = Manager()
    passedData = manager.dict()
    passedData["correctedWords"] = manager.dict()
    passedData["finalFileText"] = manager.dict()
    passedData["misspelledWordsCount"] = 0
    passedData['numProcesses'] = 0
    # start opening the file
    # fileName = input('Your file path: ')
    fileName = "files/1.txt"
    sourceFile = open(fileName, "r").readlines()  # r: read
    startTime = time.time()
    fileLines = len(sourceFile)
    blockSize = fileLines / cpu_count()
    block = []
    for i in range(fileLines):
        block.append(str(sourceFile[i]))

        if (len(block) == blockSize or i == fileLines-1):
            currentProcess = Process(target=correctMisspelledWords, args=(
                block, passedData))
            processes.append(currentProcess)
            currentProcess.start()
            block = []

    # make sure that all the processes are done
    for process in processes:
        process.join()

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


def writeCorrectedFile(t):
    # open file
    path = "files/1_afterCorrection.txt"
    finalFile = open(path, "w")
    # convert DictProxy(t) to a normal dictionary(text)
    text = {}
    for key, value in t.items():
        text[key] = value
    # write the final text from the sorted
    # dictionary<processNumber,correctedText> by its key
    for key in sorted(text):
        finalFile.write(text[key])
    finalFile.close()
    print(f'File created at {path}')


if __name__ == '__main__':
    main()
