from click._compat import raw_input
import git
import sys
import datetime

# repo = git.Repo()
# o = repo.remotes.origin
# o.pull()

g = git.Git()
g.pull('origin', 'master')

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=2)
yesterday = str(yesterday)


class County:
    def __init__(self, date, name, state, cases, deaths):
        self.name = name
        self.state = state
        self.cases = cases
        self.deaths = deaths
        self.date = date


class State:
    def __init__(self, date, state, cases, deaths):
        self.state = state
        self.cases = cases
        self.deaths = deaths
        self.date = date


states = {}

counties = {"null": {"null": "null"}}

with open("us-states.csv") as stateFile:
    next(stateFile)
    for line in stateFile:
        parts = line.split(",")
        state = State(parts[0], parts[1], parts[3], parts[4])
        if states.get(state.state.lower(), "null") == "null":
            states[state.state.lower()] = state
        elif states.get(state.state.lower()).date < state.date:
            states[state.state.lower()] = state

with open("us-counties.csv") as countyFile:
    next(countyFile)
    for line in countyFile:
        parts = line.split(",")
        county = County(parts[0], parts[1], parts[2], parts[4], parts[5])
        if counties.get(county.state.lower(), "null") == "null":
            counties[county.state.lower()] = {}
            counties[county.state.lower()][county.name.lower()] = county
        else:
            stateCounties = counties.get(county.state.lower())
            if stateCounties.get(county.name, "null") == "null":
                counties[county.state.lower()][county.name.lower()] = county
        if counties[county.state.lower()][county.name.lower()].date < county.date:
            counties[county.state.lower()][county.name.lower()] = county

counties.pop("null")

print("Enter state or county and state seperated by a comma\nExample: Ottawa, Michigan\nOr: Michigan\n")
while True:
    input = raw_input("Input: ").strip()
    parts = input.split(",")
    input = input.lower()
    if input == "quit" or input == "exit":
        sys.exit(0)
    elif input == "searchables":
        for key in states.keys():
            print(states.get(key).state)
        for key1 in counties.keys():
            for key2 in counties[key1].keys():
                county = counties[key1][key2]
                print(county.name + ", " + county.state)
        continue
    try:
        toPrint = ""
        print("\n")
        if len(parts) == 1:
            state = states[parts[0].lower()]
            toPrint = state
        else:
            county = counties[parts[1].lower().strip()][parts[0].lower().strip()]
            toPrint = county
            print("County: " + toPrint.name)

        print("State: " + toPrint.state)
        print("Cases: " + toPrint.cases)
        print("Deaths: " + toPrint.deaths)
    except:
        print("Invalid query: Type quit to exit")
