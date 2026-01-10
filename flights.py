import time

class FlightData:
    def __init__(self, location):
        self.__flights = {}
        self.__cities = {}
        self.__parseCSV__(location)

    def __parseCSV__(self, loc: str):
        startTime = time.time()

        with open(loc) as reader:
            header = next(reader).strip().split(",")
            for line in reader:
                fields = line.strip().split(",")
                flightId = fields[0]

                self.__flights[flightId] = {}
                for i in range(1, len(fields) - 1):
                    self.__flights[flightId][header[i]] = fields[i]
                
                self.__addCityData__(flightId)
        
        print("Parsing CSV finished in %s seconds" % (time.time() - startTime))
                
    def __addCityData__(self, flightId):
        destination = self.__flights[flightId]["name_ades"]
        departure = self.__flights[flightId]["name_adep"]
        month = int(self.__flights[flightId]["date"].split("-")[1]) - 1

        if destination not in self.__cities:
            self.__cities[destination] = {}
            self.__cities[destination]["arrival_cities"] = set()
            self.__cities[destination]["monthly_arrivals"] = [0 for _ in range(12)]
        self.__cities[destination]["arrival_cities"].add(departure)
        self.__cities[destination]["monthly_arrivals"][month] += 1

    def getMonthlyArrivals(self, city):
        startTime = time.time()

        monthlyArrivals = self.__cities[city]["monthly_arrivals"]

        print("getMonthlyArrivals took %s seconds" % (time.time() - startTime))

        return monthlyArrivals

    def getDepartureCitiesToDestination(self, city):
        startTime = time.time()

        arrivalCities = self.__cities[city]["arrival_cities"]

        print("getDepartureCitiesToDestination took %s seconds" % (time.time() - startTime))

        return arrivalCities

    def getTotalFlightsBetween(self, startDay, startMonth, startYear, endDay, endMonth, endYear):
        startTime = time.time()

        count = 0
        for flight in self.__flights.values():
            date = flight["date"].split("-")
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])

            flightDate = year * 10000 + month * 100 + day
            startDate = startYear * 10000 + startMonth * 100 + startDay
            endDate = endYear * 10000 + endMonth * 100 + endDay

            if startDate <= flightDate <= endDate:
                count += 1

        print("getTotalFlightsBetween took %s seconds" % (time.time() - startTime))

        return count

flightData = FlightData("flight_list.csv")

monthlyArrivals = flightData.getMonthlyArrivals("Copenhagen")
departureCities = flightData.getDepartureCitiesToDestination("Ibiza")
totalFlights = flightData.getTotalFlightsBetween(20, 3, 2022, 21, 6, 2022)

print(f"Monthly Arrivals to Copenhagen: {monthlyArrivals}")
print(f"Departure Cities to Ibiza: {departureCities}")
print(f"Total Flights in Spring 2022: {totalFlights}")

def createTestCSV(fileName, content):
    with open(fileName, 'w') as f:
        f.write(content)

def runTest(testName, testFunction):
    result = testFunction()
    if result == True:
        print(f"{testName} PASS")
    else:
        print(f"{testName} FAIL")

def testSingleFlight():
