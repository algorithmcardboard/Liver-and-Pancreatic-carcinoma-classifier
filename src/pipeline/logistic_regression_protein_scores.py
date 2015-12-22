import time
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV

print "Script start at ", datetime.now().isoformat()

X = np.load('/scratch/ac5901/protein_data.npy')

Y=X[:,:2]
X=X[:,2:]

RS=np.random.RandomState(9)
perm=RS.permutation(307)

Y=Y[perm]
X=X[perm]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y[:,1], test_size=0.25, random_state=30, stratify=Y[:,1])

pipe = Pipeline([('pca',PCA()), 
                     ('scaled',StandardScaler()), 
                                      ('lg_r',LogisticRegression())])

n_components=[6, 12, 22, 44, 66, 116, 205]
C_vals = np.logspace(-9,9, num=19, base=2)

gs=GridSearchCV(pipe, dict(pca__n_components=n_components, lg_r__C=C_vals), cv=10, n_jobs=8, verbose=100)

gs.fit(X_train, Y_train)

score=gs.score(X_test, Y_test)

print score
print gs.best_score_
print gs.best_estimator_
print gs.best_params_

outfile="grid_lr_cancer_protein_search_scores_{0}.out".format(int(time.time()))

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
