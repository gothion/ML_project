# coding=utf8
import numpy as np
import os

from sklearn.metrics import precision_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

this_dir, this_filename = os.path.split(__file__)
data_folder = os.path.normpath(os.path.join(this_dir, '..', 'data'))


def train_and_predict(x_data, y_data, train_num=700):
    length = len(x_data)
    indices = np.arange(length)
    rng = np.random.RandomState(0)
    rng.shuffle(indices)
    x_train = x_data[indices[:train_num]]
    y_train = y_data[indices[:train_num]]
    x_test = x_data[indices[train_num+1:]]
    y_test = y_data[indices[train_num+1:]]
    rfc = RandomForestClassifier(n_estimators=200)
    rfc.fit(x_train, y_train)
    result = rfc.predict(x_test)
    cm = confusion_matrix(y_test, rfc.predict(x_test), labels=[0, 1])
    print cm
    print precision_score(y_test, result)
    return precision_score(y_test, result), rfc

    # clf = GradientBoostingClassifier(n_estimators=1200, learning_rate=0.1, loss='deviance')
    # clf.fit(x_train, y_train)
    # result2 = clf.predict(x_test)
    # cm2 = confusion_matrix(y_test, result2)
    # print cm2
    # print precision_score(y_test, result2)
    # return precision_score(y_test, result2), clf



def read_sample(sample_label, sample_file_path, version=0):
    X = []
    Y = []
    with open(sample_file_path, mode='r') as samples:
        for line in samples:
            if version == 0:
                feature_vector = extract_feature(line)
            else:
                feature_vector = extract_feature_version1(line)

            if feature_vector[3] > 0.10:
                X.append(feature_vector)
                Y.append(sample_label)
    return np.array(X), np.array(Y)


def extract_feature_version1(sample_line):
    object_part = sample_line.split(' ')[0]
    object_part = object_part.split('_')[1]
    label_info = extract_object_info(object_part)
    label_num_index_arr = [0, 2, 4]
    object_num = 0.0
    for label_index in label_num_index_arr:
        object_num += label_info[label_index]
    # for label_index in label_num_index_arr:
    #     label_info[label_index] /= object_num
    # return [float(object_num)] + label_info
    return label_info


# def extract_feature(sample_line):
#     the_index = index_of_char(sample_line, ',', 2)
#     fore_part_sample = sample_line[:the_index]
#     object_num = int(fore_part_sample.split(',')[1])
#     object_part = sample_line[the_index+1:]
#     label_info = extract_object_info(object_part, object_num)
#     label_num_index_arr = [0, 2, 4]
#     # for label_index in label_num_index_arr:
#     #     label_info[label_index] /= object_num
#     # return [float(object_num)] + label_info
#     return label_info

def extract_feature(sample_line):
    line_arr = sample_line.split('\t')

    object_num = int(line_arr[3])
    object_part = line_arr[4]
    label_info = extract_object_info(object_part, object_num)
    quality = float(line_arr[-1])
    if is_part_of_car(sample_line):
        part_info = 1
    else:
        part_info = 0
    return label_info + [quality] + [part_info]

# def extract_car_object_size(sample_line):
#     line_arr = sample_line.split('\t')
#     object_part = line_arr[4]
#     width = float(line_arr[2])
#     height = float(line_arr[1])
#     max_area = 0.0
#     object_part_arr = object_part.split(';')[:-1]
#     for object_str in object_part_arr:
#         object_arr = object_str.split(',')
#         object_sign = object_arr[0]
#         if object_sign ==


def extract_object_info(object_part, object_num=-1):
    object_part_arr = object_part.split(';')
    if len(object_part_arr) > int(object_num):
        object_part_arr = object_part_arr[:object_num]
    result = [0.0] * 6
    for object_str in object_part_arr:
        object_info = extract_object_info_impl(object_str)
        for index in range(len(result)):
            result[index] += object_info[index]
    return result


def extract_object_info_impl(object_str):
    object_arr = object_str.split(',')
    object_sign = object_arr[0]
    object_area = float(object_arr[6])
    if object_sign =='other.other':
        unknown_label = 1
        car_label = 0
        not_related = 0
    elif object_sign == 'vehicle.car':
        unknown_label = 0
        car_label = 1
        not_related = 0
    else:
        unknown_label = 0
        car_label = 0
        not_related = 1
    return unknown_label, unknown_label*object_area,  \
        car_label, car_label * object_area, \
        not_related, not_related * object_area


def index_of_char(the_str, char, n_th):
    occur = 0
    for index, character in enumerate(the_str):
        if char == character:
            occur += 1
            if occur == n_th:
                return index
    if occur < n_th:
        return -1


def test():
    print index_of_char("hello world", 'w', 1)
    test_str = '720617597,6,person.face,0.998,75,565,218,688,0.0155;' \
               'person.body,0.959,39,457,305,1062,0.1422;' \
               'person.body,0.957,434,349,752,1016,0.1874;person.body,0.928,272,364,559,1045,0.1726;' \
               'person.face,0.890,318,493,449,623,0.0150;person.body,0.872,617,303,960,956,0.1978;'

    the_index = index_of_char(test_str, ',', 2)
    sub_str = test_str[the_index + 1:]
    print test_str
    print sub_str
    print sub_str.split(';')[:-1]
    feature_info = extract_feature(test_str)
    print feature_info


def get_model():
    # x_data1, y_data1 = read_sample(1, '/home/galois/PycharmProjects/ml_project/data/good', version=1)
    x_data3, y_data3 = read_sample(1, data_folder + '/car_select_url.txt')
    x_data2, y_data2 = read_sample(0, data_folder + '/bad_multi_lable_scoreb.txt')
    indices = np.arange(len(x_data2))
    rng = np.random.RandomState(0)
    rng.shuffle(indices)

    # x_data2 = x_data2[indices[:880]]
    # y_data2 = y_data2[indices[:880]]
    x_data1 = np.tile(x_data3, (2, 1))
    y_data1 = np.tile(y_data3, 2)
    # x_data1 = x_data3
    # y_data1 = y_data3

    x_data = np.concatenate((x_data1, x_data2))
    y_data = np.concatenate((y_data1,  y_data2))
    precision, model = train_and_predict(x_data, y_data)
    return precision, model


def prediction_with_model(model, out_put_file):
    to_be_predicted = read_predicted_line(data_folder + '/good_multi_lable_scoreb.txt')
    to_be_predicted2 = read_predicted_line(data_folder + '/bad_multi_lable_scoreb.txt')
    to_be_predicted = dict(to_be_predicted.items() + to_be_predicted2.items())
    with open(out_put_file, mode='w') as out_put_data:
        for photo_id, vector_info in to_be_predicted.iteritems():
            new_vector_info = vector_info.reshape(1, -1)
            if vector_info[3] > 0.10:
                out_put_data.write(photo_id + ',' + str(model.predict_proba(new_vector_info)[0][1]) + ','
                                    + str(vector_info) + '\n')


def read_predicted_line(file_path):
    picture_dict = {}
    with open(file_path, mode='r') as input_data:
        for line in input_data:
            photo_id = get_picture_id(line)
            picture_dict[photo_id] = np.array(extract_feature(line))
    return picture_dict


def get_picture_id(line):
    return line.split("\t")[0]


def is_part_of_car(line):
    str_vec = line.split('\t')
    str_vec2 = str_vec[4].split(';')
    height = int(str_vec[1])
    width = int(str_vec[2])
    for i in range(len(str_vec2)):
        str_vec3 = str_vec2[i].split(',')
        if 7 != len(str_vec3):
            continue
        center_x = (int(str_vec3[2]) + int(str_vec3[4])) / 2
        center_y = (int(str_vec3[3]) + int(str_vec3[5])) / 2
        center_x_dist = float(abs(width/2 - center_x)) / width
        center_y_dist = float(abs(height/2 - center_y)) / height

        if "car" in str_vec3[0] and (float(str_vec3[6]) > 0.36):
           return True
        if "other.other" == str_vec3[0] and (float(str_vec3[6]) > 0.8):
           return True
        if "car" in str_vec3[0] and ( center_x_dist < 0.2 and center_y_dist < 0.2):
           return True
        if "car" in str_vec3[0] and (int(str_vec3[2]) > 0 and int(str_vec3[4]) < width and int(str_vec[3]) > 0
            and int(str_vec3[5]) < height):
           return True
    return False


if __name__ == '__main__':
    precision, model = get_model()
    # print precision
    prediction_with_model(model, 'result3.txt')



class ObjectInfo(object):
    def __init__(self, area, x_point, y_point):
        self.area = area
        self.x_point = x_point
        self.y_point = y_point
