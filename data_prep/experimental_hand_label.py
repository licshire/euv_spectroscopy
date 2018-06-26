import os
import sys
from datetime import datetime
from shutil import copyfile

from collections import namedtuple

from prep_utils import *

EXP_BASE = '../data/experimental'

Label = namedtuple('Label', ['eid', 'foname', 'finame', 'element',\
        'energy', 'current', 'collectiontime', 'frames', 'cooktime', 'date'])

def getnumber(label):
    try:
        num = float(input(label+': '))
        return num
    except:
        return np.nan

def getstring(label):
    strin = input(label+': ')
    if strin == '':
        return np.nan
    else:
        return strin

def inputLabels(foldername, filename, cdate):

    eid = getnumber('eID')
    foname = foldername
    finame = filename
    element = getstring('element')
    energy = getnumber('energy')
    current = getnumber('current')
    collectiontime = getnumber('collection time')
    frames = getnumber('frames')
    cooktime = getnumber('cooktime')
    date = cdate
    
    return Label(eid, foname, finame, element, energy,\
            current, collectiontime, frames, cooktime, date)


folder_nms = []
for filepath in os.walk(EXP_BASE):
    folder_nms.append(filepath[0])
folder_nms = folder_nms[1:]

x = 1
for folder in folder_nms:
    folder_name = folder.split('/')[-1]
    dbname = 'spectrabase_' + folder_name + '.csv'
    dbase = SpectraBase(dbname)
    outfolder = '../data/experimental_labeled/'+folder_name
    try:
        os.mkdir(outfolder)
    except:
        pass

    for file_name in os.listdir(folder):
        date = datetime.fromtimestamp(os.path.getmtime(folder+'/'+file_name)).strftime('%Y-%m-%d')
        if '.SPE' in file_name:
            print('({}%) {}'.format(round(x/3203*100, 2), file_name))
            labs = inputLabels(folder_name, file_name, date)
            x += 1
            spectra = load_with_cosmic_applied(folder+'/'+file_name)
            dbase.addRow(spectra, *labs)
            newfilename = 'id{}_el{}_en{}_cu{}_cl{}_fr{}_ck{}_dt{}.SPE'.format(labs.eid, labs.element, labs.energy,\
                    labs.current, labs.collectiontime, labs.frames, labs.cooktime, labs.date)

            copyfile(folder+'/'+file_name, outfolder+'/'+newfilename)
    dbase.save(dbname)












