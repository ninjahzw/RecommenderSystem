class split:
    
    def __init__(self):
        self.ratio = 0.5
        self.file = "/disk/hou/workspace/RecommenderSystem/librec-1m/result/predicts.BiasedMF/BiasedMF-prediction-movie"

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
        with open(self.file) as f:
            for line in f:
                movieid, userid, origin, predicted = line.split()
                if prev == -1 : prev = movieid
                if prev != movieid:
                    count = counts.pop(0)
                    prev = movieid
                    index = 0
                else:
                    if index < count * self.ratio:
                        print line.strip()
                    index += 1
        print len(counts)

split().split()
