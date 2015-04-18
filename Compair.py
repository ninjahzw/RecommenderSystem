import math
class Compair:
    def __init__(self):
        self.k = 300
        self.item_knn_result = "/disk/hou/workspace/liangdong/ItemKNN2-prediction-movie-300"
        self.regsvd_result = "/disk/hou/workspace/RecommenderSystem/librec-1m/result/predicts.RegSVD/RegSVD-prediction-movie"
        self.seperate_out = "/disk/hou/workspace/RecommenderSystem/librec-1m/myresult/ItemKNN2-prediction-movie-except-300"

    def seperate(self):
        s = set()
        out_file = open(self.seperate_out, "w")
        with open(self.item_knn_result) as f:
            for l in f:
                items = l.split()
                if items[-1] >= self.k
                    s.add(items[0]+"-"+items[1])
        with open(self.regsvd_result) as f:
            for l in f:
                items = l.split()
                if items[0]+"-"+items[1] in s:
                    continue
                out_file.write(l)
        out_file.close()

    def compair(self):
        total_squired_diff = 0
        total_diff = 0
        total_items = 0
        with open(self.seperate_out) as f:
            for l in f:
                items = l.split()
                original = float(items[2])
                predict = float(items[3])
                diff = abs(predict-original)
                squired_diff = diff**2
                total_diff += diff
                total_squired_diff += squired_diff
                total_items += 1
        MAE = total_diff/total_items
        RMSE = math.sqrt(total_squired_diff/total_items)
        print MAE, RMSE

    def origin(self):
        total_squired_diff = 0
        total_diff = 0
        total_items = 0
        with open(self.regsvd_result) as f:
            for l in f:
                items = l.split()
                original = float(items[2])
                predict = float(items[3])
                diff = abs(predict-original)
                squired_diff = diff**2
                total_diff += diff
                total_squired_diff += squired_diff
                total_items += 1
        MAE = total_diff/total_items
        RMSE = math.sqrt(total_squired_diff/total_items)
        print MAE, RMSE

#Compair().origin()
Compair().compair()


