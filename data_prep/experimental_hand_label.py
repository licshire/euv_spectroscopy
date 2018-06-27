import os
import sys
from datetime import datetime
from shutil import copyfile

from collections import namedtuple

from prep_utils import *

EXP_BASE = '../data/experimental'

Label = namedtuple('Label', ['foname', 'finame', 'element',
                             'energy', 'current', 'date', 'note'])


def getEnergy(ls):
    for element in ls:
        if 'keV' in element:
            try:
                return float(element[:-3].replace('p', '.')) * 1000
            except:
                return float(input('energy(eV): '))

        if 'eV' in element:
            try:
                return float(element[:-2])
            except:
                return float(input('energy(eV): '))

        if 'KV' in element:
            try:
                return float(element[:-2].replace('p', '.')) * 1000
            except:
                return float(input('energy(eV): '))

    try:
        return float(input('energy(eV): '))
    except:
        return np.nan


def getCurrent(ls):
    for element in ls:
        if 'mA' in element:
            try:
                return float(element[:-2])
            except:
                if 'p' in element:
                    try:
                        return float(element[:-2].replace('p', '.'))
                    except:
                        continue
                else:
                    return float(input('current(mA): '))
    try:
        return float(input('current(mA): '))
    except:
        return np.nan


def findElement(ls):

    element_dict = {'Ar': 18, 'Ne': 10, 'Fe': 26, 'Kr': 36, 'Y': 39, 'Zr': 40, 'Nb': 41, 'Mo': 42,
                    'Xe': 54, 'Ba': 56, 'Sm': 62, 'Gd': 64, 'Dy': 66, 'Er': 68, 'Yb': 70, 'W': 74, 'Pt': 78, 'Bi': 83}

    for element in ls:
        if element in list(element_dict.keys()):
            return element_dict[element]

    return 0


def inputLabels(foldername, filename, cdate, fn):

    fn = fn.split('_')
    foname = foldername
    finame = filename
    element = findElement(fn)
    energy = getEnergy(fn)
    current = getCurrent(fn)
    date = cdate
    print(element, energy, current)
    note = ''

    return Label(foname, finame, element, energy,
                 current, date, note)


folder_nms = []
for filepath in os.walk(EXP_BASE):
    folder_nms.append(filepath[0])
folder_nms = folder_nms[1:]

x = 1
for folder in folder_nms:

    folder_name = folder.split('/')[-1]

    dbname = 'spectrabase_' + folder_name + '.csv'
    dbase = SpectraBase(dbname)

    outfolder = '../data/experimental_labeled/' + folder_name

    try:
        os.mkdir(outfolder)
    except:
        pass
    y = 1
    for file_name in os.listdir(folder):
        date = datetime.fromtimestamp(os.path.getmtime(folder + '/' + file_name)).strftime('%m-%d-%Y')
        if '.SPE' in file_name:
            try:
                spectra = load_with_cosmic_applied(folder + '/' + file_name)
            except:
                continue
            print('{} ({} %)'.format(file_name, round(x / 3203 * 100, 2)))
            labs = inputLabels(folder_name, file_name, date, file_name)
            dbase.addRow(spectra, *labs)
            newfilename = '{}_{}_{}eV_{}mA_{}.SPE'.format(y, labs.element, labs.energy,
                                                          labs.current, labs.date)

            copyfile(folder + '/' + file_name, outfolder + '/' + newfilename)
            x += 1
            y += 1

    dbase.save(dbname)
