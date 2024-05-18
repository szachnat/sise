import glob
import csv
from os.path import isfile, join
import os
import re
from os import listdir


solutionRegex_f8 = r'^f8_stat+_[0-9]+.csv$'
mypath_f8 = "..\\dane\\f8\\stat"
statFiles_f8 = [join(mypath_f8, f) for f in listdir(mypath_f8) if isfile(join(mypath_f8, f)) and re.search(solutionRegex_f8, f)]

solutionRegex_f10 = r'^f10_stat+_[0-9]+.csv$'
mypath_f10 = "..\\dane\\f10\\stat"
statFiles_f10 = [join(mypath_f10, f) for f in listdir(mypath_f10) if isfile(join(mypath_f10, f)) and re.search(solutionRegex_f10, f)]


field_names =["x_UWB","y_UWB","x_actual","y_actual"]

solutionRegex_f8_dyn = r'^f8_dyn+_[0-9]+[a-zA-Z].csv$'
mypath_f8_dyn = "..\\dane\\f8\\dyn"
statFiles_f8_dyn = [join(mypath_f8_dyn, f) for f in listdir(mypath_f8_dyn) if isfile(join(mypath_f8_dyn, f)) and re.search(solutionRegex_f8_dyn, f)]

solutionRegex_f10_dyn = r'^f10_dyn+_[0-9]+[a-zA-Z].csv$'
mypath_f10_dyn = "..\\dane\\f10\\dyn"
statFiles_f10_dyn = [join(mypath_f10_dyn, f) for f in listdir(mypath_f10_dyn) if isfile(join(mypath_f10_dyn, f)) and re.search(solutionRegex_f10_dyn, f)]

class Reader:
    def load_learning_data(self)-> list[dict] | None:
        #a=0
        #b=0
        data=[]
        for file_f8 in statFiles_f8:
            #print(file_f8)
            #a+=1
            if not os.path.exists(file_f8) or field_names == None:
                return None
            
            with open(file_f8, mode='r', encoding= 'utf-8') as csv_file:
                csv_reader=csv.DictReader(csv_file, fieldnames=field_names, delimiter=',', quoting=csv.QUOTE_NONE)
                for row in csv_reader:
                    data.append(row)
                    #print(row)
            #return data
        for file_f10 in statFiles_f10:
            #print(file_f10)
            #b+=1
            if not os.path.exists(file_f10) or field_names == None:
                return None
            with open(file_f10, mode='r', encoding= 'utf-8') as csv_file:
                csv_reader=csv.DictReader(csv_file, fieldnames=field_names, delimiter=',', quoting=csv.QUOTE_NONE)
                for row in csv_reader:
                    data.append(row)
                    #print(row)
        #print(a,b)
        return data
    
    def load_testing_data(self)-> list[dict] | None:
        #a=0
        #b=0
        data=[]
        for file_f8 in statFiles_f8_dyn:
            #print(file_f8)
            #a+=1
            if not os.path.exists(file_f8) or field_names == None:
                return None
            
            with open(file_f8, mode='r', encoding= 'utf-8') as csv_file:
                csv_reader=csv.DictReader(csv_file, fieldnames=field_names, delimiter=',', quoting=csv.QUOTE_NONE)
                for row in csv_reader:
                    data.append(row)
                    #print(row)
            #return data
        for file_f10 in statFiles_f10_dyn:
            #print(file_f10)
            #b+=1
            if not os.path.exists(file_f10) or field_names == None:
                return None
            with open(file_f10, mode='r', encoding= 'utf-8') as csv_file:
                csv_reader=csv.DictReader(csv_file, fieldnames=field_names, delimiter=',', quoting=csv.QUOTE_NONE)
                for row in csv_reader:
                    data.append(row)
                    #print(row)
        #print(a,b)
        return data