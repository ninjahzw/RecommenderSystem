"""
This class is to  make each run of the LibRec algorithm consistent by making the folds same.
According to the first 5-fold result, 
For each fold, split the origin rating file into train (original - current_fold) and test (current_fold) data.
Then modify the the configuration file to use each train and test data to run instead of using k-fold
But after run all five train and test, the result is same as k-fold.
"""
import math, os
class SplitFold:
    def __init__(self):
        self.k = 300
        self.item_knn_result = "/disk/hou/workspace/RecommenderSystem/librec-1m/result/predicts.ItemKNN/ItemKNN-prediction-"
        self.original= "/disk/hou/workspace/ml-1m/ratings"
        self.seperate_out = "/disk/hou/workspace/RecommenderSystem/result/newtrain/"

    def split(self, fold, original, output):
        s = set()
        out_file_train = open(output + "train", "w")
        out_file_test = open(output + "test", "w")
        with open(fold) as f:
            for l in f:
                items = l.split()
                if items[-1] >= self.k:
                    s.add(items[0]+"-"+items[1])
        with open(original) as f:
            for l in f:
                items = l.split()
                if items[0]+"-"+items[1] in s:
                    out_file_test.write(l)
                    continue
                out_file_train.write(l)
        out_file_train.close()
        out_file_test.close()
    

split = SplitFold()
for i in xrange(1, 6):
    print split.seperate_out + str(i) + "/"
    os.system("mkdir -p " + split.seperate_out + str(i) + "/")
    split.split(split.item_knn_result + str(i) + ".txt", split.original, split.seperate_out + str(i) + "/")
