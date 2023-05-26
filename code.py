import FOON_class as FOON
from collections import deque

def parse_file(file):
    _file = open(file, 'r')
    items = _file.read().splitlines()
    item = None
    item_list = []

    for line in items:
        if line.startswith("O"):
            # -- we have an Object already in consideration which we were appending states to:
            if item:
                item_list.append(item)

            # -- this is an Object node, get the Object identifier by splitting first instance of O
            objectParts = line.split("O")
            objectParts = objectParts[1].split("\t")

            # -- create a new object which is equal to the kitchenItem and add it to the list:
            item = FOON.Object(objectID=int(
                objectParts[0]), objectLabel=objectParts[1])

        elif line.startswith("S"):
            # -- get the Object's state identifier by splitting first instance of S
            stateParts = line.split("S")
            stateParts = stateParts[1].split("\t")
            stateParts = list(filter(None, stateParts))

            # -- check if this object is a container or has ingredients:
            container = None
            list_ingredients = []
            if len(stateParts) > 2:
                if '{' in stateParts[2]:
                    # NOTE: all ingredients are enclosed in curly brackets:
                    ingredients = [stateParts[2]]
                    ingredients = ingredients[0].split("{")
                    ingredients = ingredients[1].split("}")

                    # -- we then need to make sure that there are ingredients to be read.
                    if len(ingredients) > 0:
                        ingredients = ingredients[0].split(",")
                        for I in ingredients:
                            list_ingredients.append(I)
                elif '[' in stateParts[2]:
                    # NOTE: a container is enclosed in square brackets (e.g. in [bowl]):

                    container = stateParts[2].replace('[', '').replace(']', '')
                else:
                    print(' -- WARNING: possibly incorrect or unexpected extra entry in line ' +
                          str(items.index(line)) + '? > ' + str(stateParts[2]))
                    pass

            item.addNewState(
                [int(stateParts[0]), stateParts[1], container])

            if list_ingredients:
                item.setIngredients(list_ingredients)

        else:
            pass
    # endfor

    item_list.append(item)

    _file.close()  # -- Don't forget to close the file once we are done!
    return item_list


# enddef


def parsing_foon_file(file):
    _file = open(file, 'r')
    items = _file.read().splitlines()
    item = None
    items_list = []
    input_list = []
    output_list = []
    input_output_list = []
    principal_list = []

    itemlist = []
    isOutput = False
    for line in items:
        if line.startswith("O"):
            # -- we have an Object already in consideration which we were appending states to:
            if item and isOutput:
                output_list.append(item)
            elif item and not isOutput:
                input_list.append(item)

            # -- this is an Object node, get the Object identifier by splitting first instance of O
            objectParts = line.split("O")
            objectParts = objectParts[1].split("\t")

            # -- create a new object which is equal to the kitchenItem and add it to the list:
            item = FOON.Object(objectID=int(
                objectParts[0]), objectLabel=objectParts[1])

        elif line.startswith("S"):
            # -- get the Object's state identifier by splitting first instance of S
            stateParts = line.split("S")
            stateParts = stateParts[1].split("\t")
            stateParts = list(filter(None, stateParts))

            # -- check if this object is a container or has ingredients:
            container = None
            list_ingredients = []
            if len(stateParts) > 2:
                if '{' in stateParts[2]:
                    # NOTE: all ingredients are enclosed in curly brackets:
                    ingredients = [stateParts[2]]
                    ingredients = ingredients[0].split("{")
                    ingredients = ingredients[1].split("}")

                    # -- we then need to make sure that there are ingredients to be read.
                    if len(ingredients) > 0:
                        ingredients = ingredients[0].split(",")
                        for I in ingredients:
                            list_ingredients.append(I)
                elif '[' in stateParts[2]:
                    # NOTE: a container is enclosed in square brackets (e.g. in [bowl]):

                    container = stateParts[2].replace('[', '').replace(']', '')
                else:
                    print(' -- WARNING: possibly incorrect or unexpected extra entry in line ' +
                          str(items.index(line)) + '? > ' + str(stateParts[2]))
                    pass

            item.addNewState(
                [int(stateParts[0]), stateParts[1], container])

            if list_ingredients:
                item.setIngredients(list_ingredients)
        elif line.startswith("M"):
            if item:
                input_list.append(item)
                item = None
                isOutput = True
        elif line.startswith("//"):
            isOutput = False
            if item:
                output_list.append(item)
            item = None
            if len(input_list):
                input_output_list.append(input_list)
                input_output_list.append(output_list)
                principal_list.append(input_output_list)
                input_output_list = []
                input_list = []
                output_list = []

        else:
            pass
    # endfor

    _file.close()  # -- Don't forget to close the file once we are done!
    return principal_list


# enddef

def listFromFoonFile(file):
    my_file = open(file, "r")
    content = my_file.read().split("//")
    content.remove(content[0])
    content.remove(content[-1])
    for i in range(0, len(content)):
        content[i] = content[i] + "//"
    return content


def searchNodeInOutput(node, principal_list):
    for i in range(0, len(principal_list)):
        for j in range(0, len(principal_list[i][1])):
            if (compareNodes(node, principal_list[i][1][j])):
                return i
    return -1


def searchNodeInInput(node, principal_list):
    for i in range(0, len(principal_list)):
        for j in range(0, len(principal_list[i][0])):
            if (compareNodes(node, principal_list[i][0][j])):
                return i
    return -1


def searchNodeWithLeastUnits(node, principal_list):
    possibleCandidate = {}
    for i in range(0, len(principal_list)):
        for j in range(0, len(principal_list[i][1])):
            if (compareNodes(node, principal_list[i][1][j])):
                possibleCandidate[i] = len(principal_list[i][0])

    if (possibleCandidate):
        return min(possibleCandidate, key=possibleCandidate.get)
    return -1


def getCandidates(node, principal_list):
    candidates = []
    for i in range(0, len(principal_list)):
        for j in range(0, len(principal_list[i][1])):
            if (compareNodes(node, principal_list[i][1][j])):
                candidates.extend(principal_list[i][0])


def compareNodes(node1, node2):
    if (node1.getObject() == node2.getObject()):
        return True


def nodeInList(node, checkList):
    for i in range(0, len(checkList)):
        if (compareNodes(node, checkList[i])):
            return True
    return False


if __name__ == '__main__':

    goal_nodes = parse_file('goal_nodes.txt')

    principal_list = parsing_foon_file('FOON.txt')

    foonList = listFromFoonFile('FOON.txt')

    for z in range(0, len(goal_nodes)):
        if searchNodeInOutput(goal_nodes[z], principal_list):
            content = []
            kitchen_list = parse_file('kitchen.txt')
            candidateList = []
            q = deque()
            q.append(goal_nodes[z])
            myset = set()
            while len(q):
                Node = q.popleft()
                if node is not in list(Node, kitchen_list)):
                    i = searchNodeInOutput(Node, principal_list)

                    if i >= 0 and id not in myset:
                        myset.add(i)
                        content.insert(0, foonList[i])
                        for k in principal_list[i][0]:
                            q.append(k)

                        kitchen_list.append(Node)

                    elif (i < 0):
                        print(" No path found for " + str(
                            z) + "th goal node when first candidate is considered every time")

        else:
            print("goal node is not found in output of foon file")

        f = open("solutionfile" + str(z) + ".txt", "w")
        f.writelines(content)
        f.close()

    for z in range(0, len(goal_nodes)):
        if searchNodeInOutput(goal_nodes[z], principal_list):
            content = []
            kitchen_list = parse_file('kitchen.txt')
            candidateList = []
            q = deque()
            q.append(goal_nodes[z])
            myset = set()
            while len(q):
                Node = q.popleft()
                if (not nodeInList(Node, kitchen_list)):
                    i = searchNodeWithLeastUnits(Node, principal_list)

                    if (i >= 0 and not i in myset):
                        myset.add(i)

                        content.insert(0, foonList[i])
                        for k in principal_list[i][0]:
                            q.append(k)

                        kitchen_list.append(Node)

                    elif (i < 0):
                        print(" No path found for " + str(
                            z) + "th goal node when first candidate is considered every time")

        else:
            print("goal node is not found in output of foon file")

        f = open("modifiedsolutionfile" + str(z) + ".txt", "w")
        f.writelines(content)
        f.close()