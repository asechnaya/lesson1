import csv
with open('data-397-2018-03-02.csv', 'r', encoding='UTF-8') as f:
    #fields = ['ID', 'Name', 'Longitude_WGS84', 'Latitude_WGS84', 'Street', 'AdmArea']
    fields = ['ID','Name','Longitude_WGS84','Latitude_WGS84','NameOfStation','Line','ModeOnEvenDays','ModeOnOddDays','FullFeaturedBPAAmount','LittleFunctionalBPAAmount','BPAAmount','RepairOfEscalators','global_id','geoData']
    reader = csv.DictReader(f, fields, delimiter=',')
    new_st = set()

    for row in reader: 
        esk = row['RepairOfEscalators']
        #print(street)
        if (esk != ""):
            new_st.add(row['NameOfStation'])
    print(new_st)