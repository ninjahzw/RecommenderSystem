# NOTE This is for data preprocessing to generate distinct lists of all Movies and Users.

# Path to the directory of your dataset, you can change this to your local path of the data when using this script to generate data. and comment mine.
data_path="/home/hzw/workspace/mldata"
# For movie data
cat $data_path/movies.dat | awk '{split($1,a,"::"); print a[1]}' | uniq > $data_path/all_movies
# for user data
cat $data_path/ratings.dat | awk '{split($1,a,"::"); print a[1]}' | uniq > $data_path/all_users
echo "complete!"
