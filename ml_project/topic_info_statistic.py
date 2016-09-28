# coding=utf8
from matplotlib import pyplot as plt
import operator
import math


def statistic_info(input_file_name, first_field_column_index, second_field_column_index,
                   count_column_index, file_sep='\t'):
    static_info_list = []
    static_info_arr = {}
    with open(input_file_name) as input_file:
        for line in input_file:
            line_arr = line.split(file_sep)
            first_field = line_arr[first_field_column_index]
            if first_field not in static_info_arr:
                static_info_arr[first_field] = [[line_arr[second_field_column_index],
                                                line_arr[count_column_index]]]
            else:
                static_info_arr[first_field].append([line_arr[second_field_column_index],
                                                     line_arr[count_column_index]])
    for k, v in static_info_arr.iteritems():
        total_count = 0
        max_num = 0
        max_sign = ''
        for item_info_arr in v:
            second_column = item_info_arr[0]
            count = item_info_arr[1]
            total_count += int(count)
            if int(count) >= max_num:
                max_sign = second_column
                max_num = int(count)
        # print 'tag name is {0}, total_count is {1}, max_sign is {2} and max_num is {3} '\
        #     .format(k, total_count, max_sign, max_num)
        static_info_list.append([k, total_count, max_sign, max_num])
    return static_info_list


def plot_hist(static_info_list):
    sign_arr_map = {}
    for k, total_count, max_sign, max_num in static_info_list:
        if max_sign not in sign_arr_map:
            sign_arr_map[max_sign] = []
        sign_arr_map[max_sign].append([k, total_count, max_sign, max_num])
    for k, v in sign_arr_map.iteritems():
        plot_hist_impl(v)


def plot_hist_impl(static_info_list):
    total_arr = [(2.0+a_info[3])/(a_info[1]+4.0) for a_info in static_info_list]
    total_k_arr = [[a_info[0], a_info[2], a_info[1], (2.0+a_info[3])/(a_info[1]+4.0), a_info[3]] for a_info in static_info_list]
    h_prob = [[k, attribute, total_num, -1 * prob * math.log(prob) - (1 - prob) * math.log(1 - prob), max_num]
              for k, attribute, total_num, prob, max_num in total_k_arr]
    h_prob_sorted = sorted(h_prob, key=operator.itemgetter(3))
    for k, attribute, total_num, v, max_num in h_prob_sorted:
        if v < 0.6 and k != '男'  :
            print attribute, total_num, max_num, v, k
    h_prob = [-1 * prob * math.log(prob) - (1-prob)*math.log(1-prob) for prob in total_arr]

    # fig = plt.figure()
    # ax1 = fig.add_subplot(2, 1, 1)
    # ax2 = fig.add_subplot(2, 1, 2)
    #
    # n, bins, patch = ax1.hist(total_arr, bins=20)
    # print n, bins, patch
    # ax1.set_xlabel('total_arr')
    # ax1.set_ylabel('probality')
    #
    # n, bins, patch = ax2.hist(h_prob, bins=20)
    # print n, bins, patch
    # ax2.set_xlabel('h_prob dist')
    # ax2.set_ylabel('information')
    # # plt.hist(total_arr, bins=20)
    # # plt.hist(h_prob)
    # plt.show()


if __name__ == '__main__':
    file_name='/home/galois/code/shell/topic_gender_info.txt'
    info_list = statistic_info(file_name, 1, 2, 3)
    plot_hist(info_list)


