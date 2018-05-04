import psycopg2
import numpy as np
import random
import db

# Define matrix structure
# define slicing of features

# Main loop
# cosine similarity
# connect to db and fetch results from there
# build web interface


# DEFINITION AND SLICING OF EACH DIMENSION. todo: replace with actual values
# domHueSpace = ['c1', 'c2','c3','c4','c5','c6']
# saturationSpace = ['s1','s2','s3','s4','s5','s6','s7','s8']
# orientation = ['o1','o2','o3']

domHueSpace = [0, 1, 2, 3, 4, 5]
saturationSpace = [0, 1, 2, 3, 4, 5, 6, 7]
orientation = [0, 1, 2]

# POPULATION OF HYPERCUBES, BY COMBINING THE ABOVE SPACES

hypercubes = []
for i in range(0, len(domHueSpace)):
    for j in range(0, len(saturationSpace)):
        for k in range(0, len(orientation)):
            hypercubes.append(np.array([domHueSpace[i], saturationSpace[j], orientation[k]]))


def mainLoop():
    print("Welcome to the Moodboard Machine cli")
    selectedHypercube = raw_input("To start, select a random hypercube index (0-143): ")

    addToUserProfile(int(selectedHypercube), True)

    while True:

        print("selecting hypercube suggestion...")
        similarHypercubes = computeSimilarHypercube()
        suggestedHypercube = pickHypercube(similarHypercubes)

        print ("the suggested hypercube is:")
        print(hypercubes[suggestedHypercube])

        liked = raw_input("Do you like it? y or n: ")

        if liked == "y":
            addToUserProfile(suggestedHypercube, True)
        else:
            addToUserProfile(suggestedHypercube, False)

    return


# User profile
userProfile = []


def addToUserProfile(hypercubeIndex, liked):
    userProfile.append([hypercubeIndex, liked])

    #print("appended to profile" + hypercubeIndex )
    #print (len(userProfile))
    return


# compares all the user profile hypercubes with all the items in the list, to find similares. Returns similars
def computeSimilarHypercube():
    # for every hypercube in the profile, compare with the all the others to get the X most similar
    # decide to explore or exploit
    #

    selectedHypercubes = []  # the list of indexes of all selected similar hypercubes

    for i in range(0, len(userProfile)):

        userHypercube = userProfile[i][0]
        userHypercubeLiked = userProfile[i][1]

        simHypercubes = []  # list of tuples
        if userHypercubeLiked:
            for j in range(0, len(hypercubes)):  # create a list of tuples with all hypercubes and similarity values

                sim = cosineSimilarity(hypercubes[userHypercube], hypercubes[j])
                simHypercubes.append((j, sim))  # tuple (id, sim)

        sortedSim = sorted(simHypercubes, key=lambda x: x[1], reverse=True)  # sort by 2nd tuple item

        for k in range(0, NR_SIMILAR):

            indexHypercube = sortedSim[k][0]

            if (indexHypercube not in selectedHypercubes) and indexHypercube != userHypercube:  # avoid duplicates
                selectedHypercubes.append(indexHypercube)

    return selectedHypercubes


def pickHypercube(selectedHypercubes):

    if random.random() < EPSLON:  # exploration: pick random

        randIndex = random.randint(0, len(selectedHypercubes))

        return selectedHypercubes[randIndex]
    else:

        return selectedHypercubes[0]  # exploitation: pick item with highest similarity


def cosineSimilarity(hypercubeA, hypercubeB):
    dotProduct = np.dot(hypercubeA, hypercubeB)
    normA = np.linalg.norm(hypercubeA)
    normB = np.linalg.norm(hypercubeB)

    return dotProduct / (normA * normB)


# PARAMS

NR_SIMILAR = 20
EPSLON = .6


mainLoop()