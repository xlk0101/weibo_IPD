class FileConfig(object):
    def __init__(self):
        # dir
        self.base_dir = "/data/py_proj/tianchi_proj/weibo_IPD/"
        self.data_dir = self.base_dir + "data/"
        self.pickle_dir = self.data_dir + "pickle/"
        self.csv_dir = self.data_dir + 'csv/'

        # file
        self.file_weibo_train_data = "weibo_train_data.txt"
        self.file_weibo_predict_data = "weibo_predict_data.txt"
        self.file_train_txt = "train_data.txt"
        self.file_test_txt = "test_data.txt"
        self.file_train_pickle = "train_pickle.pkl"
        self.file_test_pickle = "test_pickle.pkl"
        self.file_train_pandas = "train_data.csv"
        self.file_test_pandas = "test_data.csv"
        self.file_fe_train = 'fe_train.csv'
        self.file_fe_predict = 'fe_predict.csv'
        self.file_fe_test = "fe_test.csv"
        self.file_train_user_dict_pkl = 'train_user_dict.pkl'
        self.file_train_mblog_dict_pkl = "train_mblog_dict.pkl"


class CommonConfig(object):
    def __init__(self):
        self.col_uid = "uid"
        self.col_mid = "mid"
        self.col_time = "time"
        self.col_forward_count = "forward_count"
        self.col_comment_count = "comment_count"
        self.col_like_count = "like_count"
        self.col_pre_forward_count = "pre_forward_count"
        self.col_pre_comment_count = "pre_comment_count"
        self.col_pre_like_count = "pre_like_count"
        self.col_content = "content"
        self.col_cache = 'cache'
        self.col_past_avg_forward = 'past_avg_forward'
        self.col_past_avg_comment = 'past_avg_comment'
        self.col_past_avg_like = 'past_avg_like'
        self.col_attention = 'attention'
        self.col_active = 'active'
        self.col_is_work_day = 'is_work_day'
        self.col_is_work_time = 'is_work_point'
        self.col_has_link = 'has_link'
        self.col_has_title = 'has_title'
        self.col_has_emoj = 'has_emoj'
        self.col_has_at = 'has_at'  # has @
        self.col_text_len = 'text_len'
        self.col_mblog_count = 'mblog_count'
