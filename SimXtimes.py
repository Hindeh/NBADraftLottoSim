#Author: Hunter Hinde
#Description: Will run draft sim Code X times and output results to a CSV file.
from numpy.random import choice
import csv
#REMINDER: team 1 is the worst team and is at the top of the file
#REMINDER: RunSim has some odds included, but more can be added there and named for ease of use later.
OUTFI = "testing.csv" #name of the output CSV file. (keep .csv for ease of use)
NUMSIMS = 100 #The number of simulations to run
NUMTEAMS = 16 #The number of teams we are making. Can do more teams than odds, and will be blank in output CSV.
ALLLOTTO = True
def makeText(numTeams):
    # makes team names, and header for CSV since already in that loop
    header = ["Team #"]
    team_names = []
    for i in range(numTeams):
        teamName ="Team " + str(i+1)
        team_names.append(teamName)

        pickNum = "Pick " + str(i+1)
        header.append(pickNum)
    return header, team_names

def runSim(team_names, display = False,check = False,allLotto = False):
    """team_names is the output of makeText(). display is for error checking, and so is check. allLotto changes
    whether or not we are drawing all 14 or only the first 4 picks"""
    # get draft results in raw format
    # Run the drawing, removing selected teams once chosen, uses standings after the 5th pick
    order = []
    picked = 0
    baseOdds = {
        0: 140,
        1: 140,
        2: 140,
        3: 125,
        4: 105,
        5: 90,
        6: 75,
        7: 60,
        8: 45,
        9: 30,
        10: 20, #four play in losers
        11: 15,
        12: 10,
        13: 5,}
    playIn14 = { #has been editted from base odds
        0: 140,
        1: 130,
        2: 120,
        3: 110,
        4: 100,
        5: 90,
        6: 80,
        7: 70,
        8: 60,
        9: 50,
        10: 18, #four play in losers
        11: 15,
        12: 10,
        13: 7,}
    playIn16 = { #play-in adjusted odds 16 teams HJH version
        0: 140,
        1: 130,
        2: 120,
        3: 105,
        4: 90,
        5: 85,
        6: 75,
        7: 65,
        8: 55,
        9: 45,
        10: 35,
        11: 25,
        12: 9, # assume we still have 4 play in losers
        13: 8,
        14: 7,
        15: 6}
    oddsChoice = playIn16
    if check:
        print(1000)
        print(sum(oddsChoice.values()))
    if allLotto == False:
        while picked < 4 :
            total = float(sum(oddsChoice.values()))
            draw = choice(list(oddsChoice.keys()), 1, p=[oddsChoice[c] / total for c in oddsChoice])[0]
            order.append(team_names[draw])
            del oddsChoice[draw]
            picked +=1

        #now make order with the worst teams after the fourth pick is drawn
        #start with the worst team
        for team in team_names:
            if team not in order:
                order.append(team)

    if allLotto == True:
        while picked < NUMTEAMS :
            total = float(sum(oddsChoice.values()))
            draw = choice(list(oddsChoice.keys()), 1, p=[oddsChoice[c] / total for c in oddsChoice])[0]
            order.append(team_names[draw])
            del oddsChoice[draw]
            picked +=1


    if display: ##Debugging option
        print(order)
        for i, result in enumerate(order):
            if (1+i) < 10:
                print('#%d:  %s' % (1+i, result))
            else:
                print('#%d: %s' % (1+i, result))
    #gives list of the order
    return order

def makeDics(team_names):
    #team_names is a list of team names from the getTeamNames function
    listDics = [] ##lost of all dictionaries in order, so no need for names as first dic is team 1
    for team in team_names:
        teamDic = team
        teamDic = {}
        listDics.append(teamDic)
        for i in range(len(team_names)):
            teamDic[i+1] = 0

    return listDics

def simOnce(listDics,team_names):
    ##runs sim once and adds results to dictionaries as output
    draftOrder = runSim(team_names, ALLLOTTO) #can change allLotto here!
    pick = 1
    for team in draftOrder: #goes through the list in order starting with best pick
        #hard coded to get the number from how I named the teams i.e. team 1 team 2 ... team 14
        #could easily change so that team names can be changed but I do not want to do that since I won't change it
        if len(team) == 6:
            entry = team[-1]
            entry = int(entry)

        elif len(team) == 7:
            entry = team[5:7]
            entry = int(entry)

        listDics[entry-1][pick] +=1

        pick +=1

    return listDics

def simX (listDics,numSims,team_names):
    #is essientially a for loop for simOnce with numSims being how many times
    for i in range(numSims): # runs numSims times
        listDics = simOnce(listDics,team_names)
    return listDics

def outputCSV(listDics,header):
    #makes listDics into a nice neat output File with Headers
    #returns nothing
    with open(OUTFI,'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        count = 1
        for team in listDics:
            name = "Team " + str(count)
            line = [name]
            vals = list(team.values())
            line.extend(vals) #put list of values instead of 5
            writer.writerow(line)
            count += 1

    file.close()

def main(): # does not need to be adjusted. Change global variables and RunSim
    # puts together all the functions to make the CSV
    header,team_names = makeText(NUMTEAMS)
    listDics = makeDics(team_names)
    listDics = simX(listDics,NUMSIMS,team_names)
    outputCSV(listDics,header)
    print("Finished!") #helps when simulations take a long time!

def oddsCheck(oddsToUse = None): #debugging purposes for odds with an option to input as well
    baseOdds = { #has been editted from base odds
        0: 140,
        1: 140,
        2: 140,
        3: 125,
        4: 105,
        5: 90,
        6: 75,
        7: 60,
        8: 45,
        9: 30,
        10: 20, #four play in losers
        11: 15,
        12: 10,
        13: 5,}
    playIn14 = { #has been editted from base odds
        0: 140,
        1: 130,
        2: 120,
        3: 110,
        4: 100,
        5: 90,
        6: 80,
        7: 70,
        8: 60,
        9: 50,
        10: 18, #four play in losers
        11: 15,
        12: 10,
        13: 7,}
    playIn16 = { #play-in adjusted odds 16 teams
        0: 140,
        1: 130,
        2: 120,
        3: 105,
        4: 90,
        5: 85,
        6: 75,
        7: 65,
        8: 55,
        9: 45,
        10: 35,
        11: 25,
        12: 9, # assume we still have 4 play in losers
        13: 8,
        14: 7,
        15: 6}
    oddsToUse= playIn16
    total = sum(oddsToUse.values())
    print("Total of odds. Should equal 1,000: ",total)
    print("Amount of teams. Should equal %i: " % NUMTEAMS, len(oddsToUse))

oddsCheck() #Run a check just in case

if __name__ == "__main__":
    main()