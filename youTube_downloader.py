from pytube import YouTube
from pytube import Playlist
import pandas as pd
import os
import glob


def playlist(url,parth):
    pl = Playlist(url)
    pl.download_all(parth)

def youTube_dowloader(url,parth):
    yt = YouTube(url)
    #stream = yt.streams.first()
    #stream.download(parth)
    #yt = yt.get('mp4', '720p')
    #yt.download(parth+"/"+str(yt.title))
    #+"/" + str(yt.title)
    #print(yt.title)
    #p=glob.glob(parth+"/"+str(yt.title)+".*")
    #print(p)
    #if len(p)==0:
    #    print(yt.title)
    YouTube(url).streams.first().download(parth)


def excal_read(parth= '/home/peter/Documents/IISP/youtube_cctv_data'):
    file_name = parth+"/"+'YouTube-Playlist_update.xlsx'#"YouTube-Playlist_csv.csv" # path to file + file name
    #sheet = 0 # sheet name or sheet number or list of sheet numbers and names

    df = pd.read_excel(file_name)
    #df = pd.read_html(file_name)
    #df=pd.read_csv(file_name)#,sep='delimiter')#header=None#error_bad_lines=False)
    #dft = pd.DataFrame(df, columns= ['Video URL'])
    dft=df['Unnamed: 1']#'Video URL']
    #print(dft)  # print first 5 rows of the dataframe
    print(len(dft)-1)
    dft=list(dft)
    dft=dft[1:]#remove the title
    #print(df.columns)
    return dft


if __name__ == '__main__':#
    url1='https://www.youtube.com/watch?v=PmO6ehLAeCM&list=PL4uBjNm43dQAmpCgL6Z-TBqSlqzt_J62-&index=5&t=0s'#"https://www.youtube.com/watch?v=n06H7OcPd-g"
    play_url='https://www.youtube.com/playlist?list=PL4uBjNm43dQAmpCgL6Z-TBqSlqzt_J62-'
    parth = '/home/peter/Documents/IISP/youtube_cctv_data'
    dft = excal_read()
    t=0
    h=0
    error=[]
    for url in dft:
        print(str(t)+"/"+str(len(dft))+" ("+str(len(dft)-h)+" left to run)")
        try:
            youTube_dowloader(url,parth)
        except:
            print(url)
            print("did not load")
            t = t - 1
            error.append(url)
        t=t+1
        h=h+1
    #playlist(play_url, parth)
    print("Errors :")
    for e in error:
        print(e)
    print("there are "+str(len(error))+" to be removed")
    print("but we have " + str(t) + " number of load vidios")
