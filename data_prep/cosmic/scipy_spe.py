#!python numbers=disabled
# read_spe.py
import numpy as N

class File(object):

    def __init__(self, fname):
        self._fid = open(fname, 'rb')
        self._load_size()

    def _load_size(self):
        self._xdim = N.int64(self.read_at(42, 1, N.int16)[0])
        self._ydim = N.int64(self.read_at(656, 1, N.int16)[0])
        self.frame = N.int64(self.read_at(1446, 1, N.int16)[0])

    def _load_date_time(self):
        rawdate = self.read_at(20, 9, N.int8)
        rawtime = self.read_at(172, 6, N.int8)
        strdate = ''
        for ch in rawdate :
            strdate += chr(ch)
        for ch in rawtime:
            strdate += chr(ch)
        self._date_time = time.strptime(strdate,"%d%b%Y%H%M%S")

    def get_size(self):
        return (self._xdim, self._ydim)

    def read_at(self, pos, size, ntype):
        self._fid.seek(pos)
        return N.fromfile(self._fid, ntype, size)

    def load_img(self):
        img = self.read_at(4100, self._xdim * self._ydim * self.frame, N.uint16)
        return img.reshape((self.frame, self._xdim, self._ydim))

    def close(self):
        self._fid.close()

def load(fname):
    fid = File(fname)
    img = fid.load_img()
    fid.close()
    return img

if __name__ == "__main__":
    import sys
    img = load(sys.argv[-1])
