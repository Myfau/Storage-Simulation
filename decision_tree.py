import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg

attributes = ['shelf type','shelf max weight','shelf loaded','box type','box weight','cart loaded']

def treelearn():
    dataset = pandas.read_csv('tree_utils/train_dataset.csv')
    x = dataset[attributes] # atrybuty
    y = dataset['load possible'] # decyzje
    decision_tree = DecisionTreeClassifier()
    decision_tree = decision_tree.fit(x, y)
    return decision_tree

def make_decision(tree, shelf_type, shelf_max_weight, shelf_loaded, box_type, box_weight, cart_loaded): 
    decision = tree.predict([[shelf_type, shelf_max_weight, shelf_loaded, box_type, box_weight, cart_loaded]])
    return decision

def visualize_decision_tree(decision_tree):
    fig = plt.figure(figsize=(25,20))
    _ = tree.plot_tree(decision_tree, 
                   feature_names=attributes,  
                   filled=True)
    fig.savefig("tree_utils/decision_tree.png")

def decision_initialisation(tree, box, shelf, cart_loaded_bool):
    types = ["dang", "norm", "radi", "frag", "flam"]

    shelf_type = types.index(shelf.type) + 1
    box_type = types.index(box.type) + 1
    if shelf.is_loaded == False:
        shelf_loaded = 0
    else:
        shelf_loaded = 1
    if cart_loaded_bool == False:
        cart_loaded = 0
    else:
        cart_loaded = 1

    print(str(shelf_type) + " " + str(shelf.max_weight) + " " + str(shelf_loaded) + " " + str(box_type) + " " + str(box.weight) + " " + str(cart_loaded))

    decision = make_decision(tree, shelf_type, shelf.max_weight, shelf_loaded, box_type, box.weight, cart_loaded)

    print (decision)
    return decision