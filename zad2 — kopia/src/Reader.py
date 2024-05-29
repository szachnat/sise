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
        data=[]
        for file_f8 in statFiles_f8:
            if not os.path.exists(file_f8) or field_names == None:
                return None
            with open(file_f8, mode='r', encoding= 'utf-8') as csv_file:
                csv_reader=csv.reader(csv_file)
                for row in csv_reader:
                    if(row[0]!='' and row[1]!=''):
                        data.append(Reader.to_float(row))

        for file_f10 in statFiles_f10:
            if not os.path.exists(file_f10) or field_names == None:
                return None
            with open(file_f10, mode='r', encoding= 'utf-8') as csv_file:
                csv_reader=csv.reader(csv_file)
                for row in csv_reader:
                    if(row[0]!='' and row[1]!=''):
                        data.append(Reader.to_float(row))
        return data
    
    def load_testing_data(self)-> list[dict] | None:
        data=[]
        for file_f8 in statFiles_f8_dyn:
            if not os.path.exists(file_f8) or field_names == None:
                return None
            with open(file_f8, mode='r', encoding= 'utf-8') as csv_file:
                csv_reader=csv.reader(csv_file)
                for row in csv_reader:
                    if(row[0]!='' and row[1]!=''):
                        data.append(Reader.to_float(row))
        for file_f10 in statFiles_f10_dyn:
            if not os.path.exists(file_f10) or field_names == None:
                return None
            with open(file_f10, mode='r', encoding= 'utf-8') as csv_file:
                csv_reader=csv.reader(csv_file)
                for row in csv_reader:
                    if(row[0]!='' and row[1]!=''):
                        data.append(Reader.to_float(row))
        return data
    def normalize(data):
        # Obliczenie min i max dla całej macierzy
        flat_matrix = [item for sublist in data for item in sublist]
        data_min = min(flat_matrix)
        data_max = max(flat_matrix)
        
        # Normalizacja macierzy
        normalized_matrix = [[(x - data_min) / (data_max - data_min) for x in row] for row in data]
        
        return normalized_matrix, data_min, data_max

    def denormalize(data, data_min, data_max):
        # Denormalizacja macierzy
        # Denormalizacja macierzy
        denormalized_matrix = [[x * (data_max - data_min) + data_min for x in row] for row in data]
        
        return denormalized_matrix
    
    def to_float(row):
        floats=[]
        floats.append(float(row[0]))
        floats.append(float(row[1]))
        floats.append(float(row[2]))
        floats.append(float(row[3]))
        return floats
    
