
import siftnsave as sift
from Result import Result
from Query import Query
import math


def objectRecognition(mObj, methodType, query, dataset):

    if methodType == "Sift Matching":
        sift.siftMatching(mObj, query, dataset)



    return;

def main():

    #Dataset
    dataset = ['banana1.png','banana2.png','banana3.png','banana4.png',
               'banana5.jpg', 'banana6.jpg', 'banana7.jpg', 'banana8.jpg',
               'banana9.jpg', 
               'bar1.png', 'bar2.png','bar3.png', 'bar4.png',
               'box1.png', 'box2.png', 'box3.png', 'box4.png',
               'box5.png', 'box6.png', 'box7.png', 'oj1.png',
               'oj2.png', 'oj3.png','oj4.png','oj5.png',
               'oj6.jpg', 'oj7.jpg', 'oj8.jpg', 'oj9.jpg', 
               'carrot1.png', 'carrot2.png', 'carrot3.png', 'carrot4.png',
               'carrot5.png', 'carrot6.png', 'carrot7.png', 'carrot8.jpg',
               'carrot9.jpg', 'carrot10.jpg', 'carrot11.jpg', 'carrot12.jpg',
               'carrot13.jpg', 'carrot14.jpg', 'energy1.jpg', 'energy2.jpg',
               'energy3.jpg', 'energy4.jpg','coffee1.jpg', 'coffee2.jpg',
               'coffee3.jpg', 'coffee4.jpg']
    objects = []
    #0-8 banana
   # 9-12 bar
   # 13-19 box
    #20-28 orange
   # 29-42 carrot
   # 43-46 energy
   #  47-50 coffee
    #each image in dataset will be used as a query
    for i in range(len(dataset)):
        if(i == 1):
            break


        objects.append(Query(dataset[i]))

        objectRecognition(objects[i], "Sift Matching", dataset[i], dataset)

        #Print the ranking for each test
        print "Query image: "+dataset[i]
        for k in range(len(objects[i].results)):
            print "    Test: "+objects[i].get_result(k).type
            print "         Ranking: "
            for j in range(len(objects[i].get_result(k).matches)):
                print "         "+str(j+1)+": "+objects[i].get_result(k).get_match(j)

    #Multi dimensional dictionary to store Method used, Variation of method, # of queries, # of matches, and scores
    testing = {}

    pass;


if __name__ == "__main__": main()


