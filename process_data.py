import config
import utils
import pandas as pd
from tqdm import tqdm

# init params
fileConfig = config.FileConfig()
comConfig = config.CommonConfig()


def create_train_pickle():
    print("start create train pickle file...")
    train_data = open(fileConfig.data_dir + fileConfig.file_weibo_train_data, "r", encoding="utf-8")
    out_datas = []
    for line in tqdm(train_data, "deal train file..."):
        train_infos = line.split('\t')
        assert len(train_infos) == 7
        out_datas.append(
            {comConfig.col_uid: train_infos[0], comConfig.col_mid: train_infos[1], comConfig.col_time: train_infos[2],
             comConfig.col_forward_count: train_infos[3],
             comConfig.col_comment_count: train_infos[4], comConfig.col_like_count: train_infos[5],
             comConfig.col_content: train_infos[6]})
    print("save train and test infos...")
    test_data_len = 200000
    train_datas = out_datas[:len(out_datas) - test_data_len]
    test_datas = out_datas[len(out_datas) - test_data_len:]
    utils.check_dir(fileConfig.pickle_dir)
    utils.pickle_save(train_datas, fileConfig.pickle_dir + fileConfig.file_train_pickle)
    utils.pickle_save(test_datas, fileConfig.pickle_dir + fileConfig.file_test_pickle)


def create_pandas_file(input_file, output_file):
    print("start create train pandas file {}...".format(input_file))
    train_data = open(input_file, "r", encoding="utf-8")
    uid_list = []
    mid_list = []
    time_list = []
    forward_count_list = []
    like_count_list = []
    comment_count_list = []
    content_list = []
    for line in tqdm(train_data, "create csv..."):
        train_infos = line.split('\t')
        assert len(train_infos) == 7
        uid_list.append(train_infos[0])
        mid_list.append(train_infos[1])
        time_list.append(train_infos[2])
        forward_count_list.append(train_infos[3])
        comment_count_list.append(train_infos[4])
        like_count_list.append(train_infos[5])
        content_list.append(train_infos[6])
    utils.check_dir(fileConfig.csv_dir)
    pandas_dict = {comConfig.col_uid: uid_list, comConfig.col_mid: mid_list, comConfig.col_time: time_list,
                   comConfig.col_forward_count: forward_count_list,
                   comConfig.col_comment_count: comment_count_list, comConfig.col_like_count: like_count_list,
                   comConfig.col_content: content_list}
    df = pd.DataFrame.from_dict(pandas_dict)
    df.to_csv(output_file)
    print("success create train pandas data file {}".format(output_file))


def create_train_test_file():
    print("start create train/test txt file...")
    train_file = open(fileConfig.data_dir + fileConfig.file_weibo_train_data)
    out_train_txt = open(fileConfig.data_dir + fileConfig.file_train_txt, "w", encoding="utf-8")
    out_test_txt = open(fileConfig.data_dir + fileConfig.file_test_txt, "w", encoding="utf-8")
    train_datas = train_file.readlines()
    train_data_len = len(train_datas)
    test_data_len = 20000
    save_train_datas = train_datas[:train_data_len - test_data_len]
    save_test_datas = train_datas[train_data_len - test_data_len:]
    count = 0
    for line in save_train_datas:
        # count += 1
        # if count < 1205179:
        #     continue
        # if len(line.strip("")) == 0:
        #     continue
        result = ""
        for text in line.split("\t"):
            result += text.strip("").strip("\n") + "\t"
        out_train_txt.write(result[0:len(result) - 1])
        out_train_txt.write("\n")
    for line in save_test_datas:
        if len(line.strip("")) == 0:
            continue
        result = ""
        for text in line.split("\t"):
            result += text.strip("").strip("\n") + "\t"
        out_test_txt.write(result[0:len(result) - 1])
        out_test_txt.write("\n")
    print("success create train/test txt file!")


def create_mblog_dict():
    print("start create mblog dict")
    train_datas = open(fileConfig.data_dir + fileConfig.file_weibo_train_data, "r", encoding="utf-8")
    out_datas = []
    mblog_id_set = set()
    for line in tqdm(train_datas, "deal train datas..."):
        train_infos = line.split('\t')
        assert len(train_infos) == 7
        mblog_id_set.add(train_infos[1])
        out_datas.append(
            {comConfig.col_uid: train_infos[0], comConfig.col_mid: train_infos[1], comConfig.col_time: train_infos[2],
             comConfig.col_forward_count: train_infos[3],
             comConfig.col_comment_count: train_infos[4], comConfig.col_like_count: train_infos[5],
             comConfig.col_content: train_infos[6]})
    Dict = {}
    for item in list(mblog_id_set):
        Dict[item] = [0]  # 该博文的 总转发 + 总评论 + 总赞数
    for index, item in tqdm(enumerate(out_datas), "calc mblog num"):
        mblog_id = item[comConfig.col_mid]
        if mblog_id in mblog_id_set:
            user_list = Dict[mblog_id]
            user_list[0] = user_list[0] + int(item[comConfig.col_forward_count])
            user_list[0] = user_list[0] + int(item[comConfig.col_comment_count])
            user_list[0] = user_list[0] + int(item[comConfig.col_like_count])
    utils.check_dir(fileConfig.pickle_dir)
    utils.pickle_save(Dict, fileConfig.pickle_dir + fileConfig.file_train_mblog_dict_pkl)
    print("Dict:博文ID-该博文的总转发+总评论+总赞数,准备完毕！")


if __name__ == '__main__':
    # create_train_pickle()
    # create_train_pandas()
    # create_train_test_file()
    create_pandas_file(fileConfig.data_dir + fileConfig.file_train_txt,
                       fileConfig.csv_dir + fileConfig.file_train_pandas)
    create_pandas_file(fileConfig.data_dir + fileConfig.file_test_txt,
                       fileConfig.csv_dir + fileConfig.file_test_pandas)
    # create_mblog_dict()
