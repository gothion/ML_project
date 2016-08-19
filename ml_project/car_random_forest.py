# coding=utf8
import numpy as np
import os
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt
from ml_project import data_combiner

this_dir, this_filename = os.path.split(__file__)
data_folder = os.path.normpath(os.path.join(this_dir, '..', 'data'))
out_put_folder = os.path.normpath(os.path.join(this_dir, '..', 'test_result'))
object_info_sep = ';'
object_field_sep = ','
white_list = ['other.text', 'other.sticker', 'other.log']


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


def read_sample(sample_label, sample_file_path):
    X = []
    Y = []
    with open(sample_file_path, mode='r') as samples:
        for line in samples:
            feature_vector = extract_feature(line)
            if feature_vector[3] > 0.10:
                X.append(feature_vector)
                Y.append(sample_label)
    return np.array(X), np.array(Y)


def extract_feature(sample_line):
    line_arr = sample_line.split('\t')

    object_num = int(line_arr[3])
    object_part = line_arr[4]
    label_info = extract_object_info(object_part, object_num)
    quality = float(line_arr[-1])
    object_info_list = get_object_info_list(object_part)
    is_car_blocked = is_car_overlapped(object_info_list)
    if is_car_blocked:
        return label_info + [quality] + [1]
    return label_info + [quality] + [0]

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
    if object_sign == 'other.other':
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
    x_data1 = np.tile(x_data3, (3, 1))
    y_data1 = np.tile(y_data3, 3)
    # x_data1 = x_data3
    # y_data1 = y_data3

    x_data = np.concatenate((x_data1, x_data2))
    y_data = np.concatenate((y_data1,  y_data2))
    precision, model = train_and_predict(x_data, y_data)
    return precision, model


def prediction_with_model(model, out_put_file, input_data_path):
    to_be_predicted = read_predicted_line(input_data_path)
    with open(out_put_file, mode='w') as out_put_data:
        with open(out_put_file + "_v2", mode='w') as output_data_v2:
            with open(out_put_file + "_v3", mode='w') as output_data_v3:
                for photo_id, (vector_info, raw_line) in to_be_predicted.iteritems():
                    new_vector_info = vector_info.reshape(1, -1)
                    prediction_result = model.predict_proba(new_vector_info)[0][1]
                    if prediction_result >= 0.5 and vector_info[3] > 0.10\
                            and vector_info[7] == 0 and not is_car_only_part(raw_line):
                        out_put_data.write(photo_id + ',' + str(prediction_result) + ',' + str(vector_info) + '\n')
                    if vector_info[6] >= 0.98 and vector_info[7] == 0 and not is_car_only_part(raw_line):
                        output_data_v2.write(photo_id + ',' + str(vector_info[6]) + ',' + str(vector_info) + '\n')
                        output_data_v3.write(photo_id + ',' + str(vector_info[6]) + ',' + str(vector_info) + '\n')
                    elif vector_info[6] >= 0.75 and prediction_result > 0.45 \
                            and vector_info[3] > 0.10 and vector_info[7] == 0 and not is_car_only_part(raw_line):
                        output_data_v2.write(photo_id + ',' + str(vector_info[6]) + ',' + str(vector_info) + '\n')
                        output_data_v3.write(photo_id + ',' + str(vector_info[6]) + ',' + str(vector_info) + '\n')
                    elif vector_info[6] >= 0.40 and prediction_result > 0.65 \
                            and vector_info[3] > 0.10 and vector_info[7] == 0 and not is_car_only_part(raw_line):
                        output_data_v3.write(photo_id + ',' + str(vector_info[6]) + ',' + str(vector_info) + '\n')

    # total_out_file = out_put_file+"_total"
    # with open(total_out_file, mode='w') as out_total:
    #     for photo_id, (vector_info, raw_line) in to_be_predicted.iteritems():
    #         out_total.write(photo_id + ',' + str(prediction_result) + ',' + str(is_car_only_part(raw_line)) + '\n')

    data_combiner.get_url_info_by_id(out_put_file, out_put_file+'_with_url',
                                     input_columns=['photo_id', 'score', 'vector_info'])
    data_combiner.get_url_info_by_id(out_put_file + '_v2', out_put_file + '_v2_with_url',
                                     input_columns=['photo_id', 'score', 'vector_info'])
    data_combiner.get_url_info_by_id(out_put_file + '_v3', out_put_file + '_v3_with_url',
                                     input_columns=['photo_id', 'score', 'vector_info'])
    # data_combiner.get_url_info_by_id(total_out_file, total_out_file+'_with_url',
    #                                  input_columns=['photo_id', 'score', 'vector_info'])


def read_predicted_line(file_path):
    picture_dict = {}
    with open(file_path, mode='r') as input_data:
        for line in input_data:
            photo_id = get_picture_id(line)
            picture_dict[photo_id] = (np.array(extract_feature(line)), line)
    return picture_dict


def get_picture_id(line):
    return line.split("\t")[0]


# def is_part_of_car(line):
#     str_vec = line.split('\t')
#     str_vec2 = str_vec[4].split(';')
#     height = int(str_vec[1])
#     width = int(str_vec[2])
#     for i in range(len(str_vec2)):
#         str_vec3 = str_vec2[i].split(',')
#         if 7 != len(str_vec3):
#             continue
#         center_x = (int(str_vec3[2]) + int(str_vec3[4])) / 2
#         center_y = (int(str_vec3[3]) + int(str_vec3[5])) / 2
#         center_x_dist = float(abs(width/2 - center_x)) / width
#         center_y_dist = float(abs(height/2 - center_y)) / height
#
#         if "car" in str_vec3[0] and (float(str_vec3[6]) > 0.36):
#             return True
#         if "other.other" == str_vec3[0] and (float(str_vec3[6]) > 0.8):
#             return True
#         if "car" in str_vec3[0] and (center_x_dist < 0.2 and center_y_dist < 0.2):
#             return True
#         if "car" in str_vec3[0] and (int(str_vec3[2]) > 0 and int(str_vec3[4]) < width and int(str_vec[3]) > 0 and
#                                      int(str_vec3[5]) < height):
#             return True
#     return False


def is_car_only_part(input_line):
    line_arr = input_line.split('\t')
    height = int(line_arr[1])
    width = int(line_arr[2])
    object_part = line_arr[4]
    object_arr = get_object_info_list(object_part)
    for object_info in object_arr:
        if object_info.object_name == 'vehicle.car':
            if object_info.is_part_object(width, height):
                return True
    return False


def get_object_info_list(objects_str):
    object_info_arr = []
    objects_arr = objects_str.split(object_info_sep)[:-1]
    for object_info_str in objects_arr:
        object_field_arr = object_info_str.split(object_field_sep)
        object_name = object_field_arr[0]
        l_x = int(object_field_arr[2])
        l_y = int(object_field_arr[3])
        r_x = int(object_field_arr[4])
        r_y = int(object_field_arr[5])
        object_info_arr.append(ObjectInfo(object_name, l_x, l_y, r_x, r_y))
    return object_info_arr


def is_car_overlapped(object_info_list):
    if len(object_info_list) < 2:
        return False
    for i in range(len(object_info_list)):
        for j in range(len(object_info_list)):
            if i != j:
                if object_info_list[i].object_name == 'vehicle.car' or object_info_list[j].object_name == 'vehicle.car':
                    if object_info_list[i].object_name not in white_list and object_info_list[j].object_name not in \
                            white_list:
                        if object_info_list[i].is_overlap(object_info_list[j]):
                            return True


def test_car_overlapped(objects_str):
    object_info_list = get_object_info_list(objects_str)
    result = is_car_overlapped(object_info_list)
    print result
    return result


class ObjectInfo(object):
    def __init__(self, object_name,
                 l_x, l_y, r_x, r_y):
        self.object_name = object_name
        self.l_x = l_x
        self.l_y = l_y
        self.r_x = r_x
        self.r_y = r_y

    def is_overlap(self, other):
        x_bool = self._is_overlap_1d(self.l_x, self.r_x, other.l_x, other.r_x)
        y_bool = self._is_overlap_1d(self.l_y, self.r_y, other.l_y, other.r_y)
        return x_bool and y_bool

    def get_over_lap_area(self, other):
        if not self.is_overlap(other):
            return 0
        l_x = max(self.l_x, other.l_x)
        l_y = max(self.l_y, other.l_y)
        r_x = min(self.r_x, other.r_x)
        r_y = min(self.r_y, other.r_y)
        return (r_y - l_y) * (l_x - r_x)

    def is_part_object(self, width, height):
        if self.l_x > 0 and self.l_y > 0 and self.r_x < width and self.r_y < height:
            return False
        x_center = (self.l_x + self.r_x)/2.0
        if abs((width/2.0 - x_center))/width < 0.05 and max(self.l_x, width - self.r_x)/width < 0.08 \
                and self.l_y > 0 and self.r_y < height:
            return False
        return True

    @staticmethod
    def _is_overlap_1d(l_1, r_1, l_2, r_2):
        return (l_1 - l_2) * (l_1 - r_2) < 0 or (r_1 - l_2) * (r_1 - r_2) < 0

if __name__ == '__main__':
    precision, model_result = get_model()
    # print precision
    out_put_result = 'result5.test.txt'
    abs_output_path = data_combiner.get_result_data(out_put_result)
    # object_str = 'vehicle.car,0.995,117,325,805,1170,0.4731;person.face,0.991,492,235,610,365,0.0125;'
    # test_car_overlapped(object_str)
    input_data_path = 'car_data_20160817'
    abs_input_data_path = data_combiner.get_input_data(input_data_path)
    input_data_with_score_b = abs_input_data_path + '_with_score_b'
    data_combiner.get_score_b_by_id(abs_input_data_path, input_data_with_score_b,
                                    input_columns=['photo_id', 'width', 'height', 'object_num', 'object_info'])

    prediction_with_model(model_result, abs_output_path, input_data_with_score_b)
