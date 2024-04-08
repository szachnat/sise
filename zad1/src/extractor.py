from os import listdir
from os.path import isfile, join
import re
from typing import Callable
from copy import deepcopy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

solutionRegex = r'^[a-zA-Z0-9]+_[0-9]+_[0-9]+_[a-zA-Z]+_[a-zA-Z]+_stats.txt$'
mypath = "."#\\_testy"#".\\puzzles"
wykresyPath = "..\\wykresy"#".\\wykresy"

statFiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and re.search(solutionRegex, f)]

class Stats:
    def __init__(self, distance: int, type: str, parameter: str, length: int, visited: int, computed: int, time: float, maxDepth: int) -> None:
        self.distance = distance
        self.type = type
        self.parameter = parameter
        self.length = length
        self.visited = visited
        self.computed = computed
        self.time = time
        self.maxDepth = maxDepth

def get_from_filename(filename: str) -> tuple[int, str, str]:
    texts = filename.split("_")
    distance = int(texts[1])
    type = texts[3]
    parameter = texts[4]
    return distance, type, parameter

def get_from_file(filename: str) -> tuple[int, int, int, int, float]:
    text = ""
    with open(filename, 'r') as f:
        text = f.read()
    lines = text.split('\n')
    length = int(lines[0])
    visited = int(lines[1])
    computed = int(lines[2])
    maxDepth = int(lines[3])
    time = float(lines[4])
    return length, visited, computed, maxDepth, time

def group_by_stats(statsList: list[Stats], attrName: str) -> dict[object, list[Stats]]:
    groups = {}
    for stats in statsList:
        groupName = getattr(stats, attrName, None)
        if groupName is None:
            raise Exception(f"Nie ma atrybutu o podanej nazwie '{attrName}'")

        group = groups.get(groupName, None)
        if group is None:
            group = []
        group.append(stats)
        groups[groupName] = group
    return groups

def condition_stats(statsList: list[Stats], attrName: str, condition: Callable[[object], bool]) -> list[Stats]:
    conditionedStats = []
    for stat in statsList:
        attrVal = getattr(stat, attrName, None)
        if condition(attrVal):
            conditionedStats.append(stat)
    return conditionedStats

def avarage_stats(statsList: list[Stats]) -> Stats:
    avg_length = 0
    avg_visited = 0
    avg_computed = 0
    avg_time = 0
    avg_maxDepth = 0
    new_list = condition_stats(statsList, 'length', lambda val: val != -1)
    for stat in new_list:
        avg_length += stat.length
        avg_visited += stat.visited
        avg_computed += stat.computed
        avg_time += stat.time
        avg_maxDepth += stat.maxDepth
    avg_length /= len(new_list)
    avg_visited /= len(new_list)
    avg_computed /= len(new_list)
    avg_time /= len(new_list)
    avg_maxDepth /= len(new_list)

    avg_stats = Stats(0, "", "", avg_length, avg_visited, avg_computed, avg_time, avg_maxDepth)
    return avg_stats

def max_stats(statsList: list[Stats]) -> Stats:
    max_length = 0
    max_visited = 0
    max_computed = 0
    max_time = 0
    max_maxDepth = 0
    new_list = condition_stats(statsList, 'length', lambda val: val != -1)
    if len(new_list) > 0:
        max_length = new_list[0].length
        max_visited = new_list[0].visited
        max_computed = new_list[0].computed
        max_time = new_list[0].time
        max_maxDepth = new_list[0].maxDepth
        for stat in new_list[1:]:
            if stat.length > max_length:
                max_length = stat.length
            if stat.visited > max_visited:
                max_visited = stat.visited
            if stat.computed > max_computed:
                max_computed = stat.computed
            if stat.time > max_time:
                max_time = stat.time
            if stat.maxDepth > max_maxDepth:
                max_maxDepth = stat.maxDepth
    print("-",max_visited)
    max_stats = Stats(0, "", "", max_length, max_visited, max_computed, max_time, max_maxDepth)
    return max_stats

def min_stats(statsList: list[Stats]) -> Stats:
    min_length = 0
    min_visited = 0
    min_computed = 0
    min_time = 0
    min_maxDepth = 0
    new_list = condition_stats(statsList, 'length', lambda val: val != -1)
    if len(new_list) > 0:
        min_length = new_list[0].length
        min_visited = new_list[0].visited
        min_computed = new_list[0].computed
        min_time = new_list[0].time
        min_maxDepth = new_list[0].maxDepth
        for stat in new_list[1:]:
            if stat.length < min_length:
                min_length = stat.length
            if stat.visited < min_visited:
                min_visited = stat.visited
            if stat.computed < min_computed:
                min_computed = stat.computed
            if stat.time < min_time:
                min_time = stat.time
            if stat.maxDepth < min_maxDepth:
                min_maxDepth = stat.maxDepth

    min_stats = Stats(0, "", "", min_length, min_visited, min_computed, min_time, min_maxDepth)
    return min_stats

def found_not_found_ratio(statsList: list[Stats]) -> tuple[int, int]:
    found = 0
    not_found = 0
    
    for stat in statsList:
        if stat.length == -1:
            not_found += 1
        else:
            found += 1
    return found, not_found

def get_only_one_attr(groups: dict[object, dict[object, dict[object, Stats]]], attrName: str) ->dict[object, dict[object, dict[object, object]]]:
    new_groups = deepcopy(groups)
    for t in new_groups.keys():
        for p in new_groups[t].keys():
            for d in new_groups[t][p].keys():
                value = getattr(new_groups[t][p][d], attrName, None)
                if value == None:
                    raise Exception(f"Nie ma objektu o podanej nazwie '{attrName}'")
                new_groups[t][p][d] = value
    return new_groups

def groupedBarChart(groups: dict[object, dict[object, Stats]], title: str, yLabel: str, xLabel: str, filepath: str):
    # dla danego typu (bfs) podzielić na konkretne dystanse i dla każdego dystansu wypisać wartości przy każdym parametrze

    distances: list[object] = groups.keys()
    types_and_values_for_distance: dict[str, list[object]] = {}
    for d in groups.keys():
        for p in groups[d].keys():
            if types_and_values_for_distance.get(p, None) is None:
                types_and_values_for_distance[p] = []
            types_and_values_for_distance[p].append(groups[d][p])

    to_data_frame = {}
    to_data_frame[xLabel] = distances
    for type in types_and_values_for_distance.keys():
        to_data_frame[type] = types_and_values_for_distance[type]

    df = pd.DataFrame(to_data_frame)
    # df = pd.DataFrame({'Subject': ['English', 'Maths', 'Science'], 'Mean': [90, 87, 67], 'cos': [0, 80, 20]})

    # create bar graph
    ax = df.plot.bar(x=xLabel, y=types_and_values_for_distance.keys(), fontsize='9', rot=0)
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.set_title(title)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
 
   

    plt.savefig(filepath, bbox_inches='tight', dpi=100)
    #plt.show()

def groupedBarChartRatio(groups: dict[object, tuple[int, int]], title: str, yLabel: str, xLabel: str, filepath: str):
    x_keys: list[object] = groups.keys()
    found_for_x_keys: dict[str, list[object]] = {}

    founds = 0
    not_founds = 0
    for x in groups.keys():
        found, not_found = groups[x]
        if found_for_x_keys.get('Znalezione', None) is None:
            found_for_x_keys['Znalezione'] = []
        found_for_x_keys['Znalezione'].append(found)
        if found_for_x_keys.get('Nie znalezione', None) is None:
            found_for_x_keys['Nie znalezione'] = []
        found_for_x_keys['Nie znalezione'].append(not_found)

        founds += found
        not_founds += not_found

    # print((not_founds * 100) / (founds + not_founds))

    to_data_frame = {}
    to_data_frame[xLabel] = x_keys
    for type in found_for_x_keys.keys():
        to_data_frame[type] = found_for_x_keys[type]

    df = pd.DataFrame(to_data_frame)
    # df = pd.DataFrame({'Subject': ['English', 'Maths', 'Science'], 'Mean': [90, 87, 67], 'cos': [0, 80, 20]})

    # create bar graph
    ax = df.plot.bar(x=xLabel, y=found_for_x_keys.keys(), fontsize='9', rot=0, stacked=True)
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.set_title(title)

    plt.savefig(filepath, bbox_inches='tight', dpi=100)
    plt.show()

def main():
    all_stats = []
    for stat in statFiles:
        distance, type, parameter = get_from_filename(stat)
        length, visited, computed, maxDepth, time = get_from_file(stat)
        all_stats.append(Stats(distance, type, parameter, length, visited, computed, time, maxDepth))

    avg_res = group_by_stats(all_stats, 'type')
    # min_res = deepcopy(avg_res)
    # max_res = deepcopy(avg_res)
    for t in avg_res.keys():
        avg_res[t] = group_by_stats(avg_res[t], 'distance')
        for d in avg_res[t].keys():
            avg_res[t][d] = group_by_stats(avg_res[t][d], 'parameter')
            new_params = {}
            for p in avg_res[t][d].keys():
                new_p = p.upper()
                if new_p == 'HAMM':
                    new_p = 'Hamminga'
                elif new_p == 'MANH':
                    new_p = 'Manhattan'
                avg_res[t][d][p] = avarage_stats(avg_res[t][d][p])
                new_params[new_p] = avg_res[t][d][p]
            avg_res[t][d] = new_params

    avg_length = get_only_one_attr(avg_res, 'length')
    avg_visited = get_only_one_attr(avg_res, 'visited')
    avg_computed = get_only_one_attr(avg_res, 'computed')
    avg_time = get_only_one_attr(avg_res, 'time')
    avg_maxDepth = get_only_one_attr(avg_res, 'maxDepth')

    for t in avg_res.keys():
        type = t.upper()
        if type == 'ASTR':
            type = 'A*'
        groupedBarChart(avg_length[t], type, "Średnia długość rozwiązania", "Odległość", join(wykresyPath, f"{t.lower()}_długość.png"))
        groupedBarChart(avg_visited[t], type, "Średnia liczba stanów odwiedzonych", "Odległość", join(wykresyPath, f"{t.lower()}_odwiedzone.png"))
        groupedBarChart(avg_computed[t], type, "Średnia liczba stanów przetworzonych", "Odległość", join(wykresyPath, f"{t.lower()}_przetworzone.png"))
        groupedBarChart(avg_time[t], type, "Średni czas rozwiązywania (s)", "Odległość", join(wykresyPath, f"{t.lower()}_czas.png"))
        groupedBarChart(avg_maxDepth[t], type, "Średnia maksymalna głębokość rekursji", "Odległość", join(wykresyPath, f"{t.lower()}_rekursja.png"))


    # found_dist_res = group_by_stats(all_stats, 'type')
    # found_param_res = deepcopy(found_dist_res)
    # for t in found_dist_res.keys():
    #     found_dist_res[t] = group_by_stats(found_dist_res[t], 'distance')
    #     for d in found_dist_res[t].keys():
    #         found_dist_res[t][d] = found_not_found_ratio(found_dist_res[t][d])
    #     found_param_res[t] = group_by_stats(found_param_res[t], 'parameter')

    #     new_params = {}
    #     for p in found_param_res[t].keys():
    #         found_param_res[t][p] = found_not_found_ratio(found_param_res[t][p])
    #         new_p = p.upper()
    #         if new_p == 'HAMM':
    #             new_p = 'Hamminga'
    #         elif new_p == 'MANH':
    #             new_p = 'Manhattan'
    #         new_params[new_p] = found_param_res[t][p]
    #     found_param_res[t] = new_params

    # for t in found_dist_res.keys():
    #     type = t.upper()
    #     xlabel = "Porządek przeszukania sąsiedztwa"
    #     if type == 'ASTR':
    #         type = 'A*'
    #         xlabel = "Heurystyka"

    #     groupedBarChartRatio(found_dist_res[t], type, "Liczba zbadanych plików", "Odległość", join(wykresyPath, f"{t.lower()}_dist_liczba_znalezionych.png"))
    #     groupedBarChartRatio(found_param_res[t], type, "Liczba zbadanych plików", xlabel, join(wykresyPath, f"{t.lower()}_param_liczba_znalezionych.png"))

    # # TEST
    # for t in min_res.keys():
    #     min_res[t] = group_by_stats(min_res[t], 'distance')
    #     for d in min_res[t].keys():
    #         min_res[t][d] = group_by_stats(min_res[t][d], 'parameter')
    #         new_params = {}
    #         for p in min_res[t][d].keys():
    #             new_p = p.upper()
    #             if new_p == 'HAMM':
    #                 new_p = 'Hamminga'
    #             elif new_p == 'MANH':
    #                 new_p = 'Manhattan'
    #             min_res[t][d][p] = min_stats(min_res[t][d][p])
    #             new_params[new_p] = min_res[t][d][p]
    #         min_res[t][d] = new_params
    #
    # min_length = get_only_one_attr(min_res, 'length')
    # min_visited = get_only_one_attr(min_res, 'visited')
    # min_computed = get_only_one_attr(min_res, 'computed')
    # min_time = get_only_one_attr(min_res, 'time')
    # min_maxDepth = get_only_one_attr(min_res, 'maxDepth')
    #
    # for t in min_res.keys():
    #     type = t.upper()
    #     if type == 'ASTR':
    #         type = 'A*'
    #     groupedBarChart(min_length[t], type, "Najmniejsza długość rozwiązania", "Odległość", join(wykresyPath, f"{t.lower()}_min_długość.png"))
    #     groupedBarChart(min_visited[t], type, "Najmniejsza liczba stanów odwiedzonych", "Odległość", join(wykresyPath, f"{t.lower()}_min_odwiedzone.png"))
    #     groupedBarChart(min_computed[t], type, "Najmniejsza liczba stanów przetworzonych", "Odległość", join(wykresyPath, f"{t.lower()}_min_przetworzone.png"))
    #     groupedBarChart(min_time[t], type, "Najmniejszy czas rozwiązywania (ms)", "Odległość", join(wykresyPath, f"{t.lower()}_min_czas.png"))
    #     groupedBarChart(min_maxDepth[t], type, "Najmniejsza maksymalna głębokość rekursji", "Odległość", join(wykresyPath, f"{t.lower()}_min_rekursja.png"))

if __name__ == "__main__":
    main()