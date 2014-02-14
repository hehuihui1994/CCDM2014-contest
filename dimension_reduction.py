#coding=utf8

"""
对原始数据进行降维
特征提取/降维方法：PCA，ICA，CCA, ISOMAP
特征选择：MRMR
注：原始数据中一些特征的取值全部为0，这种情况在降维时已经考虑了。
"""

import numpy as np

def PCA(model_train_data, model_test_data, test_data):
    """ Unsupervised dimension reduction
    Note: 由于scikit-learn中PCA无法针对目前的训练集进行PCA分解，所以这里采用matlab的分解结果
    """
    #import ipdb; ipdb.set_trace()
    print 'PCA fitting...'
    """
    from sklearn.decomposition import PCA
    pca = PCA(n_components, whiten=False).fit(model_train_data)
    print 'PCA transformation...'
    model_train_data2 = pca.transform(model_train_data)
    model_test_data2 = pca.transform(model_test_data)
    test_data2 = pca.transform(test_data)
    """
    # 读入mat文件
    import scipy.io
    mat_dict = scipy.io.loadmat('dataset/task2-PCA-decomp.mat')
    W = np.asmatrix(mat_dict['COEFF'])
    X_transformed = np.asmatrix(mat_dict['SCORE']) # 已经转换好的
    
    model_train_data2 = X_transformed
    model_test_data2 = np.asmatrix(model_test_data) * W
    test_data2 = np.asmatrix(test_data) * W
    
    return model_train_data2, model_test_data2, test_data2
    
def main():
    print 'Loading dataset...'
    train_path = 'dataset/train-model.csv'    
    train_data = np.genfromtxt(train_path, delimiter=',')
    label_train = np.array(train_data[:, -1], int)
    model_train_data = train_data[:, :-1]

    # 用于测试训练模型的测试集
    test_path = 'dataset/test-model.csv'
    model_test_data = np.genfromtxt(test_path, delimiter=',')
    label_test = np.array(model_test_data[:, -1], int)
    model_test_data = model_test_data[:, :-1]
    # 真正的训练集
    test_path = 'dataset/test2.csv'
    test_data = np.genfromtxt(test_path, delimiter=',')

    # 这里我们保存所有的维度，在进行模型选择时再决定
    #n_components = 100

    dr_method = 'PCA'
    model_train_data2, model_test_data2, test_data2 = PCA(model_train_data, model_test_data, test_data)
        
    # 保存降维后的结果
    print 'Saving new datasets...'
    import pickle
    f = open('dataset/task2-PCA.pickle', 'w')
    pickle.dump([model_train_data2, label_train, model_test_data2, label_test, test_data2], f)
    f.close()

if __name__ == '__main__':
    main()
