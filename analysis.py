import config
import pandas as pd
import utils
from collections import Counter
from tqdm import tqdm

# init params
fileConfig = config.FileConfig()
comConfig = config.CommonConfig()


def analysis_train_pandas():
    train_df = pd.read_csv(fileConfig.csv_dir + fileConfig.file_train_pandas)
    print("forward describe...")
    print(train_df[comConfig.col_forward_count].describe())
    print("comment describe...")
    print(train_df[comConfig.col_comment_count].describe())
    print("like describe...")
    print(train_df[comConfig.col_like_count].describe())


def analysis_train_data():
    train_data = open(fileConfig.data_dir + fileConfig.file_weibo_train_data, "r", encoding="utf-8")
    user_dict = {}
    for line in tqdm(train_data, 'count user...'):
        train_infos = line.split('\t')
        utils.dict_add(user_dict, train_infos[0])
    print("the user infos...")
    print(len(user_dict))
    print(Counter(user_dict).most_common())


def analysis_user_info():
    train_datas = open(fileConfig.data_dir + fileConfig.file_weibo_train_data, "r", encoding="utf-8")
    pre_datas = open(fileConfig.data_dir + fileConfig.file_weibo_predict_data, "r", encoding="utf-8")
    train_user_dict = {}
    pre_user_dict = {}
    unkown_user_list = []
    for line in tqdm(train_datas, "deal train data"):
        train_infos = line.split("\t")
        utils.dict_add(train_user_dict, train_infos[0])
    print(len(train_user_dict))
    for line in tqdm(pre_datas, "deal pre datas"):
        pre_infos = line.split("\t")
        utils.dict_add(pre_user_dict, pre_infos[0])
        if train_user_dict.get(pre_infos[0]) is None:
            unkown_user_list.append(pre_infos[0])
    print("the pre user is {}".format(len(pre_user_dict)))
    print("find unkown user {} ratio is {}".format(len(unkown_user_list), len(unkown_user_list) / len(pre_user_dict)))


if __name__ == '__main__':
    # analysis_train_pandas()
    # analysis_train_data()
    analysis_user_info()
