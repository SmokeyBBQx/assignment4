import time
import os

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

    def getTotalFlightsBetween(self, startYear, startMonth, startDay, endYear, endMonth, endDay):
        startTime = time.time()

        count = 0
        for flight in self.__flights.values():
            if not "date" in flight:
                return
            
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
    
    def getFlights(self):
        return self.__flights

flightData = FlightData("flight_list.csv")

monthlyArrivals = flightData.getMonthlyArrivals("Copenhagen")
departureCities = flightData.getDepartureCitiesToDestination("Ibiza")
totalFlights = flightData.getTotalFlightsBetween(2022, 3, 20, 2022, 6, 21)

print(f"Monthly Arrivals to Copenhagen: {monthlyArrivals}")
print(f"Departure Cities to Ibiza: {departureCities}")
print(f"Total Flights in Spring 2022: {totalFlights}")

def createTestCSV(fileName, content):
    with open(fileName, 'w') as f:
        f.write(content)

def cleanup(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)

def compare(name, expected, outcome):
    result = expected == outcome
    print(f"{name}: Expected {expected}, Got {outcome}, Pass: {result}")
    return result

def runTest(testName, input, comparisons):
    print(f"\n== Running {testName} ==")
    testFile = "test.csv"
    createTestCSV(testFile, input)
    flightData = FlightData(testFile)
    cleanup(testFile)

    print("== Output ==")
    results = []
    for description, actual, expected in comparisons(flightData):
        results.append(compare(description, expected, actual))
    result = all(results)

    print("== Result ==")
    if result == True:
        print(f"{testName}: PASS")
    else:
        print(f"{testName}: FAIL")

# == General Tests ==

runTest(
    "Control Case 1: Basic functionality test with 2 flights",
    """flight_id,name_adep,name_ades,date
    0,Paris,London,2022-03-15
    1,Berlin,Paris,2022-04-20""",
    lambda fd: [
        ("Arrivals in March", fd.getMonthlyArrivals("London")[2], 1),
        ("Departure Cities to Paris", fd.getDepartureCitiesToDestination("Paris"), {"Berlin"}),
        ("Total Flights in 2022", fd.getTotalFlightsBetween(2022, 1, 1, 2022, 12, 31), 2)
    ]
)

runTest(
    "Control Case 2: Test with multiple flights to same destination",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-06-15
    1,Madrid,Berlin,2022-06-20
    2,Paris,Berlin,2022-04-15""",
    lambda fd: [
        ("June arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[5], 2),
        ("Departure Cities to Berlin", fd.getDepartureCitiesToDestination("Berlin"), {"Paris", "Madrid"}),
        ("Total Flights in June", fd.getTotalFlightsBetween(2022, 6, 1, 2022, 6, 30), 2)
    ]
)

runTest(
    "Control Case 3: Test with dates across years",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-04-15
    1,Madrid,Berlin,2020-06-20
    2,Paris,Berlin,2021-04-15""",
    lambda fd: [
        ("April arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[3], 2),
        ("Total Flights From 2020-1-1 to 2021-12-31", fd.getTotalFlightsBetween(2020, 1, 1, 2021, 12, 31), 2),
        ("Total Flights", fd.getTotalFlightsBetween(2020, 1, 1, 2022, 12, 31), 3)
    ]
)

runTest(
    "Edge Case 1: Empty Data",
    "flight_id,date,callsign,adep,name_adep,country_code_adep,ades,name_ades,country_code_ades,actual_offblock_time,arrival_time,aircraft_type,wtc,airline,flight_duration,taxiout_time,flown_distance,tow,",
    lambda fd: [
        ("April arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[3], 0),
        ("Total Flights", fd.getTotalFlightsBetween(2022, 1, 1, 2022, 12, 31), 0)
    ]
)

runTest(
    "Edge Case 2: Single Flight",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-04-15""",
    lambda fd: [
        ("April arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[3], 1),
        ("Departure Cities to Berlin", fd.getDepartureCitiesToDestination("Berlin"), {"Paris"}),
        ("Total Flights", fd.getTotalFlightsBetween(2022, 1, 1, 2022, 12, 31), 1)
    ]
)

runTest(
    "Edge Case 3: Same Departure, Same Destination",
    """flight_id,name_adep,name_ades,date
    0,Berlin,Berlin,2022-04-15""",
    lambda fd: [
        ("April arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[3], 1),
        ("Departure Cities to Berlin", fd.getDepartureCitiesToDestination("Berlin"), {"Berlin"}),
        ("Total Flights", fd.getTotalFlightsBetween(2022, 1, 1, 2022, 12, 31), 1)
    ]
)

runTest(
    "Structural Case 1: Only Flight IDs",
    """flight_id
    0
    1
    2""",
     lambda fd: [
        ("Total Flights", len(fd.getFlights()), 3)
    ]
)

runTest(
    "Structural Case 2: Extra Field",
    """flight_id,name_adep,name_ades,date,extra
    0,Paris,Berlin,2022-06-15,x
    1,Madrid,Berlin,2022-06-20,x
    2,Paris,Berlin,2022-04-15,x""",
    lambda fd: [
        ("June arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[5], 2),
        ("Departure Cities to Berlin", fd.getDepartureCitiesToDestination("Berlin"), {"Paris", "Madrid"}),
        ("Total Flights in June", fd.getTotalFlightsBetween(2022, 6, 1, 2022, 6, 30), 2)
    ]
)

# == getTotalFlightsBetween() tests ==

runTest(
    "Same Date",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-06-15
    1,Madrid,Berlin,2022-06-20
    2,Paris,Berlin,2022-04-15""",
    lambda fd: [
        ("Total Flights on Same Day", fd.getTotalFlightsBetween(2022, 4, 15, 2022, 4, 15), 1)
    ]
)

runTest(
    "Out of Range Date",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-06-15
    1,Madrid,Berlin,2022-06-20
    2,Paris,Berlin,2022-04-15""",
    lambda fd: [
        ("Total Flights in 2021", fd.getTotalFlightsBetween(2021, 6, 1, 2021, 6, 30), 0)
    ]
)

runTest(
    "All 0s Date",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-06-15
    1,Madrid,Berlin,2022-06-20
    2,Paris,Berlin,2022-04-15""",
    lambda fd: [
        ("Total Flights in 2021", fd.getTotalFlightsBetween(0, 0, 0, 0, 0, 0), 0)
    ]
)

