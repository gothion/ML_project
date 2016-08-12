# coding=utf8
def read_sample(sample_label, sample_file_path):
    with open(sample_file_path, mode='r') as samples:
        X = []
        Y = []
        for line in samples:
            X.append(extract_feature(line))
            Y.append(sample_label)


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


def extract_object_info(object_part, object_num):
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
    test()