import pickle

all_speeches = {}

for i in range(106,115):
    speeches = {}

    file_speakermap = open("hein-daily/" + str(i) + "_SpeakerMap.txt", 'r')
    next(file_speakermap)
    for line in file_speakermap.readlines():
        arr = line.split("|")
        speakerID = arr[0]
        speechID = arr[1]
        party = arr[7]
        if party in ('D', 'R'):
            speeches[speechID] = {'party': party, 'speakerID': speakerID}
    file_speakermap.close()

    file_descr = open("hein-daily/descr_" + str(i) + ".txt", 'r')
    next(file_descr)
    for line in file_descr.readlines():
        arr = line.split("|")
        speech_id = arr[0]
        if speech_id in speeches:
            date_string = arr[2]
            year = int(date_string[:4])
            month = int(date_string[4:6])
            day = int(date_string[6:])
            speeches[speech_id]['date'] = {"year": year, "month": month, "day": day}
    file_descr.close()
    
    all_speeches[i] = speeches

pickle.dump(all_speeches, open("speeches.p", "wb"))