import time
from datetime import datetime
import csv
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import GaussianNB

print "Script start at ", datetime.now().isoformat()

X=np.load('/scratch/ac5901/protein_data.npy')
Y=X[:,:2]
X=X[:,2:]

RS=np.random.RandomState(9)
perm=RS.permutation(307)

Y=Y[perm]
X=X[perm]

X_train, X_test, Y_train1, Y_test1 = train_test_split(X, Y[:,1], test_size=0.25, random_state=30, stratify=Y[:,1])

pipe=Pipeline([('pca',PCA()), ('scaled',StandardScaler()), ('gbayes',GaussianNB())])

pca_val=[6,12,22,44,66,116]

gs=GridSearchCV(pipe, dict(pca__n_components=pca_val), n_jobs=12, verbose=100)
gs.fit(X_train, Y_train1)

score=gs.score(X_test, Y_test1)

print score
print gs.best_score_
print gs.best_estimator_
print gs.best_params_

outfile="grid_gnb_protein_cancer_search_scores_{0}.out".format(int(time.time()))

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
