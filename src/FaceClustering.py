from VideoWrapper import *
import cv2 
import sys
#from PIL import Image
#from numpy import *
import numpy as np
#import pylab

def readFaces(video):
    X = []
    biggestFace = (0, 0)
    
    for frame, faces in video.getFaces():
        f = video.getFrame(frame)
        #imshow(str(frame), f)
        
        for face in faces:
            if face[2]*face[3] > biggestFace[0]*biggestFace[1]:
                biggestFace = (face[2], face[3])
            
            X.append(f[face[1]:(face[1]+face[3]), face[0]:(face[0]+face[2])])

    res = map(lambda f: cvtColor(resize(f, biggestFace), COLOR_BGR2GRAY), X)
    return res

def comparePixels(p1, p2):
    return 1.0-abs(float(p1) - float(p2))/255.0

def compareFaces(f1, f2):
    h1 = calcHist([f1], [0], None, [256], [0, 255])
    h2 = calcHist([f2], [0], None, [256], [0, 255])

    normalize(h1, h1, 0, 255, NORM_MINMAX)
    normalize(h2, h2, 0, 255, NORM_MINMAX)

    return compareHist(h1, h2, cv.CV_COMP_BHATTACHARYYA)

def clusterFaces(faces, t=0.75):
    similarities = {}
    clusters = []

    for i, f in enumerate(faces):
        for i2_, f2 in enumerate(faces[i:]):
            i2 = i2_ + i

            v = 1.0-compareFaces(f, f2)

            if v > t:
                for (a, b) in [(i, i2), (i2, i)]:
                    try:
                        similarities[a].add(b)
                    except:
                        similarities[a] = set([b])


    print similarities
    return tarjan(similarities)

def tarjan(graph):
    output = []

    index = [0]
    indexes = {}
    lowlinks = {}
    stack = []

    def strong_connect(v):
        indexes[v] = index[0]
        lowlinks[v] = index[0]
        index[0] = index[0] + 1
        stack.append(v)

        successors = graph[v]

        for succ in successors:
            if succ not in indexes:
                strong_connect(succ)
                lowlinks[v] = __builtins__.min(lowlinks[v], lowlinks[succ])
            elif succ in stack:
                lowlinks[v] = __builtins__.min(lowlinks[v], indexes[succ])

        if indexes[v] == lowlinks[v]:
            connected_component = []

            while True:
                succ = stack.pop()
                connected_component.append(succ)
                if succ == v:
                    break
        
            output.append(connected_component)

    for v in graph:
        if v not in indexes:
            strong_connect(v)

    return output

def writeFace(f, index):
    normalize(f, f, 0, 255, NORM_MINMAX)
    imwrite("img" + str(index) + ".jpg", f)
#
#
#def pca(X):
#    # Principal Component Analysis
#    # input: X, matrix with training data as flattened arrays in rows
#    # return: projection matrix (with important dimensions first),
#    # variance and mean
#
#    #get dimensions
#    num_data,dim = X.shape
#
#    #center data
#    mean_X = X.mean(axis=0)
#    for i in range(num_data):
#        X[i] -= mean_X
#        if dim>100:
#            print 'PCA - compact trick used'
#            M = dot(X,X.T) #covariance matrix
#            e,EV = linalg.eigh(M) #eigenvalues and eigenvectors
#            tmp = dot(X.T,EV).T #this is the compact trick
#            V = tmp[::-1] #reverse since last eigenvectors are the ones we want
#            S = sqrt(e)[::-1] #reverse since eigenvalues are in increasing order
#        else:
#            print 'PCA - SVD used'
#            U,S,V = linalg.svd(X)
#            V = V[:num_data] #only makes sense to return the first num_data
#
#        #return the projection matrix, the variance and the mean
#        return V,S,mean_X
#
#

'''
def read_images(path, sz=None):
    c=0
    X,y = [], []
    for dirname , dirnames , filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname , subdirname)
            for filename in os.listdir(subject_path):
                try:
                    im = Image.open(os.path.join(subject_path , filename))
                    im = im.convert("L")
                    # resize to given size (if given)
                    if (sz is not None):
                        im = im.resize(sz, Image.ANTIALIAS)
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)
                except IOError:
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
    return [X,y]


def asRowMatrix(X):
    if len(X) == 0:
        return np.array([])
    mat = np.empty((0, X[0].size), dtype=X[0].dtype)
    for row in X:
        mat = np.vstack((mat, np.asarray(row).reshape(1,-1)))
    return mat

def pca(X, y, num_components=0):
    [n,d] = X.shape
    if (num_components <= 0) or (num_components >n):
        num_components = n
    mu = X.mean(axis=0)
    X = X - mu
    if n>d:
        C = np.dot(X.T,X)
        [eigenvalues ,eigenvectors] = np.linalg.eigh(C)
    else:
        C = np.dot(X,X.T)
        [eigenvalues ,eigenvectors] = np.linalg.eigh(C)
        eigenvectors = np.dot(X.T,eigenvectors)
        for i in xrange(n):
            eigenvectors[:,i] = eigenvectors[:,i]/np.linalg.norm(eigenvectors[:,i])
    # or simply perform an economy size decomposition
    # eigenvectors , eigenvalues , variance = np.linalg.svd(X.T, full_matrices=False)
    # sort eigenvectors descending by their eigenvalue
    idx = np.argsort(-eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:,idx]
    # select only num_components
    eigenvalues = eigenvalues[0:num_components].copy() 
    eigenvectors = eigenvectors[:,0:num_components].copy()
    return [eigenvalues , eigenvectors , mu]

def project(W, X, mu=None):
    if mu is None:
        return np.dot(X,W)
    return np.dot(X - mu, W)

'''


if __name__ == "__main__":
    faces = readFaces(VideoWrapper(VideoCapture(sys.argv[1]), 2650, 2800))
    #[X,y] = read_images(")
    
    
    
    
    
    
    
    
    '''
    mean, eigenvectors = cv2.PCACompute(np.array([faces[20].flatten()]))
    
    f = cv2.equalizeHist(faces[0])
    cv2.normalize(f, f, 0, 255, cv2.NORM_MINMAX)
    vec = f.reshape(1, f.shape[0]*f.shape[1])
    projection = cv2.PCAProject(vec, mean, eigenvectors)
    '''
    
    '''
    data = np.array([f.flatten() for f in faces])
    rows = len(faces)
    #data = cv.fromarray(data)
    #data.reshape(rows, cols)
    #print data[:3]
    
    np.reshape(mean, (len(data[0]), 1))
    normalize(mean, mean, 0, 255, NORM_MINMAX);
    imshow("mean", mean)
    waitKey(0)
    '''
    
    #print mean
    #pcaProject = cv2.PCAProject(data, mean, pcaCompute)
    #comps = np.dot(data.transpose(), pcaProject)
#print(comps)
#   imshow("img", comps)
    #imshow("mean", mean)
#   waitKey(0)
    

    #sim = clusterFaces(faces)

    #for cluster in sim:
    #    for i, face in enumerate(cluster):
    #        imshow(str(i), faces[face])
    #    waitKey(0)
    #    destroyAllWindows()

    #print sim

