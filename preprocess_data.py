#coding=utf8

"""
对task2中的特征进行预处理，方法为：将所有的nominal特征转化为categorical，使用One Hot Encoder
判断某个特征是否为nominal特征：该特征全部为正整数
注：在对训练集进行转换的同时，需要将测试集也按照相同的方式转换
"""

import numpy as np
from numpy import genfromtxt
from sklearn.preprocessing import OneHotEncoder

def main():
    train_path = '/home/kqc/dataset/CCDM2014/task2/train_data.csv'
    test_path = '/home/kqc/dataset/CCDM2014/task2/test_feature_data.csv'
    
    train_data = genfromtxt(train_path, delimiter=',')
    test_data = genfromtxt(test_path, delimiter=',')
    
    # 删除test data中的第一列，此列为样本的序号
    test_data = test_data[:, 1:]
    label_train = train_data[:, -1] # 训练集最后一列为标签信息
    train_data = train_data[:, :-1]
    train_count, num_feature = train_data.shape
    # 将训练集和测试集合并
    whole_data = np.vstack((train_data, test_data))
    total, num_feature = whole_data.shape
    
    # 遍历所有的特征
    nominal_feature_index = []
    for i in range(num_feature):
        s = whole_data[:, i]
        # 特殊处理第400个和第407个特征
        if i == 400:
            s = s / 25
            whole_data[:, i] = s
        elif i == 407:
            s = s / 20
            whole_data[:, i] = s
        
        flag = False
        for j in range(total):
            if s[j] < 0 or int(s[j]) != s[j]:
                # 此列为numeric特征，可忽略
                flag = True
                break
        if flag:
            continue
        # s中只有0，不考虑
        elif max(s) == 0:
            continue
        # 如果该特征只有0和1两个取值，则同样不考虑
        elif min(s) == 0 and max(s) == 1:
            continue
        else:  
            nominal_feature_index.append(i)
            
    nominal_feature = np.array(whole_data[:, nominal_feature_index], dtype=int)
    # 在原始数据中删除nominal特征列
    numeric_feature = np.delete(whole_data, nominal_feature_index, 1)
    # 转换数据
    enc = OneHotEncoder(dtype=int).fit(nominal_feature)
    nominal_feature = enc.transform(nominal_feature).toarray()
    
    # 将转换好的数据添加到原数据之后
    whole_data = np.hstack((numeric_feature, nominal_feature))
    label_train = label_train.reshape((train_count, 1))
    train_data = np.hstack((whole_data[:train_count, :], label_train))
    test_data = whole_data[train_count:]
    
    total, num_feature = whole_data.shape
    print 'Total:', total
    print 'Train:', train_count
    print 'Num of features:', num_feature
    import ipdb; ipdb.set_trace()
    print 'Saving processed results...'
    np.savetxt("dataset/train2.csv", train_data, delimiter=",", fmt='%2f')
    np.savetxt("dataset/test2.csv", test_data, delimiter=",", fmt='%2f')

if __name__ == '__main__':
    main()
