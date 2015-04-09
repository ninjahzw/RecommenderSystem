import math
class hybrid:

    def __init__(self):
        self.ItemKNN_file = "/disk/hou/workspace/RecommenderSystem/librec/result/predicts.ItemKNN/ItemKNN-prediction"
        self.Biased_MF_file = "/disk/hou/workspace/RecommenderSystem/librec/result/predicts.BiasedMF/BiasedMF-prediction"
        self.UserKNN_file = "/disk/hou/workspace/RecommenderSystem/librec/result/predicts.UserKNN/UserKNN-prediction"
        self.RegSVD_file = "/disk/hou/workspace/RecommenderSystem/librec/result/predicts.RegSVD/RegSVD-prediction"
        self.BPMF_file = "/disk/hou/workspace/RecommenderSystem/librec/result/predicts.BPMF/BPMF-prediction"
        self.original = "/disk/hou/workspace/mldata/ratings.csv"


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
                average = (float(predict1) + float(predict2)\
                        + float(predict3) + float(predict4) + float(predict5))/5.0
                predict = self.get_predict(predict1, predict2, predict3, predict4, predict5) 
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

    def get_predict(self, *args):
        total = 0
        num = 0
        for one in args:
            print one
            total += float(one)
            num += 1
        avg = total/num
        pairs = []
        for one in args:
            pairs.append([abs(float(one)-avg),float(one)])
        pairs.sort()
        # remove last two elements from dict
        pairs.pop()
        pairs.pop()
        total = 0
        for one in pairs:
            total += one[-1]
        print pairs
        print total/len(pairs)
        print '----------'
        return total/len(pairs)
      
hybrid().majority_vote()
