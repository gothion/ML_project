# coding=utf8


def filter_old_item_impl(base_file, next_file, out_file):
    pid_set = set([])
    with open(base_file) as input_base:
        for line in input_base:
            line_arr = line.split(',')
            pid_set.add(line_arr[0])
    with open(next_file) as input_source:
        with open(out_file, 'w') as output_data:
            for line in input_source:
                pid = line.split(',')[0]
                if pid not in pid_set:
                    output_data.write('{0}\n'.format(line))


def filter_old_item(base_file, next_file):
    out_put_file_name = next_file + '_filter'
    filter_old_item_impl(base_file, next_file, out_put_file_name)

if __name__ == '__main__':
    filter_old_item('/Users/galois/Downloads/search_data/星空', 'xingkong.csv')