# coding=utf8

# coding=utf8

import pandas as pd
import os

this_dir, this_filename = os.path.split(__file__)
data_folder = os.path.normpath(os.path.join(this_dir, '..', 'data'))
result_folder = os.path.normpath(os.path.join(this_dir, '..', 'test_result'))

photo_url_info = pd.DataFrame(pd.read_csv(data_folder + '/' + 'vechile_photo_url.csv', header=None).get_values(),
                              columns=['cate_a', 'photo_id', 'score_a', 'score_b', 'photo_url'])


def get_result_data(input_data):
    return result_folder + '/' + input_data


def get_input_data(input_data):
    return data_folder + '/' + input_data


# ['photo_id', 'score', 'vector_info']
# cols_to_keep = ['photo_id', 'score', 'photo_url']
def get_url_info_by_id(input_file_path, output_file_path, input_columns,
                       cols_to_keep=['photo_id', 'score', 'photo_url']):
    result_info = pd.DataFrame(pd.read_csv(input_file_path, header=None).get_values(),
                               columns=input_columns)
    final_result = pd.merge(photo_url_info, result_info, on='photo_id', how='inner')
    final_result[cols_to_keep].to_csv(output_file_path, encoding='utf8', header=False)
