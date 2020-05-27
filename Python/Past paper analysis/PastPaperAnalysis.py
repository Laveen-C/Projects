import PyPDF2
import csv

#Note: Changing this will make it reusable for other paper formats
def parseText(directory): #Function to convert the pdf into a 2D list of questions
    # Note:
    # - Function will remove any extra characters that do not add value to the analysis e.g. punctuation, numbers etc.
    # - Usage of 'directory' parameter as the function may be used to parse a pdf not in the same W.D. as this python file.
    pdfFileObj = open(directory, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) #Calling the class constructor to create a pdfreader object to use it's methods
    questionList = []
    questionString = ""
    for pageNum in range(1, pdfReader.numPages - 1):
        pageObj = pdfReader.getPage(pageNum)
        pageText = pageObj.extractText()
        tempText = pageText.split("\n") #Each
        try:
            tempText[1] #Failure of this means that the page is blank
        except:
            continue #We aren't interested in analysing blank pages so skip all the below code
        else:
            if tempText[1].isnumeric(): #Checking to see if we have reached a new question due to the structure of the paper
                questionList.append(stripText(questionString)) #Appending the string containing all the words in that question into the list.
                #Note: stripText will take questionString and remove all unnecessary characters, as I felt it was better to implement this as a separate function
                questionString = ""
            questionString += pageText #We are free to add the page's text since we know it is a continuation of the previous question
            if pageNum == pdfReader.numPages - 2:
                questionList.append(stripText(questionString))
    return(questionList)

def stripText(text): #Function to return the question in the form of a list.
    #Felt this was too much to squeeze into a function, and have therefore implemented it separately.
    result = ""
    text = text.replace("\n", " ")
    for index in range(len(text)):
        if text[index].isalpha() or text[index] == " ":
            result += text[index].upper()
    result = result.split()
    return result

def generateKeywordList(): #Read keywords from text file and return a list of keywords
    fileName = "cie_as_compsci.txt"
    f = open(fileName)
    isFirstWord = False #Using this isFirstWord to identify where the topic name is
    fileContents=f.readlines()
    keywordList = [] #Temporary list to hold all the keywords for a topic. This list is emptied when we reach a new topic.
    allKeywords = [] #List to hold all the keywords from the keyword text file (file name is given above)
    topicNames = [] #List to hold the names of all the topics that MAY APPEAR in the paper.
    for line in fileContents:
        if line == "\n":
            allKeywords.append(keywordList)
            keywordList = []
            isFirstWord = False
        else:
            line = line.replace("\n","")
            if isFirstWord == False: #Checking to see if we are looking at the first word
                isFirstWord = True
                topicNames.append(line.upper())
            keywordList.append(line.upper())
    allKeywords.remove([])
    f.close()
    #print(allKeywords)
    return allKeywords, topicNames #Returning a tuple to also obtain the topicNames

def analyse():
    for topicIndex in range (len(allKeywords)): # Loop for each topic
        for keywordIndex in range (len(allKeywords[topicIndex])): # Loop for each keyword in topic
            keywordLength = len(allKeywords[topicIndex][keywordIndex].split()) # find size of keyword
            for questionIndex in range (len(questionList)): # Loop for a list containing a whole question
                #print(questionList[questionIndex])
                for j in range (len(questionList[questionIndex])-keywordLength):
                    compareText = questionList[questionIndex][j] #first word
                    for k in range (1,keywordLength):
                        compareText = compareText + " " + questionList[questionIndex][j+k] # add words together to same size as keywordLength
                    if compareText.upper() == allKeywords[topicIndex][keywordIndex]: # if compareText in allKeywords
                        if allKeywords[topicIndex][0] not in outputList[questionIndex]: #if topic is not in outputList
                            outputList[questionIndex].append(allKeywords[topicIndex][0]) #then append it

def writeToCSV(paperName):
    valueList = [] #Holds the values to be placed into keyIndexDict
    tempList = [] #Temporary list implemented to transpose the rows and columns to make format more readable.
    for i in range(0, len(topicNames)):
        valueList.append(i)
    keyIndexDict = {paperName : 0}
    for key, value in zip(topicNames, valueList): #Zip allows for iterating through two tuples simultaneously.
        keyIndexDict[key] = value
    with open("analysis.csv", "w") as file:
        writer = csv.writer(file, dialect = 'excel', lineterminator = "\n")
        line = [paperName]

        for item in topicNames:
            line.append(item)
        newColumnSize = len(line)
        tempList.append(line) #We append to the list as we shall process the list to transpose it later
        questionNo = "1"
        for question in outputList:
            line = [] #Reinitialising back to empty line for the iteration below
            questionName = "Q" + questionNo
            line.append(questionName) # Line has question number at index 0
            indexesToSet = []
            #print(line) <= run this to check
            for item in question:
                indexesToSet.append(keyIndexDict[item])
            #print(indexesToSet)
            for i in range(len(topicNames)): #Iterate depending on how many topics there are
                if i in indexesToSet:
                    line.append("Y")
                else:
                    line.append("")
            #print(line)
            tempList.append(line)
            questionNo = str(int(questionNo) + 1)
        for column in range(newColumnSize): #Transposition begins here
            lineToWrite = []
            for index in range(len(tempList)):
                lineToWrite.append(tempList[index][column])
            writer.writerow(lineToWrite)

if __name__ == "__main__":
    paperName = "CoverPapers_2017_May_1_1_QP.pdf"
    allKeywords, topicNames = generateKeywordList()
    #print(topicNames) #just used this to see if the tuple returned works.
    #print(allKeywords)
    questionList = parseText(paperName)
    #print(questionList)
    outputList = [[] for i in range (len(questionList))]
    analyse()
    outputList.remove([])
    writeToCSV(paperName)
    print("TOPICS IDENTIFIED: \n")
    counter = "1"
    for item in outputList: #Changed output format so my eyes don't hurt!
        questionNum = "Q" + counter
        print(f"{questionNum}:")
        for topic in item:
            print(topic)
        print("\n")
        counter = str(int(counter) + 1)
    print("\nTOPICS HAVE BEEN WRITTEN TO 'analysis.csv'")
