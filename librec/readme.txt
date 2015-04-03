* LibRec Version 1.2

* see changes at https://github.com/guoguibing/librec/blob/master/CHANGES.md

* librec.jar is a runnable jar via 
    java -jar librec.jar
or 
    java -jar librec.jar -c yourConfig.conf [You may try with BiasedMF.conf]

* Folder librec_lib contains all depedent libraries. 

* log4j.xml configs the logger for librec.jar
    comment out: <!-- <appender-ref ref="STDOUT"/> -->  if you don't need console output.

* librec.conf configs the recommender for LibRec
  to understand the configurations, see http://www.librec.net/tutorial.html#config

* The FilmTrust data set is included

    * filmtrust-ratings.txt: user-item rating data
    * filmtrust-trust.txt: user-user trust data

* Contact: guoguibing@gmail.com