# coding=utf8
from ml_project.picture_search import result_compare

cate_object_map = {
    '动漫': '6015',
    '汽车': '6012',
    '宠物': '200',
    '运动': '1005',
    '搭配': '3002001',
    # '摄影': '',
    # '明星': '',

}

english_cate_object_map = {
    'astronomy': '10061',
    'cartoon': '6015',
    'decoration': '6005',
    'handsome': '3005001',
    'kid': '300401',
    'plant': '700',
    'sport': '1005',
    'wedding': '6019002'
}

to_be_looked_cate_arr = ['astronomy', 'cartoon', 'decoration', 'handsome', 'kid', 'plant', 'sport', 'wedding']
searched_objects_map = ['动漫', '汽车','宠物', '运动', '搭配',]
out_file_suffix = '_recognized.csv'


def extract_recognized_files(input_file):
    extract_recognized_files_impl(input_file, cate_object_map, searched_objects_map)


def extract_recognized_files_impl(input_file, input_map, input_category_arr):
    cate_index = 4

    object_file_map = {}
    for object_name in input_category_arr:
        if object_name in input_map:
            if object_name not in object_file_map:
                object_file_map[object_name] = open(object_name + out_file_suffix, 'w')
    with open(input_file) as input_data:
        for line in input_data:
            line_arr = line.split('\t')
            recognized_cate = line_arr[cate_index]
            for object_name in input_category_arr:
                if object_name in input_map:
                    cate_arr = input_map[object_name].split(',')
                    for cate in cate_arr:
                        if recognized_cate.startswith(cate):
                            object_file_map[object_name].write(line)
                            continue

    for object_name, out_file in object_file_map.iteritems():
        out_file.close


def extract_english_cate_files(input_file):
    extract_recognized_files_impl(input_file, english_cate_object_map, to_be_looked_cate_arr)


def extract_extra_file():
    for object_name in searched_objects_map:
        if object_name in cate_object_map:
            source_file = object_name + out_file_suffix
            input_file = object_name + '.csv_uniq'
            result_compare.filter_old_item(source_file, input_file, input_sep='\t')


def get_extract_score_b():
    for object_name in to_be_looked_cate_arr:
        if object_name in english_cate_object_map:
            source_file = object_name + out_file_suffix
            out_put_file = object_name + '_kept.csv'
            out_put_with_url = out_put_file + '_with_url'
            result_compare.filter_in_items(source_file, 'MutiLabel_BigData.txt', out_put_file,
                                           [5], input_sep='\t', output_sep='\t')
            result_compare.filter_in_items('photo_url.txt', out_put_file, out_put_with_url,
                                           [1], input_sep=',', output_sep='\t')

if __name__ == '__main__':
    extract_recognized_files('photo_text_cate.csv')
    # extract_english_cate_files('photo_text_cate.csv')
    extract_extra_file()
    # get_extract_score_b()
