flights = {}
monthToFlights = [[] for _ in range(12)]
dateToFlights = {}
monthlyArrivals = {}

def parseCSV(loc: str):
    with open(loc) as reader:
        header = next(reader).strip().split(",")
        for line in reader:
            fields = line.strip().split(",")
            flights[fields[0]] = {}
            for i in range(1, len(fields) - 1):
                flights[fields[0]][header[i]] = fields[i]
            
            dest = fields[7]
            month = fields[1].split("-")[1]
            if dest not in monthlyArrivals:
                monthlyArrivals[dest] = []
                monthlyArrivals[dest][month] = 0
            monthlyArrivals[dest][month] += 1

            addDate(fields[1], fields[0])

def addDate(date, flight):
    year = date[0]
    month = int(date[1])
    day = int(date[2])
    if year not in dateToFlights:
        dateToFlights[year] = [[[] for _ in range(31)] for _ in range(12)]
    dateToFlights[year][month][day].append(flight)

def getMonthlyArrivalsAlt(city):
    counts = [0] * 12
    for i in range(0, 12):
        for id in monthToFlights[i]:
            if flights[id]["name_ades"] == city:
                counts[i] += 1
    return counts

def getMonthlyArrivals(city):
    counts = [0] * 12
    for year in dateToFlights.values():
        for month in range(0, 12):
            for day in year[month]:
                for flight in day:
                    if flights[flight]["name_ades"] == city:
                        counts[month] += 1
    return counts
    
def getDepartureCitiesToCity(city):
    cities = set()
    for flight in flights.values():
        if flight["name_ades"] == city:
            cities.add(flight["name_adep"])
    return cities

def getFlightsBetween(startDay, startMonth, startYear, endDay, endMonth, endYear):
    count = 0
    for i in range(startMonth, endMonth):
        for id in monthToFlights[i]:
            date = flights[id]["date"].split("-")
            day = int(date[2])
            year = int(date[0])
            if day >= startDay and day <= endDay and year >= startYear and year <= endYear:
                count += 1
    return count

parseCSV("C:\\Users\\phili\\Desktop\\flight_list.csv")
print(getMonthlyArrivals("Copenhagen"))
print(getDepartureCitiesToCity("Ibiza"))
print(getFlightsBetween(20, 3, 2022, 21, 6, 2022))
print(monthlyArrivals["Copenhagen"])
