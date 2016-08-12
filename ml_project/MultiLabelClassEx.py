# coding = utf8

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import datasets
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
iris = datasets.load_iris()
X, y = iris.data, iris.target
result = OneVsOneClassifier(LinearSVC(random_state= 0)).fit(X, y).predict(X)
print result


def test_transform_label():
    test_label = [[2, 3, 4], [0, 1, 3], [0, 1, 2, 3, 4], [0, 1, 2]]
    result = MultiLabelBinarizer().fit_transform(test_label)
    print result


def transform_label(raw_arr):
    return MultiLabelBinarizer().fit_transform(raw_arr)
