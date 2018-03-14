import csv
import math


def coord(lat1, lat2, lon1, lon2):
    d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2))
    L = d * 6371  # средний радиус земного шара.
    return L

#задаем начальные значения долготы и широты
class GeoPoint(object):
    def __init__(self):
        self.latitude = -1.0
        self.longitude = -1.0

# в этом классе хранятся координаты
class GeoObject(object):
    def __init__(self):
        self.name = ''   #имя остановки или станции
        self.listOfPoint = []  #

    """docstring for GeoObject"""

    def addPoint(self, lat, lon):
        p = GeoPoint()
        p.latitude = float(lat)
        p.longitude = float(lon)
        self.listOfPoint.append(p) # добавляет точки к объекту ГеоОбджект

    """ здесь вычисляется, если расстояние меньше 0.5 км, то берем в расчет"""
    def is_dist(self, other):
        for first in self.listOfPoint:
            for second in other.listOfPoint:
                if (coord(first.latitude, second.latitude, first.longitude, second.longitude) <= 0.5):
                    return True
        return False


# как перевести класс в строку   repr_


busStationList = []
metroStationList = []
metroBusStationNumber = {}

with open('data-397-2018-03-02.csv', 'r', encoding='UTF-8') as f:
    fields = ['ID', 'Name', 'Longitude_WGS84', 'Latitude_WGS84', 'NameOfStation', 'Line', 'ModeOnEvenDays',
              'ModeOnOddDays', 'FullFeaturedBPAAmount', 'LittleFunctionalBPAAmount', 'BPAAmount', 'RepairOfEscalators',
              'global_id', 'geoData']
    metroreader = csv.DictReader(f, delimiter=',')
    for row in metroreader:
        metroStation = GeoObject()
        metroName = row['NameOfStation']
        existedObject = next((x for x in metroStationList if x.name == metroName), None) #проверяет наличие объекта в списке
        # print(existedObject)
        if (existedObject != None):
            existedObject.addPoint(row['Latitude_WGS84'], row['Longitude_WGS84'])

        else:
            newObj = GeoObject()
            newObj.name = metroName
            newObj.addPoint(row['Latitude_WGS84'], row['Longitude_WGS84'])
            metroStationList.append(newObj)
    print(metroStationList)

with open('data-398-2018-03-07.csv', 'r', encoding='PT154') as f2:
    fields = ['ID', 'Name', 'Longitude_WGS84', 'Latitude_WGS84', 'Street', 'AdmArea', 'District', 'RouteNumbers',
              'StationName', 'Direction', 'Pavilion', 'OperatingOrgName', 'EntryState', 'global_id', 'geoData']
    busreader = csv.DictReader(f2, delimiter=';')
    i = 0
    for row in busreader:
        busStationName = row['Name']

        busStation = GeoObject()
        existedObject = next((x for x in busStationList if x.name == busStationName), None)
        if (existedObject != None):
            existedObject.addPoint(row['Latitude_WGS84'], row['Longitude_WGS84'])
        else:
            newObj = GeoObject()
            newObj.name = metroName
            newObj.addPoint(row['Latitude_WGS84'], row['Longitude_WGS84'])
            busStationList.append(newObj)

for metroStation in metroStationList:
    for busStation in busStationList:
        if (metroStation.is_dist(busStation)):
            if metroStation.name in metroBusStationNumber:
                metroBusStationNumber[metroStation.name] += 1
            else:
                metroBusStationNumber[metroStation.name] = 1
sorted_x = sorted(metroBusStationNumber.items(), key=lambda item: item[1])
# b_stops.append(Street['Street'])
print(sorted_x)
