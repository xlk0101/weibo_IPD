import pandas as pd
import calendar
import os
import config
import utils
from tqdm import tqdm

# init params
fileConfig = config.FileConfig()
comConfig = config.CommonConfig()


class feature_extraction(object):
    def read_train_data(self, file_path):
        # test = open(file_path).readlines()
        # pass
        data = pd.read_csv(file_path)
        # data.columns = [comConfig.col_uid, comConfig.col_mid, comConfig.col_time, comConfig.col_forward_count,
        #                 comConfig.col_comment_count, comConfig.col_like_count, comConfig.col_content]
        data[comConfig.col_cache] = 0
        data.loc[:, [comConfig.col_cache]] = data[comConfig.col_uid]
        # data = data.set_index(comConfig.col_mid)
        return data

    def read_predict_data(self, file_path):
        data = pd.read_table(file_path, header=None)
        data.columns = [comConfig.col_uid, comConfig.col_mid, comConfig.col_time, comConfig.col_content]
        data = data.set_index(comConfig.col_mid)
        return data

    def read_test_data(self, file_path=None):
        data = pd.read_csv(file_path)
        # data.columns = [comConfig.col_uid, comConfig.col_mid, comConfig.col_time, comConfig.col_forward_count,
        #                 comConfig.col_comment_count, comConfig.col_like_count, comConfig.col_content]
        data[comConfig.col_cache] = 0
        data.loc[:, [comConfig.col_cache]] = data[comConfig.col_uid]
        # data = data.set_index(comConfig.col_mid)
        return data

    def get_Dict(self, data):
        if os.path.exists(fileConfig.pickle_dir + fileConfig.file_train_user_dict_pkl):
            print("Dict:用户ID-该用户的微博条数——总转发——总评论——总赞数,准备完毕！")
            return utils.pickle_load(fileConfig.pickle_dir + fileConfig.file_train_user_dict_pkl)
        else:
            User_Id_Set = set(list(data[comConfig.col_uid]))
            Dict = {}
            for item in list(User_Id_Set):
                Dict[item] = [0, 0, 0, 0]  # 该用户的微博条数 总转发 总评论 总赞数
            for index, item in tqdm(data.iterrows(), "calc user num"):
                user_id = item[comConfig.col_uid]
                if user_id in User_Id_Set:
                    user_list = Dict[user_id]
                    user_list[0] = user_list[0] + 1
                    user_list[1] = user_list[1] + item[comConfig.col_forward_count]
                    user_list[2] = user_list[2] + item[comConfig.col_comment_count]
                    user_list[3] = user_list[3] + item[comConfig.col_like_count]
            utils.check_dir(fileConfig.pickle_dir)
            utils.pickle_save(Dict, fileConfig.pickle_dir + fileConfig.file_train_user_dict_pkl)
            print("Dict:用户ID-该用户的微博条数——总转发——总评论——总赞数,准备完毕！")
            return Dict

    def build_feature(self, data, user_dict, mblog_dict):

        def get_Length(strr):
            strr = str(strr)
            return len(strr)

        def getMonthdays(yeartemp):  # 返回xxxx年的所有的工作日，不考虑节假日，只按照周末计算
            work_day_list = []
            c = calendar.TextCalendar()
            for ii in range(1, 13):
                message = ""
                message = message + str(ii) + "=["
                for week in c.monthdayscalendar(yeartemp, ii):
                    for i in range(0, 5):
                        if week[i] != 0:
                            message = message + str(week[i])
                            date = ii * 100 + (week[i])
                            work_day_list.append(date)
            return (work_day_list)

        def whe_work_day(str, list_work_day):
            whe_work_day = 0
            set_work_day = set(list_work_day)
            date = str.strip().split()[0].split('-')  # 2016-12-21
            new_date = int(date[1]) * 100 + int(date[2])
            if new_date in set_work_day: whe_work_day = 1
            return whe_work_day

        def whe_worktime(str):
            whe_work_time = 0
            time = int(str.strip().split()[1].split(':')[0])  # 10:22:56
            if (time >= 8 & time <= 12) or (time >= 14 & time <= 18): whe_work_time = 1
            return whe_work_time

        def get_average_ZPZ(user_dict, mblog_dict, data):
            def fill_with_cache(dict, x):
                if x in dict:
                    list = dict[x]
                    st = str(list[0]) + " " + str(list[1]) + " " + str(list[2]) + " " + str(list[3])
                else:
                    st = "0 0 0 0"
                return st

            def fill_mblog(dict, x):
                if x in dict:
                    st = str(dict[x][0])
                else:
                    st = "0"
                return st

            def get_zhuanfa(x):
                if int(int(x.strip().split()[0])) != 0:
                    num = int(x.strip().split()[0])
                    zhuanfa = int(x.strip().split()[1])
                    return zhuanfa / (num * 1.0)
                else:
                    return 0

            def get_pinglun(x):
                if int(x.strip().split()[0]) != 0:
                    num = int(x.strip().split()[0])
                    pinglun = int(x.strip().split()[2])
                    return pinglun / (num * 1.0)
                else:
                    return 0

            def get_zan(x):
                if int(x.strip().split()[0]) != 0:
                    num = int(x.strip().split()[0])
                    zan = int(x.strip().split()[3])
                    return zan / (num * 1.0)
                else:
                    return 0

            def get_guanzhudu(x):
                if int(x.strip().split()[0]) != 0:
                    guanzhudu = int(x.strip().split()[3]) + int(x.strip().split()[2]) + int(x.strip().split()[1])
                    return guanzhudu
                else:
                    return 0

            def get_huoyuedu(x):
                if int(x.strip().split()[0]) != 0:
                    huoyuedu = int(x.strip().split()[0])
                else:
                    huoyuedu = 0
                return huoyuedu

            new_feature_one = [comConfig.col_past_avg_forward, comConfig.col_past_avg_comment,
                               comConfig.col_past_avg_like, comConfig.col_attention, comConfig.col_active,
                               comConfig.col_mblog_count]
            for item in new_feature_one:
                data[item] = 0
            data[comConfig.col_cache] = 0
            data.loc[:, [comConfig.col_cache]] = data[comConfig.col_uid].map(lambda x: fill_with_cache(user_dict, x))
            data.loc[:, [comConfig.col_mblog_count]] = data[comConfig.col_mid].map(lambda x: fill_mblog(mblog_dict, x))
            data.loc[:, [comConfig.col_past_avg_forward]] = data[comConfig.col_cache].map(lambda x: get_zhuanfa(x))
            data.loc[:, [comConfig.col_past_avg_comment]] = data[comConfig.col_cache].map(lambda x: get_pinglun(x))
            data.loc[:, [comConfig.col_past_avg_like]] = data[comConfig.col_cache].map(lambda x: get_zan(x))
            data.loc[:, [comConfig.col_attention]] = data[comConfig.col_cache].map(lambda x: get_guanzhudu(x))
            data.loc[:, [comConfig.col_active]] = data[comConfig.col_cache].map(lambda x: get_huoyuedu(x))
            return data

        def whe_link(strr):
            strr = str(strr)
            k = 0
            if 'http:' in strr: k = 1
            return k

        def whe_title(strr):
            strr = str(strr)
            k = 0
            for item in '[#【《](.*?)[#】》]':
                if item in strr:
                    k = 1
                    break
            return k

        def whe_emoji(strr):
            strr = str(strr)

            def isEmoji(content):
                if not content:
                    return False
                if u"\U0001F600" <= content and content <= u"\U0001F64F":
                    return True
                elif u"\U0001F300" <= content and content <= u"\U0001F5FF":
                    return True
                elif u"\U0001F680" <= content and content <= u"\U0001F6FF":
                    return True
                elif u"\U0001F1E0" <= content and content <= u"\U0001F1FF":
                    return True
                else:
                    return False

            k = 0
            for item in strr:
                if isEmoji(item):
                    k = 1
                if k == 1: break
            return k

        def whe_art(strr):
            strr = str(strr)
            k = 0
            if '@' in strr: k = 1
            return k

        print("开始建立特征！")
        data = get_average_ZPZ(user_dict, mblog_dict, data)
        all_work_day_list = getMonthdays(2015)
        list_holiday = [101, 102, 103, 218, 219, 220, 221, 222, 223, 404, 405, 406, 501, 502, 503, 620, 621, 622, 926,
                        927, 928, 1001, 1002, 1003, 1004, 1005, 1006, 1007]
        all_work_day_list = list(set(all_work_day_list) - set(list_holiday))
        new_feature_two = [comConfig.col_is_work_day, comConfig.col_is_work_time]
        for item in new_feature_two:
            data[item] = 0
        data[comConfig.col_is_work_day] = data[comConfig.col_time].map(lambda x: whe_work_day(x, all_work_day_list))
        data[comConfig.col_is_work_time] = data[comConfig.col_time].map(lambda x: whe_worktime(x))
        new_feature_three = [comConfig.col_has_link, comConfig.col_has_title, comConfig.col_has_emoj,
                             comConfig.col_has_at, comConfig.col_text_len]
        for item in new_feature_three:
            data[item] = 0
        data.loc[:, [comConfig.col_has_link]] = data[comConfig.col_content].map(lambda x: whe_link(x))
        data.loc[:, [comConfig.col_has_title]] = data[comConfig.col_content].map(lambda x: whe_title(x))
        data.loc[:, [comConfig.col_has_emoj]] = data[comConfig.col_content].map(lambda x: whe_emoji(x))
        data.loc[:, [comConfig.col_has_at]] = data[comConfig.col_content].map(lambda x: whe_art(x))
        data.loc[:, [comConfig.col_text_len]] = data[comConfig.col_content].map(lambda x: get_Length(x))
        return data


if __name__ == '__main__':
    fe = feature_extraction()
    train_data = fe.read_train_data(fileConfig.csv_dir + fileConfig.file_train_pandas)
    # predict_data = fe.read_predict_data(fileConfig.data_dir + fileConfig.file_weibo_predict_data)
    test_data = fe.read_test_data(fileConfig.csv_dir + fileConfig.file_test_pandas)
    user_dict = fe.get_Dict(train_data)
    mblog_dict = utils.pickle_load(fileConfig.pickle_dir + fileConfig.file_train_mblog_dict_pkl)
    # print(dict)
    print("start create train feature...")
    train_data_updated = fe.build_feature(train_data, user_dict, mblog_dict)
    print("start create test feature...")
    # predict_data_updated = fe.build_feature(predict_data, dict)
    test_data_updated = fe.build_feature(test_data, user_dict, mblog_dict)
    # dict_dataframe=pd.DataFrame(dict).T
    # dict_dataframe.columns=['总数量','总转发','总评论','总赞']
    # dict_dataframe.to_csv('dict_pandas.csv')

    utils.check_dir(fileConfig.csv_dir)
    train_data_updated.to_csv(fileConfig.csv_dir + fileConfig.file_fe_train)
    # predict_data_updated.to_csv(fileConfig.csv_dir + fileConfig.file_fe_predict)
    test_data_updated.to_csv(fileConfig.csv_dir + fileConfig.file_fe_test)
