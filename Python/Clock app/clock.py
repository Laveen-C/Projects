import tkinter as tk
import datetime
import time
import math

class clock: #Class for each clock

    def __init__(self, location, dst, timeDiff, diameter, ID): #Constructor
        timeDiff = timeDiff.split(",")
        if time.daylight == 1: #Doing this as world may not currently be in DST period
            self.dst = int(dst) #Holds current DST value for that location if they observe DST
        else:
            self.dst = 0 #DST not needed if the world is not currently in the DST period
        self.location = location
        self.timeDiff = []
        self.timeDiff.append(str(int(timeDiff[0]) + self.dst))
        self.timeDiff.append(timeDiff[1]) #Gives us the new timezone for that location after DST
        self.currentTime = []
        self.dialSize = diameter
        self.spacing = 20 #Spacing on either side of the clock
        self.clockID = ID
        if self.clockID // 4 == 0:
            self.clockRow = 0
        else:
            self.clockRow = self.clockID//4 + 2
        self.clockColumn = self.clockID % 4

    def getTime(self): #Time will be stored as a list with 4 elements
        # time = [hours, minutes, seconds, milliseconds]
        currentTime = datetime.datetime.now(datetime.timezone.utc) #Gets time in UTC
        seconds = currentTime.strftime("%S:%f")[0:5] #Removing extra numbers from milliseconds
        minutes = int(currentTime.strftime("%M")) + int(self.timeDiff[1]) #Adding on time difference
        if minutes % 60 != minutes:
            additionalHour = 1
            minutes = minutes % 60
        else:
            additionalHour = 0
        if len(str(minutes)) == 1: #Formatting minutes back to 00 from 0 if needed
            minutes = "0" + str(minutes)
        hours = (int(currentTime.strftime("%H")) + int(self.timeDiff[0]) + additionalHour) % 24 #Adding on time difference
        if len(str(hours)) == 1: #Same formatting applied to hours
            hours = "0" + str(hours)
        #No need to format seconds as those are kept as a string the entire time
        currentTime = currentTime.strftime(f"{hours}:{minutes}:{seconds}")
        #time = currentTime.split(":")
        return currentTime #Returns time as a list for easier access when needed

    def generateDial(self):
        time = self.getTime() #Gives us the time for that location currently
        global canvas #Was making this global so I could use the canvas in refreshClock()
        canvas = tk.Canvas(window, width = dialSize + 2*self.spacing, height = dialSize + 2*self.spacing)
        # .grid() is done on a separate line because a().b() will return whatever .b() returns. In this case, .grid() returns none and so we can't use .create_oval() on it
        canvas.grid(row = self.clockRow, column = self.clockColumn)
        create_circle(canvas, self.spacing + dialSize / 2, self.spacing + dialSize / 2, dialSize / 2, fill = "black") #Creates the circle

        shift = self.dialSize/2 + self.spacing #For centre of circle, as all hands will be drawn from the centre

        #Creating the time-indicators
        #No need to optimise this step as it's only done at the beginning, so safe to take sin() and cos() here
        for lineNo in range(0, 60):
            if lineNo % 5 == 0:
                r = 25
            else:
                r = 12
            startCoord = [(dialSize/2 - r)*math.cos(math.radians(6*lineNo)) + shift, (dialSize/2 - r)*math.sin(math.radians(6*lineNo)) + shift]
            endCoord = [(dialSize/2*math.cos(math.radians(6*lineNo))) + shift, (dialSize/2*math.sin(math.radians(6*lineNo))) + shift]
            canvas.create_line(startCoord[0], startCoord[1], endCoord[0], endCoord[1], fill = "white")

        #Creating time needles
        time = self.getTime()
        tk.Label(window, text = time[:-3]).grid(row = self.clockRow + 2, column = self.clockColumn)
        startCoord = [shift, shift] #Will be the same for all needles
        #Hour needle
        endCoord = [90 * hourDict[time[0:5]][0] + shift, 90 * hourDict[time[0:5]][1] + shift]
        canvas.create_line(startCoord[0], startCoord[1], endCoord[0], endCoord[1], fill = "white", tags = "hour")
        #Minute needle
        endCoord = [130 * minuteDict[time[3:8]][0] + shift, 130 * minuteDict[time[3:8]][1] + shift]
        canvas.create_line(startCoord[0], startCoord[1], endCoord[0], endCoord[1], fill = "white", tags = "minute")
        #Second needle
        endCoord = [130 * secondDict[time[6:]][0] + shift, 130 * secondDict[time[6:]][1] + shift]
        canvas.create_line(startCoord[0], startCoord[1], endCoord[0], endCoord[1], fill = "red", tags = "second")
        #Creating centre dot on clock
        create_circle(canvas, self.spacing + dialSize / 2, self.spacing + dialSize / 2, 3, fill = "white")


def refreshClock():
    for location in clockDict:
        clockDict[location].generateDial()
    window.after(100, refreshClock)


def create_circle(canvasName, x, y, r, **kwargs): #Function to generate circle
    return canvasName.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def generateClockWindow(clockDictionary): #Passing in a list of clocks objects
    global window #So that we can refer to it in other functions
    window = tk.Tk() #Calls window
    window.title("Clock app") #Changing title
    window.resizable(height = None, width = None) #Giving the window resizeable properties
    for location in clockDictionary:
        clockDictionary[location].generateDial()
        tk.Label(window, text = location).grid(row = clockDictionary[location].clockRow + 1, column = clockDictionary[location].clockColumn)
        time = clockDictionary[location].getTime()
        tk.Label(window, text = time[:-3]).grid(row = clockDictionary[location].clockRow + 2, column = clockDictionary[location].clockColumn)
    window.update_idletasks()
    # Code to generate a circle: create_circle(canvas, offset + dialSize/2, offset + dialSize/2, dialSize/2)

def generateTrigDicts(): #This function would be pretty hefty to run, but not sure how else to optimise
    #Dictionaries to be made global as they will be used throughout the code.
    global secondDict
    secondDict = {} #Used for x & y co-ordinates of second hand
    global minuteDict
    minuteDict = {} #Used for x & y co-ordinates of minute hand
    global hourDict
    hourDict = {} #Used for x & y co-ordinates of hour hand
    #Generating values for secondDict
    #Nested loop to obtain the hour:min pair for each possible angle
    for hour in range(0, 24):
        if len(str(hour)) == 1:
            hour = "0" + str(hour)
        for min in range(0, 60):
            if len(str(min)) == 1:
                min = "0" + str(min)
            key = str(hour) + ":" + str(min)
            angle = math.radians(30*(int(hour) % 12) + int(min)/2) + math.pi/2
            value = [-math.cos(angle), -math.sin(angle)]
            hourDict[key] = value
    for min in range(0, 60):
        if len(str(min)) == 1:
            min = "0" + str(min)
        for sec in range(0, 60):
            if len(str(sec)) == 1:
                sec = "0" + str(sec)
            key = str(min) + ':' + str(sec)
            angle = math.radians(6*int(min) + int(sec)/10) + math.pi/2
            value = [-math.cos(angle), -math.sin(angle)]
            minuteDict[key] = value
    for sec in range(0, 60): #When we reach here, we can add to the minute dictionary
        if len(str(sec)) == 1:
            sec = "0" + str(sec)
        for millis in range(0, 100):
            if len(str(millis)) == 1:
                millis = "0" + str(millis)
            key = str(sec) + ":" + str(millis)
            angle = math.radians(6*int(sec) + 3*int(millis)/50) + math.pi/2
            value = [-math.cos(angle), -math.sin(angle)]
            secondDict[key] = value

if __name__ == "__main__": #Main code
    fileName = "C:\\Users\\lavee\\OneDrive\\Documents\\GitHub\\Projects\\Python\\locationInfo.txt" #Text file that holds the location info
    #Text file is in the form
    with open(fileName, "r") as file:
        locationList = []
        subListIndex = -1 #Temporary variable used within the for loop to refer to each sublist
        for line in file: #List will split each location's data into it's own sublist
            line = line.strip("\n") #Removing new lines from text file
            if line == "": #New locations are indicated by blank lines (since \n was removed)
                locationList.append([]) #For the next location to be added here
                subListIndex += 1
            else:
                locationList[subListIndex].append(line)
        print(locationList)
    dialSize = 330 #Constant for the diameter of the dial
    clockDict = {} #Key = locationName, Value = clock(location, dst value, time difference)
    clockID = 0
    for list in locationList:
        clockDict[list[0]] = clock(list[0], list[1], list[2], dialSize, clockID) #Adding key/value pair
        clockID += 1
    generateTrigDicts()
    generateClockWindow(clockDict)
    refreshClock()
    window.mainloop()
