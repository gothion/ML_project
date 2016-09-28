# coding=utf8
import numpy as np

from sklearn import preprocessing
from sklearn.cluster import KMeans

from ml_project import data_combiner


def read_data(input_file_path):
    data_point_arr = []
    label_arr = []
    object_info_map, object_name_arr = statistic_feature_info(input_file_path)
    print len(object_name_arr)
    with open(input_file_path, mode='r') as samples:
        for line in samples:
            feature_vector = extract_feature(line, object_info_map, object_name_arr)
            data_point_arr.append(feature_vector)
            line_arr = line.split('\t')
            label_arr.append(line_arr[0] + "," + line_arr[-1])
    return np.array(data_point_arr), label_arr


def extract_feature(sample_line, object_info_map, object_name_arr):
    line_arr = sample_line.split('\t')
    multiple_object_info = line_arr[4]
    object_info_vector = extract_object_info(multiple_object_info, object_info_map, object_name_arr)
    quality = float(line_arr[5])
    return object_info_vector + [quality]


def extract_object_info(multiple_object_info, object_info_map, object_name_arr):
    vector_info = [0.0] * len(object_name_arr) * 2
    object_info_arr = multiple_object_info.split(';')[:-1]
    for object_info in object_info_arr:
        object_field_arr = object_info.split(',')
        object_name = object_field_arr[0]
        object_index = object_info_map[object_name]
        object_area = float(object_field_arr[6])
        vector_index = 2*object_index
        vector_info[vector_index] += 1.0
        vector_info[vector_index + 1] += object_area
    return vector_info


def statistic_feature_info(input_file_path):
    object_name_index_map = {}
    object_name_arr = []
    with open(input_file_path, mode='r') as samples:
        index = 0
        for line in samples:
            multiple_object_info = line.split('\t')[4]
            object_info_arr = multiple_object_info.split(';')[:-1]
            for object_info in object_info_arr:
                object_field_arr = object_info.split(',')
                object_name = object_field_arr[0]
                if object_name not in object_name_index_map:
                    object_name_index_map[object_name] = index
                    index += 1
                    object_name_arr.append(object_name)
    return object_name_index_map, object_name_arr


def cluster(data_point_arr, photo_ids):
    random_state = 170
    scaled_point_arr = preprocessing.scale(data_point_arr)
    y = KMeans(n_clusters=4, random_state=random_state).fit_predict(data_point_arr)
    y2 = KMeans(n_clusters=4, random_state=random_state).fit_predict(scaled_point_arr)
    write_photo_id_by_cluster(y, photo_ids)
    write_photo_id_by_cluster(y2, photo_ids, suffix='scaled')


def write_photo_id_by_cluster(cluster_result, photo_ids, suffix=''):
    cluster_file_map = {}
    for index, cluster_num in enumerate(cluster_result):
        if cluster_num not in cluster_file_map:
            file_name = _get_cluster_result_file_name(cluster_num, suffix)
            cluster_file_map[cluster_num] = open(data_combiner.get_result_data(file_name), 'w')
        out_put_data = cluster_file_map[cluster_num]
        out_put_data.write(photo_ids[index])
    for out_put_data in cluster_file_map.values():
        out_put_data.close()


def _get_cluster_result_file_name(cluster_num, suffix):
    return 'cluster_num_{0}_{1}.test.txt'.format(cluster_num, suffix)


if __name__ == '__main__':
    data_points, photo_ids = read_data('/home/galois/PycharmProjects/ml_project/'
                                       'ml_project/picture_search/sport_kept.csv_with_url')
    cluster(data_points, photo_ids)
