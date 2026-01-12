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
                for i in range(1, len(header)):
                    self.__flights[flightId][header[i]] = fields[i]
                
                self.__addCityData__(flightId)
        
        print("Parsing CSV finished in %s seconds" % (time.time() - startTime))
                
    def __addCityData__(self, flightId):
        flight = self.__flights.get(flightId, {})

        required_fields = ["name_ades", "name_adep", "date"]
        if not all(field in flight for field in required_fields):
            return
        
        destination = flight["name_ades"]
        departure = flight["name_adep"]
        month = int(flight["date"].split("-")[1]) - 1

        if destination not in self.__cities:
            self.__cities[destination] = {
                "arrival_cities": set(),
                "monthly_arrivals": [0] * 12
            }

        self.__cities[destination]["arrival_cities"].add(departure)
        self.__cities[destination]["monthly_arrivals"][month] += 1

    def getMonthlyArrivals(self, city):
        startTime = time.time()

        monthlyArrivals = self.__cities.get(city, {}).get("monthly_arrivals", [0 for _ in range(12)])

        print("getMonthlyArrivals took %s seconds" % (time.time() - startTime))

        return monthlyArrivals

    def getDepartureCitiesToDestination(self, city):
        startTime = time.time()

        arrivalCities = self.__cities.get(city, {}).get("arrival_cities", set())

        print("getDepartureCitiesToDestination took %s seconds" % (time.time() - startTime))

        return arrivalCities

    def getTotalFlightsBetween(self, startDate, endDate):
        startTime = time.time()

        count = 0
        for flight in self.__flights.values():
            if not "date" in flight:
                return
            
            date = flight["date"].split("-")
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])

            if startDate <= (year, month, day) <= endDate:
                count += 1

        print("getTotalFlightsBetween took %s seconds" % (time.time() - startTime))

        return count
    
    def getFlights(self):
        return self.__flights
