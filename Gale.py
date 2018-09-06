import re


def readIn():
    rejectorsPreferences = dict()
    proposersPreferences = dict()
    proposersLeft = list()
    n = 0
    nameDic = dict()

    with open("friends.txt") as f:
        regex = re.compile(r"\d+\:+")
        regexNames = re.compile(r"\d+\s+[A-Z]+")

        for line in f:
            if line.startswith("n"):
                n = int(line.split("=")[1])

            elif regexNames.search(line) is not None:
                id_num = int(line.split(" ")[0])
                name = line.split(" ")[1]
                nameDic[id_num] = name
            elif regex.search(line) is not None:
                preferencee = int(line.split(":")[0])
                list_preferences = [int(s) for s in line.split(" ")[1:]]

                if preferencee % 2 == 0:
                    # if first number is even, put in rejector dict
                    rejectorsPreferences[preferencee] = list_preferences
                else:

                    # if the first number is odd, put in proposer dict
                    proposersPreferences[preferencee] = list_preferences
                    proposersLeft.append(preferencee)

    gggale = Gale(proposersPreferences, rejectorsPreferences, proposersLeft, nameDic, n)


class Gale(object):

    proposersPreferences = dict()
    rejectorsPreferences = dict()
    n = 0
    proposersLeft = list()  # list of proposers who do not yet have a match
    nameDic = dict()

    def __init__(self, proposersPreferences, rejectorsPreferences, proposersLeft, nameDic, n):

        # dict of proposer IDs mapped to their lists of preferred IDs
        self.proposersPreferences = proposersPreferences
        # dict of rejector IDs mapped to their lists of preferred IDs
        self.rejectorsPreferences = rejectorsPreferences
        self.proposersLeft = proposersLeft
        # number of proposers
        self.n = n
        self.nameDic = nameDic

        # list of the matching (initially all 0s before any mapping takes place)
        # for proposerMatching: index = proposer, value = rejector that they're mapped to
        # for rejectorMatching: index = rejector, value = proposer they're matched to
        self.proposerMatching = list()
        self.rejectorMatching = list()
        for i in range((n*2)+1):
            self.proposerMatching.append(0)
            self.rejectorMatching.append(0)

        self.gale()

    def gale(self):
        # run the algorithm while there are still proposers left

        while not len(self.proposersLeft) == 0:
            # get a proposer from the list of left proposers
            proposer = self.proposersLeft.pop(0)
            self.propose(proposer)

        self.print_gale()

    def propose(self, proposer):
        accepted = False
        # get proposer's preferences from the dict
        prefs = self.proposersPreferences.get(proposer)

        while not accepted:
            # pop the first preference in the list
            nextPref = prefs.pop(0)

            # check whether that person has a match already:
            if self.rejectorMatching[nextPref] == 0:
                # if not, match them in the matching list
                self.proposerMatching[proposer] = nextPref
                self.rejectorMatching[nextPref] = proposer
                accepted = True

            else:
                rejectorsCurrentMatch = self.rejectorMatching[nextPref]
                listOfPreferences = self.rejectorsPreferences.get(nextPref)
                priorityOfRejectorCurrentMatch = listOfPreferences.index(rejectorsCurrentMatch)
                priorityOfRejectorProposedMatch = listOfPreferences.index(proposer)
                # check if the proposed match is higher in the rejectors list of preferences
                if priorityOfRejectorCurrentMatch > priorityOfRejectorProposedMatch:
                    # if it is, change matching
                    oldProposer = self.rejectorMatching[nextPref]
                    self.proposersLeft.append(oldProposer)
                    self.proposerMatching[oldProposer] = 0
                    self.proposerMatching[proposer] = nextPref
                    self.rejectorMatching[nextPref] = proposer
                    accepted = True

    def print_gale(self):

        for i in range(len(self.proposerMatching)):
            if self.proposerMatching[i] is not 0:

                print(i, " -- ", self.proposerMatching[i])
                #print(self.nameDic.get(i), " -- ", self.nameDic.get(self.proposerMatching[i]))


readIn()
