import math, sys
class predict_bias:

    def __init__(self, data):
        self.ItemKNN_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.ItemKNN/ItemKNN-prediction-movie"
        self.Biased_MF_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.BiasedMF/BiasedMF-prediction-movie"
        self.UserKNN_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.UserKNN/UserKNN-prediction-movie"
        self.RegSVD_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.RegSVD/RegSVD-prediction-movie"
        self.BPMF_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.BPMF/BPMF-prediction-movie"

        # number of ratings to remove when appmy Majority avg.
        self.ratings_remove = 2


    def bias(self):
        pre_movie = -1
        original_sum = 0
        predict_sum = 0 
        total = 0
        with open(self.ItemKNN_file) as ikf, open(self.Biased_MF_file) as bmf,\
                open(self.UserKNN_file) as ukf, open(self.RegSVD_file) as rsf,\
                open(self.BPMF_file) as bf:
            for line1, line2, line3, line4, line5 in zip(ikf, bmf, ukf, rsf, bf):
                # the user, movie, and original information are same for two lines.
                movieid, userid, origin_rating, predict1 = line1.split()
                predict2 = line2.split()[-1]
                predict3 = line3.split()[-1]
                predict4 = line4.split()[-1]
                predict5 = line5.split()[-1]
                predict = self.avg(predict1, predict2, predict3, predict4, predict5) 
                if pre_movie == -1: pre_movie = movieid
                if pre_movie != movieid:
                    print pre_movie, original_sum/total, predict_sum/total, predict_sum/total - original_sum/total
                    pre_movie, original_sum, predict_sum, total = movieid,float(origin_rating),predict,1
                    continue
                original_sum += float(origin_rating)
                predict_sum += predict
                total += 1
        print pre_movie, original_sum/total, predict_sum/total, predict_sum/total - original_sum/total

    """
    calculate the overall average, and remove the 2 that are far away from the avg.
    Then make an average again on the left. 
    """
    def maj_avg(self, *args):
        total = 0
        num = 0
        for one in args:
            # print one
            total += float(one)
            num += 1
        avg = total/num
        pairs = []
        for one in args:
            pairs.append([abs(float(one)-avg),float(one)])
        pairs.sort()
        # remove last few elements from dict
        index = 0
        while index < self.ratings_remove:
            pairs.pop()
            index += 1
        total = 0
        for one in pairs:
            total += one[-1]
        # print pairs
        # print total/len(pairs)
        # print '----------'
        return total/len(pairs)
      
    def maj_avg_v3(self, *args):
        threshold = 5
        args = [float(one) for one in args]
        s_args = sorted(args)
        median = self.get_median(s_args)
        start, end = s_args[0], s_args[-1]
        if abs(start - median) > threshold:
            index = 0
            while index < self.ratings_remove:
                s_args.pop(0); index += 1
        if abs(end - median) > threshold:
            index = 0
            while index < self.ratings_remove:
                s_args.pop(-1); index += 1
        # calculate average again
        total = 0
        num = 0
        for one in s_args:
            # print one
            total += float(one)
            num += 1
        avg = total/num
        return avg

    """
    Calculate the overall average, and remove the 2 that are far away from the avg.
    Then make average again to the left 3 and removed 2, assign different weight to 
    the two averages and then do a weighted average.
    
    0.7-0.8 seems better
    """
    def weighted_maj_avg(self, *args):
        weight = 0.3
        total = 0
        num = 0
        for one in args:
            total += float(one)
            num += 1
        avg = total/num
        pairs = []
        for one in args:
            pairs.append([abs(float(one)-avg),float(one)])
        pairs.sort()
        poped = []
        # remove last two elements from dict
        index = 0
        while index < self.ratings_remove:
            poped.append(pairs.pop())
            index += 1
        total = 0
        for one in pairs:
            total += one[-1]

        total_poped = 0
        for one in poped:
            total_poped += one[-1]
        #return weight * self.diagonal()
        return weight * total/len(pairs) + (1-weight) * total_poped/len(poped)
   
    """
    Surprise, got 0.699989449999 0.903466663523 -best by far.
    """
    def diagonal(self, *args):
        total = 0
        for one in args:
            total += float(one)**2
        return math.sqrt(total/5)

    def avg(self, *args):
        total = 0
        for one in args:
            total += float(one)
        return total/len(args)

    """
    For the sorted args, whichever is farther to the mean, 
    remove two from that side. However the result is really poor:
    0.721583216496 0.935032298347
    because we have data like:
    [3.9003487, 3.7182412, 3.8779755, 3.4041383, 4.575588]
    -->  [3.4041383, 3.7182412, 3.8779755]
    which after delete the two, the result is not ideal
    """
    def maj_avg_v2(self, *args):
        args = [float(one) for one in args]
        total = 0
        num = 0
        for one in args:
            # print one
            total += one
            num += 1
        avg = total/num
        s_args = sorted(args)
        start, end = s_args[0], s_args[-1]
        if abs(start - avg) > abs(end - avg):
            index = 0
            while index < self.ratings_remove:
                s_args.pop(0); index += 1
        elif abs(start - avg) < abs(end - avg):
            index = 0
            while index < self.ratings_remove:
                s_args.pop(-1); index += 1
        # calculate average again
        total = 0
        num = 0
        for one in s_args:
            # print one
            total += float(one)
            num += 1
        avg = total/num
        return avg
    
    def get_median(self, a):
        length = len(a)
        if a is None or length == 0:
            return None
        if length % 2 == 0:
            return float(a[length/2] + a[length/2-1])/2.0
        else:
            return a[length/2]



if len(sys.argv) <= 1:
    print "plz input data dir"
    sys.exit()
data = sys.argv[1]
predict_bias(data).bias()
