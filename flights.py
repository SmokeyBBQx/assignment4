import time

flights = {}
cities = {}

def parseCSV(loc: str):
    with open(loc) as reader:
        header = next(reader).strip().split(",")
        for line in reader:
            fields = line.strip().split(",")
            flightId = fields[0]

            flights[flightId] = {}
            for i in range(1, len(fields) - 1):
                flights[flightId][header[i]] = fields[i]
            
            addCityData(flightId)
            
def addCityData(flightId):
    destination = flights[flightId]["name_ades"]
    departure = flights[flightId]["name_adep"]
    month = int(flights[flightId]["date"].split("-")[1]) - 1

    if destination not in cities:
        cities[destination] = {}
        cities[destination]["arrival_cities"] = set()
        cities[destination]["monthly_arrivals"] = [0 for _ in range(12)]
    cities[destination]["arrival_cities"].add(departure)
    cities[destination]["monthly_arrivals"][month] += 1

def getMonthlyArrivals(city):
    return cities[city]["monthly_arrivals"]

def getDepartureCitiesToCity(city):
    return cities[city]["arrival_cities"]

def getTotalFlightsBetween(startDay, startMonth, startYear, endDay, endMonth, endYear):
    count = 0
    for flight in flights.values():
        date = flight["date"].split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])

        flightDate = year * 10000 + month * 100 + day
        startDate = startYear * 10000 + startMonth * 100 + startDay
        endDate = endYear * 10000 + endMonth * 100 + endDay

        if startDate <= flightDate <= endDate:
            count += 1
    return count

startTime = time.time()
parseCSV("C:\\Users\\SmokeyBBQ\\Desktop\\assignment4\\assignment4\\flight_list.csv")
endTime = time.time()
print("Importing finished in %s seconds" % (endTime - startTime))

startTime = endTime
monthlyArrivals = getMonthlyArrivals("Copenhagen")
endTime = time.time()
print("getMonthlyArrivals took %s seconds" % (endTime - startTime))

startTime = endTime
departureCities = getDepartureCitiesToCity("Ibiza")
endTime = time.time()
print("getDepartureCitiesToCity took %s seconds" % (endTime - startTime))

startTime = endTime
totalFlights = getTotalFlightsBetween(20, 3, 2022, 21, 6, 2022)
endTime = time.time()
print("getTotalFlightsBetween took %s seconds" % (endTime - startTime))

