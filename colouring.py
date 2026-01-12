## This is the version without the bugs
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