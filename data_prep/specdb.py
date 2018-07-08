import pandas as pd


class SpecBase(object):
    """docstring for SpecBase"""

    def __init__(self, fname):
        super(SpecBase, self).__init__()

        try:
            self.df = pd.read_csv(fname, delimiter=',')
        except OSError:
            print('{} not found!'.format(fname))
        self.orig_df = self.df

    def getTable(self, max_energy=1000000, min_energy=0, max_current=1000000,
                 min_current=0, element=[], fstring=''):

        q_df = self.df

        # energy and current filter
        que = 'Energy >= {} & Energy <= {} & Current >= {} & Current <= {}'.format(min_energy, max_energy,
                                                                                   min_current, max_current)
        q_df = q_df.query(que)

        # element filter
        if element:
            first = 1
            for a in element:
                if first:
                    element_df = q_df[q_df.Element == a]
                    first = 0
                else:
                    element_df = pd.concat([q_df[q_df.Element == a], element_df], ignore_index=True)
            q_df = element_df

        # filename filter
        if fstring != '':
            q_df = q_df[q_df.FileName.str.contains(fstring)]

        return q_df

    def resetTable(self):
        self.df = self.orig_df

    def __len__(self):
        return len(self.df)


def main():
    sb = SpecBase('specBase.csv')
    print(sb)


if __name__ == '__main__':
    main()
