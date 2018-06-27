import numpy as np
import pandas as pd


class File(object):

    def __init__(self, fname):
        self._fid = open(fname, 'rb')
        self._load_size()

    def _load_size(self):
        self._xdim = np.int64(self.read_at(42, 1, np.int16)[0])
        self._ydim = np.int64(self.read_at(656, 1, np.int16)[0])
        self.frame = np.int64(self.read_at(1446, 1, np.int16)[0])

    def _load_date_time(self):
        rawdate = self.read_at(20, 9, np.int8)
        rawtime = self.read_at(172, 6, np.int8)
        strdate = ''
        for ch in rawdate:
            strdate += chr(ch)
        for ch in rawtime:
            strdate += chr(ch)
        self._date_time = time.strptime(strdate, "%d%b%Y%H%M%S")

    def get_size(self):
        return (self._xdim, self._ydim)

    def read_at(self, pos, size, ntype):
        self._fid.seek(pos)
        return np.fromfile(self._fid, ntype, size)

    def load_img(self):
        img = self.read_at(4100, self._xdim * self._ydim * self.frame, np.uint16)
        return img.reshape((self.frame, self._xdim, self._ydim))

    def close(self):
        self._fid.close()


def load(fname):
    fid = File(fname)
    img = fid.load_img()
    fid.close()
    return img


def load_with_cosmic_applied(filename):
    arr = load(filename)
    arr.shape  # (15, 2048, 1)
    arr = arr.reshape(arr.shape[:-1]).T

    # Using for loop beacause I couldn't figure out a way to do this vectorized

    for i, line in enumerate(arr):
        std = np.std(line)
        avg = np.average(line)
        lineshape = line.shape[0]
        line = line - avg
        line = line[line > -std * 3]
        line = line[line < std * 3]
        line = line + avg

        lineshape = lineshape - line.shape[0]
        arr[i] = line.sum() + np.average(line) * lineshape

    arr = np.average(arr, axis=1)
    return arr


class SpectraBase:

    def __init__(self, dbase_name):
        self.df = self.load(dbase_name)
        self.db_name = dbase_name

    def load(self, dbase_name):

        try:
            df = pd.read_csv(dbase_name, delimiter=',')
            print('{} loaded'.format(dbase_name))
        except:
            print('{} created'.format(dbase_name))
            expdict = {x + 1: [] for x in range(2048)}
            expdict['FolderName'] = []
            expdict['FileName'] = []
            expdict['Element'] = []
            expdict['Energy'] = []
            expdict['Current'] = []
            expdict['Date'] = []
            expdict['Note'] = []
            expdict['Calibration1'] = []
            expdict['Calibration2'] = []
            expdict['Calibration3'] = []
            expdict['Calibration4'] = []
            df = pd.DataFrame(expdict)

        return df

    def save(self, dbase_name):

        self.df.to_csv(dbase_name)

    def addRow(self, spec, foname=np.nan, finame=np.nan, element=np.nan,
               energy=np.nan, current=np.nan,
               date=np.nan, note=np.nan, calibration1=np.nan, calibration2=np.nan,
               calibration3=np.nan, calibration4=np.nan):
        # Function to add spectrum to DataFrame
        row = np.append(spec, [foname, finame, element, energy, current,
                               date, note, calibration1, calibration2, calibration3, calibration4])
        self.df.loc[len(self.df)] = row
