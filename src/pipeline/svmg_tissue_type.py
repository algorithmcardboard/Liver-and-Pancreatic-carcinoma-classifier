import time
import csv
import numpy as np
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV

X=np.load('/scratch/ac5901/methylation_norm.npy')
Y=X[:,:3]
X=X[:,3:]

RS=np.random.RandomState(90)
perm=RS.permutation(625)

Y=Y[perm]
X=X[perm]

X_train, X_test, Y_train2, Y_test2 = train_test_split(X, Y[:,2], test_size=0.25, random_state=30, stratify=Y[:,2])

pipe=Pipeline([('pca',PCA()), ('scaled',StandardScaler()), ('svm_gaussian',svm.SVC(kernel='rbf',C=1,gamma=1,class_weight={0:0.45,1:1}))])

cval=[2**-9,2**-8,2**-7,2**-6,2**-5, 2**-4, 2**-3, 2**-2, 2**-1, 2**0, 2**1, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9]
gval=[2**-9,2**-8,2**-7,2**-6,2**-5, 2**-4, 2**-3, 2**-2, 2**-1, 2**0, 2**1, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9]
pca_val=[4, 20, 92, 255, 361, 513]

gs=GridSearchCV(pipe, dict(pca__n_components=pca_val, svm_gaussian__C=cval, svm_gaussian__gamma=gval), cv=StratifiedShuffleSplit(Y[:,2],test_size=0.25,random_state=30), n_jobs=12, verbose=100)
gs.fit(X_train, Y_train2)

score=gs.score(X_test, Y_test2)

print score
print gs.best_score_
print gs.best_estimator_
print gs.best_params_

outfile="grid_search_gaussian_tissue_scores_{0}.out".format(int(time.time()))

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


