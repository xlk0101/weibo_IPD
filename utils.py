import os
import pickle


def check_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def pickle_save(items, path):
    pickle.dump(items, open(path, 'wb'))


def pickle_load(path):
    return pickle.load(open(path, 'rb'))


def dict_add(dic, dic_str):
    if dic.get(dic_str) is not None:
        dic[dic_str] += 1
    else:
        dic[dic_str] = 1
    return dic
