from sklearn import metrics
import pandas as pd
from sklearn.metrics import fbeta_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import shuffle
import config
import evaluate

# init params
fileConfig = config.FileConfig()
comConfig = config.CommonConfig()


def get_precol_name(col_name):
    if col_name == comConfig.col_forward_count:
        return comConfig.col_pre_forward_count
    elif col_name == comConfig.col_comment_count:
        return comConfig.col_pre_comment_count
    elif col_name == comConfig.col_like_count:
        return comConfig.col_pre_like_count


def train_model():
    print("start train model...")
    train_df = pd.read_csv(fileConfig.csv_dir + fileConfig.file_fe_train)
    test_df = pd.read_csv(fileConfig.csv_dir + fileConfig.file_fe_test)
    target = [comConfig.col_forward_count, comConfig.col_comment_count, comConfig.col_like_count]
    dropped_train_dataset = [comConfig.col_mid, comConfig.col_uid, comConfig.col_time, comConfig.col_forward_count,
                             comConfig.col_comment_count, comConfig.col_like_count, comConfig.col_content,
                             comConfig.col_cache, 'Unnamed: 0']
    dropped_predict_datastet = [comConfig.col_mid, comConfig.col_uid, comConfig.col_time, comConfig.col_content,
                                comConfig.col_cache]
    predictors = [x for x in train_df.columns if x not in target + dropped_train_dataset]
    for item in target:
        test_df[item] = 0
    print("use random forest regressor to find the right count...")
    for i in range(len(target)):
        print("start train {} model".format(target[i]))
        rf = RandomForestRegressor()  # 这里使用了默认的参数设置
        rf.fit(train_df[predictors], train_df[target[i]])  # 进行模型的训练
        predict_df_predictions = rf.predict(test_df[predictors])
        predict_df_predictions = [int(item) for item in predict_df_predictions]
        test_df[get_precol_name(target[i])] = predict_df_predictions
        # print(test_df[target[i]])
    forward_precisions = evaluate.calc_forward_dev(test_df[comConfig.col_forward_count],
                                                   test_df[comConfig.col_pre_forward_count])
    comment_precisions = evaluate.calc_comment_dev(test_df[comConfig.col_comment_count],
                                                   test_df[comConfig.col_pre_comment_count])
    like_precisions = evaluate.calc_like_dev(test_df[comConfig.col_like_count], test_df[comConfig.col_pre_like_count])
    single_precisions = evaluate.single_precision(forward_precisions, comment_precisions, like_precisions)
    print("the test precision is:{}".format(
        evaluate.all_precision(test_df[comConfig.col_mblog_count], single_precisions)))

    # result = predict_df.loc[:, ['微博ID', '用户ID', '转发', '评论', '赞']]
    # # result.columns=['uid','mid','forward_count','comment_count','like_count']
    # result.to_csv('result.csv')


if __name__ == '__main__':
    train_model()
