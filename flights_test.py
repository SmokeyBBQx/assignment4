import flights
import os

flightData = flights.FlightData("flight_list.csv")

monthlyArrivals = flightData.getMonthlyArrivals("Copenhagen")
departureCities = flightData.getDepartureCitiesToDestination("Ibiza")
totalFlights = flightData.getTotalFlightsBetween((2022, 3, 20), (2022, 6, 21))

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
    flightData = flights.FlightData(testFile)
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
        ("Total Flights in 2022", fd.getTotalFlightsBetween((2022, 1, 1), (2022, 12, 31)), 2)
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
        ("Total Flights in June", fd.getTotalFlightsBetween((2022, 6, 1), (2022, 6, 30)), 2)
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
        ("Total Flights From 2020-1-1 to 2021-12-31", fd.getTotalFlightsBetween((2020, 1, 1), (2021, 12, 31)), 2),
        ("Total Flights", fd.getTotalFlightsBetween((2020, 1, 1), (2022, 12, 31)), 3)
    ]
)

runTest(
    "Edge Case 1: Empty Data",
    "flight_id,date,callsign,adep,name_adep,country_code_adep,ades,name_ades,country_code_ades,actual_offblock_time,arrival_time,aircraft_type,wtc,airline,flight_duration,taxiout_time,flown_distance,tow,",
    lambda fd: [
        ("April arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[3], 0),
        ("Total Flights", fd.getTotalFlightsBetween((2022, 1, 1), (2022, 12, 31)), 0)
    ]
)

runTest(
    "Edge Case 2: Single Flight",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-04-15""",
    lambda fd: [
        ("April arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[3], 1),
        ("Departure Cities to Berlin", fd.getDepartureCitiesToDestination("Berlin"), {"Paris"}),
        ("Total Flights", fd.getTotalFlightsBetween((2022, 1, 1), (2022, 12, 31)), 1)
    ]
)

runTest(
    "Edge Case 3: Same Departure, Same Destination",
    """flight_id,name_adep,name_ades,date
    0,Berlin,Berlin,2022-04-15""",
    lambda fd: [
        ("April arrivals to Berlin", fd.getMonthlyArrivals("Berlin")[3], 1),
        ("Departure Cities to Berlin", fd.getDepartureCitiesToDestination("Berlin"), {"Berlin"}),
        ("Total Flights", fd.getTotalFlightsBetween((2022, 1, 1), (2022, 12, 31)), 1)
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
        ("Total Flights in June", fd.getTotalFlightsBetween((2022, 6, 1), (2022, 6, 30)), 2)
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
        ("Total Flights on Same Day", fd.getTotalFlightsBetween((2022, 4, 15), (2022, 4, 15)), 1)
    ]
)

runTest(
    "Out of Range Date",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-06-15
    1,Madrid,Berlin,2022-06-20
    2,Paris,Berlin,2022-04-15""",
    lambda fd: [
        ("Total Flights in 2021", fd.getTotalFlightsBetween((2021, 6, 1), (2021, 6, 30)), 0)
    ]
)

runTest(
    "All 0s Date",
    """flight_id,name_adep,name_ades,date
    0,Paris,Berlin,2022-06-15
    1,Madrid,Berlin,2022-06-20
    2,Paris,Berlin,2022-04-15""",
    lambda fd: [
        ("Total Flights in 2021", fd.getTotalFlightsBetween((0, 0, 0), (0, 0, 0)), 0)
    ]
)

