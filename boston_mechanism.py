'''
Boston Mechanism

'''
import numpy as np

# --------------------------------------Part 1 ------------------------------------
class Resident:
    def __init__(self, id, preferences):
        self.id = id
        self.prefs = preferences
        self.isMatched = False

class Hospital:
    def __init__(self, id, preferences, capacity):
        self.id = id
        self.prefs = preferences
        self.cap = capacity
        self.current_picks = []
        self.permanent_picks = []

def get_residents(filename):
    file = open(filename)
    residents = []
    for line in file:
        newline = ("".join(line.strip("\n"))).split(",")
        resident = [int(num) for num in newline]
        residents.append(resident)
    return residents

def get_hospitals(filename):
    file = open(filename)
    hospitals = []
    for line in file:
        newline = ("".join(line.strip("\n"))).split(",")
        hospital = [int(num) for num in newline]
        hospitals.append(hospital)
    return hospitals

def get_capacities(filename):
    file = open(filename)
    capacities = []
    for line in file:
        capacity = int(line.strip("\n"))
        capacities.append(capacity)
    return capacities

def deferred_acceptance(residents, hospitals):
    for id in residents.keys():
        apply_da(residents[id], residents, hospitals)
    return

def apply_da(resident, residents, hospitals):
    hospital_of_interest_id = resident.prefs.pop(0) #Gives hospital's id (int)
    hospital_of_interest = hospitals[hospital_of_interest_id]
    if (response_da(resident, residents, hospitals, hospital_of_interest) == True):
        return 
    else:
        apply_da(resident, residents, hospitals)

def response_da(resident, residents, hospitals, hosp):
    if (len(hosp.current_picks) < hosp.cap):
        hosp.current_picks.append(resident.id)
        hosp.current_picks = sorted(hosp.current_picks, key=lambda r: hosp.prefs.index(r))
        resident.isMatched = True
        return True
    else:
        resident_rank = hosp.prefs.index(resident.id)
        curr_min_rank = hosp.prefs.index(hosp.current_picks[-1])
        if (resident_rank < curr_min_rank):
            booted_resident_id = hosp.current_picks.pop() #Gives resident's id (int)
            hosp.current_picks.append(resident.id)
            hosp.current_picks = sorted(hosp.current_picks, key=lambda r: hosp.prefs.index(r))
            resident.isMatched = True
            booted_resident = residents[booted_resident_id]
            apply_da(booted_resident, residents, hospitals)
            return True
    return False

def boston_mechanism(residents, hospitals):
    num_unmatched = len(residents.keys())
    i = 0
    while (num_unmatched > 0):
        for id in residents.keys():
            if residents[id].isMatched == False:
                apply_bm(residents[id], residents, hospitals)
        response_bm(hospitals)
        for id in hospitals.keys():
            num_unmatched -= len(hospitals[id].current_picks)
            hospitals[id].cap -= len(hospitals[id].current_picks)
            hospitals[id].permanent_picks = hospitals[id].permanent_picks + hospitals[id].current_picks
            for resident_id in hospitals[id].permanent_picks:
                residents[resident_id].isMatched = True
            hospitals[id].current_picks = []   
        i += 1
    return

def apply_bm(resident, residents, hospitals):
    hospital_of_interest_id = resident.prefs.pop(0) #Gives hospital's id (int)
    hospital_of_interest = hospitals[hospital_of_interest_id]
    hospital_of_interest.current_picks.append(resident.id)
    return

def response_bm(hospitals):
    for id in hospitals.keys():
        hospital = hospitals[id]
        hospital.current_picks = sorted(hospital.current_picks, key=lambda r: hospital.prefs.index(r))
        if (len(hospital.current_picks) > hospital.cap):
            hospital.current_picks = hospital.current_picks[:hospital.cap]
    return

## DEFERRED ACCEPTANCE ##
print ("Running the deferred acceptance algorithm")
hosp_list = get_hospitals("hospitals.csv")
resid_list = get_residents("residents.csv")
cap_list = get_capacities("capacities.csv")

# resid_list = [[0,1,2], [0,2,1], [2,1,0], [2,1,0]]
# hosp_list = [[0,1,2,3], [0,2,3,1], [2,1,0,3]]
# cap_list = [1,1,2] 
residents = {}
hospitals = {}
for i in range(len(resid_list)):
    residents[i] = Resident(i, resid_list[i])
for i in range(len(hosp_list)):
    hospitals[i] = Hospital(i, hosp_list[i], cap_list[i])
deferred_acceptance(residents, hospitals)

#Repopulate residents dictionary to answer hw questions
residents = {}
resid_list = get_residents("residents.csv")
for i in range(len(resid_list)):
    residents[i] = Resident(i, resid_list[i])
applicant_preferences = {}
for hosp_id in hospitals.keys():
    hospital = hospitals[hosp_id]
    for res_id in hospital.current_picks:
        resident = residents[res_id]
        rank = resident.prefs.index(hosp_id)
        if rank not in applicant_preferences.keys():
            applicant_preferences[rank] = 1
        else:
            applicant_preferences[rank] += 1
for num in applicant_preferences.keys():
    print ("Number of residents assigned to there #" + str(num+1) + " preferred hospital is " + str(applicant_preferences[num]))
print ("--------------------------------------------")

## BOSTON MECHANISM ##
print ("Running the boston mechanism algorithm")
hosp_list = get_hospitals("hospitals.csv")
resid_list = get_residents("residents.csv")
cap_list = get_capacities("capacities.csv")

# resid_list = [[0,1,2], [0,2,1], [2,1,0], [2,1,0]]
# hosp_list = [[0,1,2,3], [0,2,3,1], [2,1,0,3]]
# cap_list = [1,1,2] 
residents = {}
hospitals = {}
for i in range(len(resid_list)):
    residents[i] = Resident(i, resid_list[i])
for i in range(len(hosp_list)):
    hospitals[i] = Hospital(i, hosp_list[i], cap_list[i])
boston_mechanism(residents, hospitals)
# for id in hospitals.keys():
#     print ("Hospital " + str(id) + " has chosen Residents " + str(hospitals[id].current_picks))
# for id in hospitals.keys():
#     print ("Hospital " + str(id) + " has chosen Residents " + str(hospitals[id].permanent_picks))

#Repopulate residents dictionary to answer hw questions
residents = {}
resid_list = get_residents("residents.csv")
for i in range(len(resid_list)):
    residents[i] = Resident(i, resid_list[i])
applicant_preferences = {}
for hosp_id in hospitals.keys():
    hospital = hospitals[hosp_id]
    for res_id in hospital.permanent_picks:
        resident = residents[res_id]
        rank = resident.prefs.index(hosp_id)
        if rank not in applicant_preferences.keys():
            applicant_preferences[rank] = 1
        else:
            applicant_preferences[rank] += 1
for num in applicant_preferences.keys():
    print ("Number of residents assigned to there #" + str(num+1) + " preferred hospital is " + str(applicant_preferences[num]))

# -------------------------------------- Part 2 -------------------------------------------

# !  Values -> advertiser 'row' will pay for keyword 'col' at this price
# !  Budgets -> the total budget of advertiser row
# !  Keywords -> Keywords for each round

budgets = np.genfromtxt("budgets.csv", dtype=int)
budgetsTotal = np.genfromtxt("budgets.csv", dtype=int)
keywords = np.genfromtxt("keywords.csv", dtype=int)
values = np.genfromtxt("values.csv", delimiter=',', dtype=int)


# ---------------------------- 3.a------------------------------------
def greedyAlg(budgets, keywords, values):
    greedyRevenue = 0
    round = 0
    while round < len(keywords):
        keyword = keywords[round]
        bidWinner = -1
        bidPrice = 0
        for i in range(len(budgets)):
            if budgets[i] >= values[i][keyword]:
                if bidPrice < values[i][keyword]:
                    bidPrice = values[i][keyword]
                    bidWinner = i
        if bidWinner != -1:
            budgets[bidWinner] -= bidPrice
            greedyRevenue += bidPrice
        round += 1
    print(greedyRevenue)