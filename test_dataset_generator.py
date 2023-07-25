#This script generates set of traning data for decision tree learning

import random
import csv

type_set = [1, 2 , 3, 4, 5]
weight_set_box = [3, 4, 5]
weight_set_shelf = [3, 4, 5]
load_set = [0, 1]


with open('tree_utils/train_dataset.csv', 'w', newline='') as file:
    filewriter = csv.writer(file)

    filewriter.writerow(["shelf type", "shelf max weight", "shelf loaded", "box type", "box weight", "cart loaded", "load possible"])

    chosen_set = []

    for i in range(500):
        chosen_set.append(random.randint(0,1295))

    iterator = 0

    for shelf_type in type_set:
        for shelf_weigth in weight_set_shelf:
            for shelf_load in load_set:
                for box_type in type_set:
                    for box_weight in weight_set_box:
                        for box_load in load_set:
                            if shelf_type == box_type and shelf_weigth >= box_weight and shelf_load == load_set[0] and box_load == load_set[0]:
                                filewriter.writerow([shelf_type, shelf_weigth, shelf_load, box_type, box_weight, box_load, 1])
                            else:
                                #if (iterator % 2 == 0):
                                filewriter.writerow([shelf_type, shelf_weigth, shelf_load, box_type, box_weight, box_load, 0])
                            iterator += 1
