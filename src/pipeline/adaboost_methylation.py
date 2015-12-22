import time
from datetime import datetime
import csv
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV

print "Script start at ", datetime.now().isoformat()

X = np.load('/scratch/ajr619/fml/methylation_norm.npy')

Y=X[:,:2]
X=X[:,2:]

print(X.shape, Y.shape)

RS=np.random.RandomState(90)
perm=RS.permutation(307)

Y=Y[perm]
X=X[perm]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y[:,1], test_size=0.25, random_state=30, stratify=Y[:,1])

pipe = Pipeline([('pca',PCA()), 
                 ('scaled',StandardScaler()), 
                 ('adaboost',AdaBoostClassifier())])


n_components=[4,20,92,255,361,513]
n_estimators = [50,100, 150]
learning_rate = [0.1, 0.25, 0.5, 0.65, 0.75, 0.9, 1]

gs=GridSearchCV(pipe, dict(pca__n_components=n_components, 
                           adaboost__n_estimators=n_estimators, 
                           adaboost__learning_rate=learning_rate), 
                cv=10, n_jobs=12, verbose=10)

gs.fit(X_train, Y_train)
print "Test score ", gs.score(X_test, Y_test)

outfile="grid_adab_dna_cancer_{0}.out".format(int(time.time()))

with open(outfile, "w") as scoreFile:
    writer = csv.writer(scoreFile, delimiter = ",")
    paramKeys = list(gs.grid_scores_[0].parameters.keys())

    writer.writerow(['mean']+ paramKeys)

    for i in gs.grid_scores_:
        output = list()
        output.append(i.mean_validation_score)

        for k in paramKeys:
            output.append(i.parameters.get(k))

        writer.writerow(output)

print "Script end at ", datetime.now().isoformat()
