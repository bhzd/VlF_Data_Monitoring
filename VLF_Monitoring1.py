import gzip, os, glob
import io
import pandas as pd
from matplotlib import pyplot as plt
import datetime
import schedule
import time
import requests
import urllib.request
import urllib
from urllib.request import urlretrieve

def job():
    print("Data Processing ...", )


    now = datetime.datetime.now()

    y = str (now.year)
    m = str (now.month)
    d = str (now.day)
    if now.month < 10:
        m = str("0" + m)
    if now.day < 10:
        d = str("0" + d)

    url = "http://172.16.180.55/cgi-bin/data_download.cgi?download=Elettronika-" + y + "_" + m + "_" + d + ".txt"
    path_downlad = "/home/pish-behzad/Maleki/pishneshangar/VLF/Online1/Elettronika-"+ y + "_" + m + "_" + d + ".txt.gz"
    print('Geting files from Elettronika device ...')
    urllib.request.urlretrieve(url, path_downlad)

    with gzip.open(path_downlad, 'rb') as f, open("Elettronika-"+ y + "_" + m + "_" + d  + "_unzip" , 'wb') as t:
        file_content = f.read()
        t.write(file_content)

    path_text_file = "/home/pish-behzad/Maleki/pishneshangar/VLF/Online1/Elettronika-"+ y + "_" + m + "_" + d + "_unzip"

    firstHeader = True

        
    stream = open ("bbbb", "w+")
        
    with open (path_text_file, "r") as file:
            
        #file = open(path_text_file, "r")
        for line in file:
            if len(line) < 10:   continue
            if 'dBmVpp' in line: continue
            if 'error'  in line: line = line[:8]
            if 'Hz'     in line:
                if firstHeader: firstHeader = False
                else:           continue
            if 'Log'    in line:
                prefix = line[len("Log file for the day "):].strip()
                continue
            stream.write(prefix+' '+line.strip()+"\n")
        stream.seek(0)
        data = pd.read_csv(stream, sep='\t', index_col=0, header=0)
        data.index = pd.to_datetime(data.index)
        idx = pd.date_range(start=min(data.index), end=max(data.index), freq='t')
        data = data.reindex(idx, fill_value=None)

        fig = plt.figure(figsize=(18,9))
        ax  = fig.gca()
        ax.plot(data)
        ax.legend(data.columns)
        ax.set_xlabel("Time")
        ax.set_ylabel("dBmVpp")
        fig.suptitle("Very Low Frequency (VLF) monitoring system for characterizing low layer ionosphere", fontsize=22)
        plt.savefig(path_text_file, format='png', dpi=100)
        plt.close()
        print('Ploting VLF data ...')
        return

    os.remove("bbbb")
    del stream
    del data
    del idx
    del firstHeader
    del path_downlad
    del url
    del path_text_file
    del now
    del y
    del m
    del d
    del file_content
    del data.index


if __name__ == '__main__':
    while True:
        job()
        time.sleep(900)
