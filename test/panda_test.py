# coding=utf8

import pandas as pd
import os

this_dir, this_filename = os.path.split(__file__)
data_folder = os.path.normpath(os.path.join(this_dir, '..', 'data'))
result_folder = os.path.normpath(os.path.join(this_dir, '..', 'test_result'))

photo_url_info = pd.DataFrame(pd.read_csv(data_folder + '/' + 'vechile_photo_url.csv', header=None).get_values(),
                              columns=['cate_a', 'photo_id', 'score_a', 'score_b', 'photo_url'])
result_info = pd.DataFrame(pd.read_csv(result_folder + '/' + 'result3.test.txt', header=None).get_values(),
                           columns=['photo_id', 'score', 'vector_info'])
final_result = pd.merge(photo_url_info, result_info, on='photo_id', how='inner')
cols_to_keep = ['photo_id', 'score', 'photo_url']
final_result[cols_to_keep].to_csv(result_folder + '/' + 'result.test.txt_url', encoding='utf8', header=False)

