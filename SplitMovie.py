class split:
    
    def __init__(self, file):
        # ratio should less than or equal to 0.5, otherwise it's meaningless
        self.ratio = 0.5
        self.file = file

    def split(self):
        prev = -1
        count = 0
        counts = []
        with open(self.file) as f:
            for line in f:
                movieid, userid, origin, predicted = line.split()
                if prev == -1 : prev = movieid
                if prev != movieid:
                    counts.append(count)
                    prev = movieid
                    count = 0
                count += 1 
            counts.append(count)
        count = counts.pop(0)
        index = 0
        prev = -1
        # split to two parts by the ratio, and write each to new file 
        part1 = open(self.file + "part1",'w')
        part2 = open(self.file + "part2",'w')
        with open(self.file) as f:
            for line in f:
                movieid, userid, origin, predicted = line.split()
                if prev == -1 : prev = movieid
                if prev != movieid:
                    count = counts.pop(0)
                    prev = movieid
                    index = 0
                    part1.write(line)
                else:
                    if index < count * self.ratio:
                        # need not to do strip here, because new fine need \n.
                        part1.write(line)
                    else:
                        part2.write(line)
                    index += 1
        print len(counts)

split("librec-1m/result/predicts.BiasedMF/BiasedMF-prediction-movie").split()
split("librec-1m/result/predicts.RegSVD/RegSVD-prediction-movie").split()
split("librec-1m/result/predicts.BPMF/BPMF-prediction-movie").split()
split("librec-1m/result/predicts.ItemKNN/ItemKNN-prediction-movie").split()
split("librec-1m/result/predicts.UserKNN/UserKNN-prediction-movie").split()
