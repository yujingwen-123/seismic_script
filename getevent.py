import os
import obspy
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import math
import seispy
from seispy.decon import RFTrace
import os

client = Client("IRIS",timeout = 120)
start_time = UTCDateTime("2003-12-01T00:00:00")
end_time = UTCDateTime("2004-06-30T23:59:59")
minmagnitude = 4

min_distance = 5
max_distance = 15


network_list=[]
stnm_list=[]
stla_list=[]
stlo_list=[]
stel_list=[]
sttm_list=[]
endtm_list=[]
with open('./gmap-stations.txt') as f:
     headers = f.readline().strip().split('|')
     for line in f:
         parts = line.strip().split('|')
         network_list.append(parts[0])
         stnm_list.append(parts[1])
         stlo_list.append(float(parts[3]))
         stla_list.append(float(parts[2]))
         sttm_list.append(parts[6])
         endtm_list.append(parts[7])
         stel_list.append(float(parts[4]))
for network, stnm, stlo, stla, stel, sttm, endtm in zip(network_list,stnm_list,stlo_list,stla_list,stel_list,sttm_list,endtm_list):
    latitude= stla
    longitude=stlo
    stnm=stnm
#    start_time = UTCDateTime(sttm)
#    end_time = UTCDateTime(endtm)
    try:
        catalog = client.get_events(starttime=start_time, endtime=end_time,
                                    latitude=latitude, longitude=longitude,
                                    minmagnitude=minmagnitude)

    except Exception as e:
        print(e)

    #catalog=obspy.read_events(f'./{stnm}.xml')



    #catalog.write(f"{stnm}.xml", format="QUAKEML")

    filtered_events_P = []
    for event in catalog:
        event_lat = event.preferred_origin().latitude
        event_lon = event.preferred_origin().longitude
        da = seispy.distaz(latitude, longitude, event_lat, event_lon)
        distance = da.delta
        setattr(event,'distance',distance)
        if min_distance <= event.distance  <= max_distance:
           filtered_events_P.append(event)

    for event in filtered_events_P:
        origin = event.preferred_origin()
        event_time = origin.time
        magnitude = event.preferred_magnitude().mag
        event_lat = origin.latitude
        event_lon = origin.longitude
        evdep = origin.depth
        da = seispy.distaz(latitude, longitude, event_lat, event_lon)
        distance = da.delta
        print(f"Event Time: {event_time} | Magnitude: {magnitude} | Location: {event_lat}, {event_lon} | Epicentral Distance: {distance}" )



    with open(f"even{stnm}.txt", "w") as f:
         f.write("Event ID\tnetwork\tstation\tstarttime\tendtime\tMag\tlont\tlat\tdistance\n")
         for event in filtered_events_P:
             origin = event.preferred_origin()
             starttime = origin.time
             endtime = starttime + 120
             magnitude = event.preferred_magnitude().mag
             event_lat = origin.latitude
             event_lon = origin.longitude
             distance = event.distance
             evdep = origin.depth
             event_id = event.resource_id.id
             f.write(f"{event_id}\t{network}\t{stnm}\t{starttime}\t{endtime}\t{magnitude}\t{event_lon}\t{event_lat}\t{distance}\t{evdep}\n")
