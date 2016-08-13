# coding=utf8
import numpy as np

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import confusion_matrix


# def train_and_predict(x_data, y_data, train_num=350):
#     length = len(x_data)
#     indices = np.arange(length)
#     rng = np.random.RandomState(0)
#     rng.shuffle(indices)
#     x_train = x_data[indices[:train_num]]
#     y_train = y_data[indices[:train_num]]
#     x_test = x_data[indices[train_num+1:]]
#     y_test = y_data[indices[train_num+1:]]
#     rfc = RandomForestClassifier(n_estimators=5)
#     rfc.fit(x_train, y_train)
#     result = rfc.predict(x_test)
#     cm = confusion_matrix(y_test, rfc.predict(x_test), labels=rfc.classes_)
#     print cm


def read_sample(sample_label, sample_file_path, version=0):
    X = []
    Y = []
    with open(sample_file_path, mode='r') as samples:
        for line in samples:
            if version == 0:
                X.append(extract_feature(line))
            else:
                X.append(extract_feature_version1(line))
            Y.append(sample_label)
    return np.array(X), np.array(Y)


def extract_feature_version1(sample_line):
    object_part = sample_line.split(' ')[0]
    label_info = extract_object_info(object_part)
    label_num_index_arr = [0, 2, 4]
    object_num = 0.0
    for label_index in label_num_index_arr:
        object_num += label_info[label_index]
    for label_index in label_num_index_arr:
        label_info[label_index] /= object_num
    return [float(object_num)] + label_info


def extract_feature(sample_line):
    the_index = index_of_char(sample_line, ',', 2)
    fore_part_sample = sample_line[:the_index]
    object_num = int(fore_part_sample.split(',')[1])
    object_part = sample_line[the_index+1:]
    label_info = extract_object_info(object_part, object_num)
    label_num_index_arr = [0, 2, 4]
    for label_index in label_num_index_arr:
        label_info[label_index] /= object_num
    return [float(object_num)] + label_info


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

if __name__ == '__main__':
    x_data1, y_data1 = read_sample(1, '/Users/galois/code/python/ML_project/data/good', version=1)
    x_data2, y_data2 = read_sample(0, '/Users/galois/code/python/ML_project/data/bad', version=1)
    indices = np.arange(800)
    x_data2 = x_data2[indices]
    y_data2 = y_data2[indices]
    x_data = np.concatenate((x_data1, x_data2))
    y_data = np.concatenate((y_data1, y_data2))
    print len(x_data)
    print len(y_data)
    # train_and_predict(x_data, y_data)
