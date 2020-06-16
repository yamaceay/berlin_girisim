#Import libraries
import numpy as np
import pandas as pd
from math import ceil
from matplotlib import pyplot as plt
from datetime import date

#Options
print("""Options:\n
    ESC: exit the database
    RST: reset workspace and restart
    LOG: log cache
    R_A: display the existing data [read_all(title)]
    D_A: delete the existing data [delete_all(title)]
    W_A: overwrite the existing data [write_all(df, title)]
    V_A: visualize existing data [plot_all(x_feature, y_feature, kind, title)]
    R_R: read the index-th row [read_row(index, title)]
    A_R: append the created row [append_row(row, title)]
    D_R: delete the index-th row [delete_row(index, title)]
    C_R: create a row [create_row(n_student, n_normal, discount_percent, unit_price, title)]
    U_O: update a cell in existing data [update_one(index, feature, value, title)]
\n""")

#File configuration
print("Enter the name of the file (default: 'table_0'): ")
title = input()
if(title == ""):
    title = "table_0"

#Display the existing data [read_all(title)]
def read_all(title = title):
    return pd.read_csv("datasets/"+title+".csv").drop("Unnamed: 0", 1)

#Overwrite the existing data [write_all(df, title)]
def write_all(df, title = title):
    df.to_csv("datasets/"+title+".csv", mode = "w")

#Visualize existing data [plot_all(x_feature, y_feature, kind, title)]
def plot_all(x_feature, y_feature, kind = "line", title = title):
    df = read_all(title)
    if(x_feature == "index" and y_feature in df.columns):
        plotted = df[[y_feature]].reset_index()
    elif(x_feature in df.columns and y_feature in df.columns):
        plotted = df[[x_feature, y_feature]]
    else:
        print("Enter valid feature names!")
    fig, ax = plt.subplots(1, 1, figsize = (10, 10))
    del fig
    if(kind):
        plotted.plot(x = x_feature, y = y_feature, kind = kind, ax = ax)
    ax.set_title(kind+" plot: "+x_feature+" ~ "+y_feature)
    plt.show()
    
#Append the created row [append_row(row, title)]
def append_row(row, title = title):
    df_ = pd.read_csv("datasets/"+title+".csv").drop("Unnamed: 0", 1)
    df = df_.append(row)
    df.to_csv("datasets/"+title+".csv", mode = "w")

#Delete the index-th row [delete_row(index, title)]
def delete_row(index, title = title):
    df = read_all(title)
    print("Deleted: \n", pd.DataFrame(df.iloc[index]).transpose())
    df.drop(df.index[index], axis = 0, inplace = True)
    write_all(df, title)

#Delete the existing data [delete_all(title)]
def delete_all(title = title):
    df = read_all(title)
    print("Deleted: \n", df)
    write_all(pd.DataFrame(), title)
    del df

#Read the index-th row [read_row(index, title)]
def read_row(index, title = title):
    df = read_all(title)
    if(len(df.iloc[index]) > 0):
        return pd.DataFrame(df.iloc[index]).transpose()

#Update a cell in existing data [update_one(index, feature, value, title)]
def update_one(index, feature, value, title = title):
    df = read_all(title)
    df_ = df.copy()
    df_[feature] = value
    write_all(df_, title)

#Create a row [create_row(n_student, n_normal, discount_percent, unit_price, title)]
def create_row(n_student, n_normal, discount_percent, unit_price, title = title):
    date_of = date.today().strftime("%d-%m-%Y")
    n_total = n_student + n_normal
    student_ratio = n_student / n_total
    old_total = unit_price * n_total
    new_total = (n_student * (1-discount_percent) + n_normal) * unit_price
    difference = old_total - new_total
    new_customers = ceil(difference / ((1-discount_percent) * unit_price))
    row = pd.DataFrame(np.array([date_of, n_student, n_normal, student_ratio, discount_percent,
     unit_price, old_total, new_total, difference, new_customers]).reshape(1, -1), 
    columns = ["date", "n_student", "n_normal", "student_ratio", "discount_percent",
     "unit_price", "old_total", "new_total", "difference", "new_customers"])
    return row

#Cache
row_created = []
row_read = []
df_read = pd.DataFrame()
df_write = pd.DataFrame()

#Loop configuration
opened = True
while(opened):
    #Operation code
    print("What do you want to do? ")
    opcode = input()
    if(opcode == "R_A"):
        df_read = read_all()
        print(df_read)
    elif(opcode == "D_A"):
        delete_all()
    elif(opcode == "W_A"):
        print("Overwritten: \n", df_write)
        write_all(df_write)
    elif(opcode == "V_A"):
        df = read_all()
        print("Features: \n", ", ".join(df.columns), "\n")
        print("Enter the feature for x_axis: ")
        x_feature = input()
        print("Enter the feature for y_axis: ")
        y_feature = input()
        print("""You can specify the type of plot. Valid types are:
            ‘line’ : line plot
            ‘bar’ : vertical bar plot
            ‘barh’ : horizontal bar plot
            ‘hist’ : histogram
            ‘box’ : boxplot
            ‘kde’ : Kernel Density Estimation plot
            ‘density’ : same as ‘kde’
            ‘area’ : area plot
            ‘pie’ : pie plot
            ‘scatter’ : scatter plot
            ‘hexbin’ : hexbin plot""")
        print("Enter the kind of plot (default = 'line')")
        kind = input()
        plot_all(x_feature, y_feature, kind)
    elif(opcode == "R_R"):
        print("Enter the index of the row: ")
        index = int(input())
        row_read = read_row(index)
        print(row_read)
    elif(opcode == "D_R"):
        print("Enter the index of the row: ")
        index = int(input())
        delete_row(index)
    elif(opcode == "C_R"):
        print("Enter the number of students: ")
        n_student = int(input())
        print("Enter the number of normal people: ")
        n_normal = int(input())
        print("Enter the discount percent (without %): ")
        discount_percent = int(input())/100
        print("Enter the price of a single product/service: ")
        unit_price = int(input())
        row_created = create_row(n_student, n_normal, discount_percent, unit_price)
        print(row_created)
    elif(opcode == "A_R"):
        row = row_created
        print(row)
        append_row(row)
    elif(opcode == "U_O"):
        print("Enter the index of the row: ")
        index = int(input())
        print("Enter the feature that you want to update: ")
        feature = input()
        print("Enter the new value: ")
        value = int(input())
        update_one(index, feature, value)
    elif(opcode == "ESC"):
        opened = False
        print("Exit database")
    elif(opcode == "RST"):
        opened = False
        if(not(len(row_created) == 0)):
            print("Last created row: \n", row_created)
            row_created = []
        if(not(len(row_read) == 0)):
            print("Last read row: \n", row_read)
            row_read = []
        if(not(df_read.size == 0)):
            print("Last read dataframe: \n", df_read)
            df_read = pd.DataFrame()
        if(not(df_write.size == 0)):
            print("Last write dataframe: \n", df_write)
            df_write = pd.DataFrame()
        opened = True
        print("Restart database")
    elif(opcode == "LOG"):
        if(not(len(row_created) == 0)):
            print("Last created row: \n", row_created)
        if(not(len(row_read) == 0)):
            print("Last read row: \n", row_read)
        if(not(df_read.size == 0)):
            print("Last read dataframe: \n", df_read)
        if(not(df_write.size == 0)):
            print("Last write dataframe: \n", df_write)
    else:
        print("Enter a valid operation code.")