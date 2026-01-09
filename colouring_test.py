class NeighbourRelation:
    def __init__(self, nr):
        self.__nr = nr
        self.__nodes = list(set([c for (c, _) in nr] + [c for (_, c) in nr]))
        self.__colouring = []

    def __areNeighbours(self, c1, c2):
        return ((c1, c2) in self.__nr or (c2, c1) in self.__nr)

    def __canExtendColour(self, country, colour):
        for c in colour:
            if self.__areNeighbours(c, country):
                return False
        return True

    def __extendColouring(self, country, colouring):
        if colouring == []: return [[country]]
        else: 
            colour = colouring[0]
            if self.__canExtendColour(country, colour):
                # Beware!:  side effect
                colouring[0].append(country)
                return colouring
            else:
                return [colour] + self.__extendColouring(country, colouring[1:])

    def makeColouring(self):
        for c in self.__nodes:
            self.__colouring = self.__extendColouring(c, self.__colouring)

    def __str__(self):
        return str(self.__colouring)
    
    def getColours(self):
        return self.__colouring
    
    def getNodes(self):
        return self.__nodes

def runTest(testName, relations, expectedColours):
    print(testName)
    print(f"Input: {relations}")
    nr = NeighbourRelation(relations)
    nr.makeColouring()
    result = nr.getColours()
    print(f"Output: {result}")

    violations = revealViolations(nr, relations, result)
    if (not len(violations) == 0):
        print("Result: FAIL")
        print(f"There are violations in colouring: {violations} \n")
        return
    
    print(f"Expected colours: {expectedColours}")
    if len(result) == expectedColours:
        print("Result: PASS \n")
    else:
        print("Result: FAIL \n")

def revealViolations(nr, relations, colouring):
    violations = []

    for node in nr.getNodes():
        nodeFound = False
        duplicateCount = 0
        for colour in colouring:
            for country in colour:
                if node == country:
                    nodeFound = True
                    duplicateCount += 1
        if not nodeFound:
            violations.append(("Country not added to colours", node))
        elif duplicateCount > 1:
            violations.append(("Country found in more than one colour", node))

    for colour in colouring:
        if colour == []:
            violations.append("Empty List")
            continue

        for country1 in colour:
            for country2 in colour:
                checkedSelf = False
                if country1 == country2:
                    if checkedSelf:
                        violations.append(("Duplicate country found in same colour", country1))
                        continue
                    checkedSelf = True

                if (country1, country2) in relations or (country2, country1) in relations:
                    violations.append(("Neighbouring countries share same colour", (country1, country2)))
    return violations

# Control Cases
runTest("Control Small", [("a", "b"), ("b", "a"), ("b", "c"), ("c", "b")], 2)
runTest("Control Medium", [("da", "se"), ("no", "da"), ("se", "no"), ("de", "da")], 3)
runTest("Control Large", [("a", "b"), ("b", "a"), ("b", "c"), ("c", "b"), ("c", "d"), ("d", "c"), ("d", "e"), ("e", "d"), ("e", "f"), ("f", "e"), ("a", "f"), ("f", "a")], 2)

# Edge Cases
runTest("Edge Empty", [], 0)
runTest("Edge Single", [("a", "b")], 2)
runTest("Edge Self Loop (Ignore failed test)", [("a", "a")], 1)

# Graph Cases
runTest("Graph Disconnected", [("a", "b"), ("b", "a"), ("c", "d"), ("d", "c")], 2)
runTest("Graph Cycle Odd", [("a", "b"), ("b", "a"), ("b", "c"), ("c", "b"), ("c", "a"), ("a", "c")], 3)
runTest("Graph Complete", [("a", "b"), ("b", "a"), ("a", "c"), ("c", "a"), ("a", "d"), ("d", "a"), ("b", "c"), ("c", "b"),("b", "d"), ("d", "b"), ("c", "d"), ("d", "c")], 4)

# Symmetry Cases
runTest("Symmetry Full", [("da", "se"), ("se", "da"), ("no", "da"), ("da", "no")], 2)
runTest("Symmetry Asymmetric", [("da", "se"), ("no", "da"), ("se", "no")], 3)
runTest("Symmetry Mixed", [("a", "b"), ("b", "a"), ("b", "c"), ("c", "d")], 2)

# Duplicate Cases
runTest("Duplicate Exact", [("a", "b"), ("a", "b"), ("b", "c"), ("c", "b")], 2)
runTest("Duplicate Symmetric", [("a", "b"), ("b", "a"), ("a", "b"), ("b", "a")], 2)
runTest("Duplicate Mixed", [("a", "b"), ("b", "c"), ("a", "b"), ("c", "b"), ("b", "c")], 2)
