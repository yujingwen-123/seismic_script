from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import os
import obspy
from obspy.core import UTCDateTime
import glob
#from glob import glob
from obspy import read, Stream, read_events, UTCDateTime as UTC
from obspy.core.event.catalog import read_events
from obspy.geodetics.base import locations2degrees, gps2dist_azimuth
from obspy.geodetics import kilometer2degrees
from obspy.taup import TauPyModel
client = Client("IRIS")

basepath='/home/host/yujingwen/tarim/atdata/'


network_list=[]
stnm_list=[]
stla_list=[]
stlo_list=[]
stel_list=[]
sttm_list=[]
endtm_list=[]
with open('./gmap-stations.txt') as f: #"gmap-stations got from IRIS https://ds.iris.edu/gmap/ "
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
    st_list=[]
    path=f'./ev/even{stnm}.txt'
    with open(path, "r") as f:

         fevn = f.readlines()
         fevn = fevn[1:]

    for i in fevn:
        t = i.split()
        date = t[4]
        lon = float(t[6])
        lat = float(t[7])
        mag = float(t[5])
        depth = float(t[-1])
        da = UTCDateTime(date)
        dis = float(t[-2])
        print(network,stnm,da)
        try:
            st = client.get_waveforms(network=f'{network}',
                                     station=f'{stnm}',
                                     location='01',
                                     channel='BH?',
                                     starttime = da,
                                     endtime = da + 600)
            for i in st:
                st_list.append(i)
                i.stats.sac= {}
                i.stats.sac.stla=stla
                i.stats.sac.stlo=stlo
                i.stats.sac.gcarc=dis
                i.stats.sac.evdp=depth
                i.stats.sac.evla=lat
                i.stats.sac.evlo=lon
                i.stats.sac.stel=stel
                path_sta = f'/home/host/yujingwen/tarim/atdata/{stnm}'
                os.makedirs(path_sta, exist_ok=True)


                output_filename = f"{i.stats.network}.{stnm}.{i.stats.location}.{i.stats.channel}.{i.stats.starttime}.sac"
                output_filepath = os.path.join(path_sta, output_filename)
                i.write(output_filepath, format='sac')

              #  print(i.stats)
        except Exception:
            pass






            
