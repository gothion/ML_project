# coding=utf8

from treeinterpreter import treeinterpreter as ti
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np

from sklearn.datasets import load_boston
boston = load_boston()
rf = RandomForestRegressor()
rf.fit(boston.data[:300], boston.target[:300])

instances = boston.data[[300, 309]]
print instances
print "Instance 0 prediction:", rf.predict(instances[0])
print "Instance 1 prediction:", rf.predict(instances[1])

prediction, bias, contributions = ti.predict(rf, instances)

prediction, bias, contributions = ti.predict(rf, instances)
for i in range(len(instances)):
    print "Instance", i
    print "Bias (trainset mean)", bias[i]
    print "Feature contributions:"
    for c, feature in sorted(zip(contributions[i],
                                 boston.feature_names),
                             key=lambda x: -abs(x[0])):
        print feature, round(c, 2)
    print "-"*20