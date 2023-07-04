from howlongtobeatpy import HowLongToBeat
from tkinter import *
from PredictiveAnalytics import *
import numpy as np
import os

# return string, button
def textInput(frame, w=40):
    text = StringVar()
    text_box = Entry(frame, width=w, textvariable=text)
    text_box.pack(expand=True)
    return text, text_box

def intInput(frame, w=5):
    text = IntVar()
    text_box = Entry(frame, width=w, textvariable=text)
    text_box.pack(expand=True)
    return text

def floatInput(frame, w=5):
    text = DoubleVar()
    text_box = Entry(frame, width=w, textvariable=text)
    text_box.pack(expand=True)
    return text

def addText(frame, text, font=('Helvetica', '14')):
    bgC = frame.cget('bg')
    Label(frame, text=text, font=font, bg=bgC).pack(expand=True)

def addPopUp(name, buttonFunc):
    def tempFunc():
        popUp.destroy()
        buttonFunc()
    popUp = Toplevel()
    popUp.geometry('100x100')
    Label(popUp, text=name).pack(expand=True)
    Button(popUp, text='OK', command=tempFunc).pack(expand=True)

def resetGUI(frame):
    frame.destroy()

def mainSearchGame(gui):
    frame = Frame(gui, bg=gui.cget('bg'))
    frame.pack(expand=True, fill=BOTH)
    def addGameName():
        outputBox.delete(0, outputBox.size())
        outputBox.yview()
        string = gameName.get()
        temp = HowLongToBeat().search(string, similarity_case_sensitive=False)
        for i, elem in enumerate(temp):
            outputBox.insert(i+1, elem.game_name + ';' + elem.game_id)
        outputBox.pack(expand=True)
        addGameButton.pack(expand=True)
    def addGame():
        tup = outputBox.curselection()
        gameName = outputBox.get(tup)
        resetGUI(frame)
        mainAddGame(gui, gameName)
    def goToPredict():
        resetGUI(frame)
        mainGamePredict(gui)
    addText(frame, 'Search for a game to add to your current collection:')
    gameName = StringVar()
    text_box = Entry(frame, width=40, textvariable=gameName)
    text_box.bind('<Return>', lambda x: addGameName())
    text_box.pack(expand=True)
    outputBox = Listbox(frame, height=10, width=60, font=('Helvetica', '14'))
    outputBox.bind('<Double-Button-1>', lambda x: addGame())
    addGameButton = Button(frame, text='add game', command=addGame)
    Button(frame, text='Make Predictions', command=goToPredict).pack(expand=True)

def mainAddGame(gui, gameName):
    frame = Frame(gui, bg=gui.cget('bg'))
    frame.pack(expand=True, fill=BOTH)
    def findGame(gameName):
        gameID = gameName.split(';')[1].strip()
        game = HowLongToBeat().search_from_id(int(gameID))
        return game
    def cancelButton():
        resetGUI(frame)
        mainSearchGame(gui)
    def getGenres():
        with open('gameGenres.txt', 'r') as f:
            return f.read().split('\n')
    def addGenre():
        genre_s = fullGenreBox.curselection()
        for elem in genre_s:
            selectedGenres.add(fullGenreBox.get(elem))
        selectedGenreBox.delete(0, selectedGenreBox.size())
        for elem in selectedGenres:
            selectedGenreBox.insert(1, elem)
    def writeGameToFile():
        with open('gamesProfile.txt', 'r') as file:
            games = file.read().split('\n')
        gameIDlist = [int(game.split(',')[0]) for game in games if game != '']
        gameData = findGame(gameName)
        if gameData is None:
            addPopUp('Game not found', cancelButton)
        else:
            if int(gameData.game_id) in gameIDlist:
                addPopUp('Game already in profile', cancelButton)
            else:
                genres = []
                for elem in genreArray:
                    if elem in selectedGenres:
                        genres.append('1')
                    else:
                        genres.append('0')
                arrToWrite = [str(gameData.game_id), gameData.game_name]
                gmpMain = gameData.gameplay_main
                gmpMainPE = gameData.gameplay_main_extra
                gmpComp = gameData.gameplay_completionist
                if gmpMain[-1].isdigit():
                    if int(gmpMain) > 0:
                        arrToWrite.append(gmpMain)
                    else:
                        arrToWrite.append('0')
                else:
                    arrToWrite.append(gmpMain[0:-1]+'.5')
                if gmpMainPE[-1].isdigit():
                    if int(gmpMainPE) > 0:
                        arrToWrite.append(gmpMainPE)
                    else:
                        arrToWrite.append('0')
                else:
                    arrToWrite.append(gmpMainPE[0:-1]+'.5')
                if gmpComp[-1].isdigit():
                    if int(gmpComp) > 0:
                        arrToWrite.append(gmpComp)
                    else:
                        arrToWrite.append('0')
                else:
                    arrToWrite.append(gmpComp[0:-1]+'.5')
                arrToWrite = arrToWrite + genres
                with open('gamesProfile.txt', 'a') as file:
                    file.write(','.join(arrToWrite) + ',' + str(hours.get()) + '\n')
                    file.flush()
                addPopUp('Game added', cancelButton)
    def genreSearch():
        def checkStrs(str1, str2):
            str1 = str1.lower()
            str2 = str2.lower()
            return str2 in str1
        filteredGenre = genreSearchVar.get()
        fullGenreBox.delete(0, fullGenreBox.size())
        for i, elem in enumerate(genreArray):
            if checkStrs(elem, filteredGenre):
                fullGenreBox.insert(i+1, elem)
        fullGenreBox.pack(expand=True)
    def removeGenre():
        genre = selectedGenreBox.curselection()
        selectedGenres.remove(selectedGenreBox.get(genre))
        selectedGenreBox.delete(genre)
        # for elem in selectedGenres:
        #     selectedGenreBox.insert(1, elem)
    addText(frame, 'Add hours and genres to '+gameName.split(';')[0]+':', font=('Helvetica', '11'))
    addText(frame, '(It\'s recommended that use the genre\'s under the game\'s steam page)', font=('Helvetica', '10'))
    Button(frame, text='cancel', command=cancelButton).pack(expand=True)
    addText(frame, 'hours:')
    hours = floatInput(frame)
    addText(frame, 'genres:')
    genreSearchVar, genreSearchBox = textInput(frame, 20)
    genreSearchBox.bind('<Return>', lambda x: genreSearch())
    fullGenreBox = Listbox(frame, height=20, width=30, font=('Helvetica', '13'), selectmode=MULTIPLE)
    selectedGenreBox = Listbox(frame, height=20, width=30, font=('Helvetica', '13'), selectmode=SINGLE)
    genreArray = getGenres()
    selectedGenres = set()
    genreArray.sort()
    for i, elem in enumerate(genreArray):
        fullGenreBox.insert(i+1, elem)
    fullGenreBox.pack(expand=True, side=LEFT)
    fullGenreBox.bind('<Double-Button-1>', lambda x: addGenre())
    selectedGenreBox.pack(expand=True, side=RIGHT)
    selectedGenreBox.bind('<Double-Button-1>', lambda x: removeGenre())
    Button(frame, text='add game', command=writeGameToFile).pack(expand=True, side=BOTTOM)
    
def mainGamePredict(gui):
    frame = Frame(gui, bg=gui.cget('bg'))
    frame.pack(expand=True, fill=BOTH)
    def addGameName():
        outputBox.delete(0, outputBox.size())
        outputBox.yview()
        string = gameName.get()
        temp = HowLongToBeat().search(string, similarity_case_sensitive=False)
        for i, elem in enumerate(temp):
            outputBox.insert(i+1, elem.game_name + ';' + elem.game_id)
        outputBox.pack(expand=True)
        addGameButton.pack(expand=True)
    def addGame():
        tup = outputBox.curselection()
        gameName = outputBox.get(tup)
        resetGUI(frame)
        predictAddGame(gui, gameName)
    def goToAdd():
        resetGUI(frame)
        mainSearchGame(gui)
    addText(frame, 'Search for a game to make a predictions for:')
    gameName = StringVar()
    text_box = Entry(frame, width=40, textvariable=gameName)
    text_box.bind('<Return>', lambda x: addGameName())
    text_box.pack(expand=True)
    outputBox = Listbox(frame, height=10, width=60, font=('Helvetica', '14'))
    outputBox.bind('<Double-Button-1>', lambda x: addGame())
    addGameButton = Button(frame, text='add game', command=addGame)
    Button(frame, text='Add Game(s)', command=goToAdd).pack(expand=True, side=BOTTOM)

def predictAddGame(gui, gameName):
    frame = Frame(gui, bg=gui.cget('bg'))
    frame.pack(expand=True, fill=BOTH)
    def findGame(gameName):
        game = HowLongToBeat().search_from_id(int(gameID))
        return game
    def cancelButton():
        resetGUI(frame)
        mainGamePredict(gui)
    def getGenres():
        with open('gameGenres.txt', 'r') as f:
            return f.read().split('\n')
    def addGenre():
        genre_s = fullGenreBox.curselection()
        for elem in genre_s:
            selectedGenres.add(fullGenreBox.get(elem))
        selectedGenreBox.delete(0, selectedGenreBox.size())
        for elem in selectedGenres:
            selectedGenreBox.insert(1, elem)
    def makePredictions():
        with open('gamesProfile.txt', 'r') as file:
            games = file.read().split('\n')
        gameIDlist = [int(game.split(',')[0]) for game in games if game != '']
        gameData = findGame(gameName)
        if gameData is None:
            addPopUp('Game not found', cancelButton)
        else:
            if int(gameData.game_id) in gameIDlist:
                addPopUp('Game already in profile', cancelButton)
            else:
                genres = []
                for elem in genreArray:
                    if elem in selectedGenres:
                        genres.append('1')
                    else:
                        genres.append('0')
                arrToWrite = [str(gameData.game_id), gameData.game_name]
                gmpMain = gameData.gameplay_main
                gmpMainPE = gameData.gameplay_main_extra
                gmpComp = gameData.gameplay_completionist
                if gmpMain[-1].isdigit():
                    if int(gmpMain) > 0:
                        arrToWrite.append(gmpMain)
                    else:
                        arrToWrite.append('0')
                else:
                    arrToWrite.append(gmpMain[0:-1]+'.5')
                if gmpMainPE[-1].isdigit():
                    if int(gmpMainPE) > 0:
                        arrToWrite.append(gmpMainPE)
                    else:
                        arrToWrite.append('0')
                else:
                    arrToWrite.append(gmpMainPE[0:-1]+'.5')
                if gmpComp[-1].isdigit():
                    if int(gmpComp) > 0:
                        arrToWrite.append(gmpComp)
                    else:
                        arrToWrite.append('0')
                else:
                    arrToWrite.append(gmpComp[0:-1]+'.5')
                arrToWrite = arrToWrite + genres
                resetGUI(frame)
                predictGUI(gui, arrToWrite)
    def genreSearch():
        def checkStrs(str1, str2):
            str1 = str1.lower()
            str2 = str2.lower()
            return str2 in str1
        filteredGenre = genreSearchVar.get()
        fullGenreBox.delete(0, fullGenreBox.size())
        for i, elem in enumerate(genreArray):
            if checkStrs(elem, filteredGenre):
                fullGenreBox.insert(i+1, elem)
        fullGenreBox.pack(expand=True)
    def removeGenre():
        genre = selectedGenreBox.curselection()
        selectedGenres.remove(selectedGenreBox.get(genre))
        selectedGenreBox.delete(genre)
    gameID = gameName.split(';')[1].strip()
    try:
        file = open('cache.txt', 'r')
    except IOError:
        file = open('cache.txt', 'w+')
    file.close()
    with open('cache.txt', 'r') as f:
        gamesArr = f.read().split('\n')
    gamesArr = [game.split(',') for game in gamesArr if game != '']
    if gameID in [game[0] for game in gamesArr]:
        for elem in gamesArr:
            if elem[0] == gameID:
                targetGame = elem
                break
        resetGUI(frame)
        predictGUI(gui, [targetGame[0]] + ['tempName'] + targetGame[1:] + [-1])
    else:
        addText(frame, 'Add genre(s) to '+gameName.split(';')[0]+', and we will make the hours prediction:', font=('Helvetica', '11'))
        addText(frame, '(It\'s recommended that use the genre\'s under the game\'s steam page)', font=('Helvetica', '10'))
        Button(frame, text='cancel', command=cancelButton).pack(expand=True)
        addText(frame, 'genres:')
        genreSearchVar, genreSearchBox = textInput(frame, 20)
        genreSearchBox.bind('<Return>', lambda x: genreSearch())
        fullGenreBox = Listbox(frame, height=20, width=60, font=('Helvetica', '13'), selectmode=MULTIPLE)
        selectedGenreBox = Listbox(frame, height=20, width=40, font=('Helvetica', '13'), selectmode=SINGLE)
        genreArray = getGenres()
        selectedGenres = set()
        genreArray.sort()
        for i, elem in enumerate(genreArray):
            fullGenreBox.insert(i+1, elem)
        fullGenreBox.pack(expand=True, side=LEFT)
        fullGenreBox.bind('<Double-Button-1>', lambda x: addGenre())
        selectedGenreBox.pack(expand=True, side=RIGHT)
        selectedGenreBox.bind('<Double-Button-1>', lambda x: removeGenre())
        Button(frame, text='Predict Game', command=makePredictions).pack(expand=True, side=BOTTOM)

def predictGUI(gui, input):
    frame = Frame(gui, bg=gui.cget('bg'))
    frame.pack(expand=True, fill=BOTH)
    def cancelButton():
        resetGUI(frame)
        mainSearchGame(gui)
    def writeToCache(input):
        input = input[0] + ',' + ','.join(input[2:])
        with open('cache.txt', 'a') as f:
            f.write(input+'\n')
    with open('gamesProfile.txt', 'r') as file:
        games = file.read().split('\n')
    games = np.array([game.split(',') for game in games if game != ''])
    data = games[:, 2:].astype(np.float32)
    if input[-1] == -1:
        input = input[0:-1]
    else:
        writeToCache(input)
    input = np.array([np.array(input)[2:].astype(np.float32)])
    predSVM, lossSVM = SVM(data, input)
    predNN, lossNN = DNN_RELU(data, input)
    predNN2, lossNN2 = DNN_IDN(data, input)
    predSGD, lossSGD = SGD(data, input)
    predSVD, lossSVD = SVD(data, input)
    addText(frame, 'SVM: '+str(round(predSVM[0], 2))+' hours, loss: '+str(round(lossSVM, 2)), font=('Helvetica', '11'))
    addText(frame, 'NN (RELU): '+str(round(predNN[0], 2))+' hours, loss: '+str(round(lossNN, 2)), font=('Helvetica', '11'))
    addText(frame, 'NN (IDN): '+str(round(predNN2[0], 2))+' hours, loss: '+str(round(lossNN2, 2)), font=('Helvetica', '11'))
    addText(frame, 'SGD: '+str(round(predSGD[0], 2))+' hours, loss: '+str(round(lossSGD, 2)), font=('Helvetica', '11'))
    addText(frame, 'SVD: '+str(round(predSVD[0,0], 2))+' hours, loss: '+str(round(lossSVD, 2)), font=('Helvetica', '11'))
    addText(frame, 'Mean: ' + str(round(np.mean([predSVM[0], predNN[0], predNN2[0], predSGD[0], predSVD[0,0]]), 2))+' hours', font=('Helvetica', '11'))
    Button(frame, text='return', command=cancelButton).pack(expand=True, side=BOTTOM)

if __name__ == '__main__':
    gui = Tk()
    gui.title('How Long to Beat')
    gui.geometry('1000x800')
    gui.config(bg='#84BF04')
    mainSearchGame(gui)
    gui.mainloop()
