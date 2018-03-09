import csv
with open('data-398-2018-03-07.csv', 'r', encoding='PT154') as f:
    #fields = ['ID', 'Name', 'Longitude_WGS84', 'Latitude_WGS84', 'Street', 'AdmArea']
    fields = ['ID','Name','Longitude_WGS84','Latitude_WGS84','Street','AdmArea','District','RouteNumbers','StationName','Direction','Pavilion','OperatingOrgName','EntryState','global_id','geoData']
    reader = csv.DictReader(f, fields, delimiter=';')
    b_stops = {}
    new_st = {}
    col = 0
    for row in reader: 
        street = row['Street']
        if street in new_st:
            new_st[street] += 1
        else:
            new_st[street] = 1
    sorted_x = sorted(new_st.items(), key=lambda item: item[1])
        #b_stops.append(Street['Street'])
    print(sorted_x[-1][0])