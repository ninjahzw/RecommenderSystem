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
        with open(self.BPMF_file) as ikf, open(self.RegSVD_file) as bmf:
            for line1, line2 in zip(ikf, bmf):
                # the user, movie, and original information are same for two lines.
                userid, movieid, origin_rating, predict1 = line1.split()
                predict2 = line2.split()[-1]
                predict = (float(predict1) + float(predict2))/2.0
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
      
hybrid().majority_vote()
