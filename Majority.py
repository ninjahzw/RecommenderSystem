import math, sys
class hybrid:

    def __init__(self, data):
        suffix = "-movie"
        self.ItemKNN_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.ItemKNN/ItemKNN-prediction" + suffix
        self.Biased_MF_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.BiasedMF/BiasedMF-prediction" + suffix
        self.UserKNN_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.UserKNN/UserKNN-prediction" + suffix
        self.RegSVD_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.RegSVD/RegSVD-prediction" + suffix
        self.BPMF_file = "/disk/hou/workspace/RecommenderSystem/" + data + "/result/predicts.BPMF/BPMF-prediction" + suffix
        self.bias = "predict_bias_1m_full"
        self.bias_map = {}
        with open(self.bias) as f:
            for line in f:
                elements = line.split()
                self.bias_map[elements[0]] = elements[-1]
        # number of ratings to remove when appmy Majority avg.
        self.ratings_remove = 2


    def majority_vote(self):
        total_squired_diff = 0
        total_diff = 0
        total_items = 0
        with open(self.ItemKNN_file) as ikf, open(self.Biased_MF_file) as bmf,\
                open(self.UserKNN_file) as ukf, open(self.RegSVD_file) as rsf,\
                open(self.BPMF_file) as bf:
            for line1, line2, line3, line4, line5 in zip(ikf, bmf, ukf, rsf, bf):
                # the user, movie, and original information are same for two lines.
                userid, movieid, origin_rating, predict1 = line1.split()
                predict2 = line2.split()[-1]
                predict3 = line3.split()[-1]
                predict4 = line4.split()[-1]
                predict5 = line5.split()[-1]
                predictions = [float(predict1), float(predict2), float(predict3), float(predict4), float(predict5)]
                # average = (float(predict1) + float(predict2)\
                #        + float(predict3) + float(predict4) + float(predict5))/5.0
                # change this function to apply different weighted average strategy.
                predict = self.avg(predictions) 
                if movieid in self.bias_map:
                    predict = predict - float(self.bias_map[movieid])
                # print movieid, origin_rating, predict, predict1, predict2, predict3, predict4, predict5
                # print movieid, origin_rating, predict
                # predict = float(predict1)
                # the distance from the predicted to the original.
                diff = abs(predict - float(origin_rating))
                # the squired difference 
                squired_diff = (predict - float(origin_rating))**2
                total_diff += diff
                total_squired_diff += squired_diff
                total_items += 1
        MAE = total_diff/total_items
        RMSE = math.sqrt(total_squired_diff/total_items)
        print MAE, RMSE

    """
    For 5 stars ratings, all algorithms will always lower than the true rating
    this method handle this edge problem by estimate if it is most probable to be a 5 rating, then make it to be 5.
    """
    def handle_edge(self, predictions):
        count_upper = 0
        count_lower = 0
        # the threshold of rating is 5
        threshold_upper = 4.5 
        # if count is greater than this count then it will return upper
        threshold_upper_count = 4
        # threshold of rating is 0
        threshold_lower = 1.0
        threshold_lower_count = 4
        for one in predictions:
            if one > threshold_upper:
                count_upper += 1
            elif one < threshold_lower:
                count_lower += 1
        if count_upper >= threshold_upper_count:
            return 4.6
        elif count_lower >= threshold_lower_count:
            return 0
        return -1

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
        threshold = 1
        args = [float(one) for one in args]
        # -- to use median as mid
        #median = self.get_median(s_args)
        # -- to use mean as mid
        s_args = sorted(args)
        mid = self.avg(*args) 
        start, end = s_args[0], s_args[-1]
        if abs(start - mid) > threshold:
            index = 0
            while index < self.ratings_remove:
                s_args.pop(0); index += 1
        if abs(end - mid) > threshold:
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
   
    def diagonal(self, *args):
        total = 0
        for one in args:
            total += float(one)**2
        return math.sqrt(total/5)

    """
    Surprise, got 0.699989449999 0.903466663523 -best by far.
    """
    def avg(self, args):
        total = 0
        for one in args:
            total += one
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
        args.sort()
        avg = self.get_median(args)
        start, end = args[0], args[-1]
        if abs(start - avg) > abs(end - avg):
            index = 0
            while index < self.ratings_remove:
                args.pop(0); index += 1
        elif abs(start - avg) < abs(end - avg):
            index = 0
            while index < self.ratings_remove:
                args.pop(-1); index += 1
        # calculate average again
        total = 0
        num = 0
        for one in args:
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
hybrid(data).majority_vote()
