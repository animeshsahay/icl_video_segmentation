import cv2
import math
import numpy as np
import random

class FaceComparator:
    def __init__(self, faces):
        raise "Unimplemented function"

    def compare(self, face1, face2):
        raise "Unimplemented function"

class HistogramComparator(FaceComparator):
    def __init__(self, faces):
        pass

    def compare(self, f1, f2):
        frame1, face1 = f1
        frame2, face2 = f2
        return compareFaces(face1, face2)

class PCAComparator(FaceComparator):
    def __init__(self, faces):
        self.faces = [cv2.cvtColor(face, cv2.COLOR_RGB2GRAY) for _, face in faces]
        self.recompute()

    def compare(self, f1, f2):
        frame1, face1 = f1
        frame2, face2 = f2

        face1    = cv2.cvtColor(face1, cv2.COLOR_RGB2GRAY)
        face2    = cv2.cvtColor(face2, cv2.COLOR_RGB2GRAY)

        f1p = self.eigvals * (self.project(face1) - self.minvals) / self.diffs
        f2p = self.eigvals * (self.project(face2) - self.minvals) / self.diffs

        #return np.square(f1p - f2p).sum()
        return np.abs(f1p - f2p).sum()

    def project(self, iface):
        face = (iface - self.mean).flatten()
        return np.dot(self.eigvecs.T, face)

    def recompute(self):
        _faces = [face.flatten() for face in self.faces]
        faces  = np.asarray(_faces)

        mean          = faces.mean(axis = 0)
        unbiasedFaces = faces - mean

        #TODO: Find out value when only one face
        cov              = np.dot(unbiasedFaces, unbiasedFaces.transpose()) / (unbiasedFaces.shape[0] - 1)
        eigvals, eigvecs = np.linalg.eig(cov)
        eigvecs          = np.dot(unbiasedFaces.transpose(), eigvecs)

        sortedidxs   = np.argsort(-eigvals)
        self.eigvals = eigvals[sortedidxs] / eigvals.sum()
        self.eigvecs = eigvecs[:, sortedidxs]

        self.mean = mean.reshape(self.faces[0].shape)
        #cv2.imwrite("mean-%f.jpg" % random.random(), np.array(self.mean, dtype=np.uint8))

        projections = np.asarray([self.project(face) for face in self.faces])
        self.minvals = projections.min(axis = 0)
        self.maxvals = projections.max(axis = 0)
        self.diffs   = np.abs(self.maxvals - self.minvals)

def convertFaces(video):
    X = []
    biggestFace = (0, 0)
    faceList = video.getFaces()
    
    for frame, faces in faceList:
        f = video.getFrame(frame)
        
        for face in faces:
            if face[2] * face[3] > biggestFace[0] * biggestFace[1]:
                biggestFace = (face[2], face[3])
            
            X.append((frame, f[face[1]:(face[1] + face[3]), face[0]:(face[0] + face[2])]))

    return map(lambda (frame, face): (frame, cv2.resize(face, biggestFace)), X)

def compareFaces(f1, f2):
    h1 = cv2.calcHist([f1], [0], None, [256], [0, 255])
    h2 = cv2.calcHist([f2], [0], None, [256], [0, 255])

    cv2.normalize(h1, h1, 0, 255, cv2.NORM_MINMAX)
    cv2.normalize(h2, h2, 0, 255, cv2.NORM_MINMAX)

    return cv2.compareHist(h1, h2, cv2.cv.CV_COMP_BHATTACHARYYA)

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
                lowlinks[v] = min(lowlinks[v], lowlinks[succ])
            elif succ in stack:
                lowlinks[v] = min(lowlinks[v], indexes[succ])

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

def clusterFaces(faces, options):
    if faces is None or faces == []:
        return []

    options = mergeDefaults(options)
    clusters = options['clusterAlgorithm'](faces, options)

    return [[faces[i] for i in l] for l in clusters]

def standardCluster(faces, options):
    similarities = {}
    clusters = []

    group = options["comparator"](faces)

    for i, f in enumerate(faces):
        for i2_, f2 in enumerate(faces[i:]):
            i2 = i2_ + i

            v = 1.0 - group.compare(f, f2)

            if v > options["clusterThreshold"]:
                for (a, b) in [(i, i2), (i2, i)]:
                    try:
                        similarities[a].add(b)
                    except:
                        similarities[a] = set([b])

    return tarjan(similarities)

class Cluster:
    def __init__(self, faces):
        assert(len(faces) > 0)
        assert(all([faces[0][1].shape == face.shape for _, face in faces]))
        self.centre = np.mean([face for _, face in faces], axis = 0)
        self.faces = faces
        self.shape = faces[0][1].shape

    def __repr__(self):
        return str([frame for frame, _ in self.faces])

    def update(self, faces):
        assert(len(faces) > 0)
        self.faces = faces
        oldCentre = self.centre
        self.centre = np.mean([face for _, face in faces], axis = 0)
        return getDist(oldCentre, self.centre)

def kMeansCluster(faces, options):
    assert(options["comparator"] == PCAComparator)

    group = options["comparator"](faces)
    faces = [(frame, group.project(cv2.cvtColor(face, cv2.COLOR_RGB2GRAY))) for frame, face in faces]

    initial = random.sample(faces, options["k"])
    clusters = [Cluster([f]) for f in initial]

    biggestShift = options["cutoff"]
    iterations = 0
    while biggestShift >= options["cutoff"] or iterations == options["maxIterations"]:
        lists = [[] for _ in clusters]
        for frame, face in faces:
            idx = np.argmin([getDist(face, cluster.centre) for cluster in clusters])
            lists[idx].append((frame, face))
        biggestShift = np.max([c.update(l) for l, c in zip(lists, clusters)])
        iterations += 1

    return [[frame for frame, _ in cluster.faces] for cluster in clusters]

def meanShiftCluster(faces, options):
    assert(options["comparator"] == PCAComparator)

    group = options["comparator"](faces)
    faces = [(frame, group.project(cv2.cvtColor(face, cv2.COLOR_RGB2GRAY))) for frame, face in faces]

    #Generate bandwidth
    amount = max(int(len(faces) * 0.3), 1)
    avgs   = []
    for i, (_, face1) in enumerate(faces):
        dists = np.sort([getDist(face1, face2)
                         for j, (_, face2) in enumerate(faces)
                         if i != j])
        avgs.append(np.mean(dists[0:min(len(dists), amount)]))

    bandwidth = np.max(avgs)
    cutoff    = 0.001 * bandwidth

    #Generate seeds
    seeds = [Cluster([face]) for face in faces]
    clusters = []

    for seed in seeds:
        while True:
            neighbours = [(frame, face) for frame, face in faces if getDist(seed.centre, face) <= bandwidth]
            if len(neighbours) == 0:
                break

            if seed.update(neighbours) < cutoff:
                clusters.append(seed)
                break

    clusters.sort(key = lambda s: len(s.faces), reverse = True)
    unique = np.ones(len(clusters), dtype=np.bool)

    for i, cluster in enumerate(clusters):
        if unique[i]:
            neighbours = [n for n, c in enumerate(clusters)
                          if getDist(c.centre, cluster.centre) <= bandwidth]
            unique[neighbours] = 0
            unique[i] = 1

    centres = [cluster.centre for cluster in np.array(clusters)[unique]]

    clusters = [[] for _ in centres]

    for i, (_, face) in enumerate(faces):
        idx = np.argmin([getDist(face, centre) for centre in centres])
        clusters[idx].append(i)

    return clusters

def getDist(arr1, arr2):
    assert(arr1.shape == arr2.shape)
    distSqrd = np.sum(np.power(arr2 - arr1, 2))
    return math.sqrt(distSqrd)

def mergeDefaults(options):
    defaults = {"clusterThreshold" : 0.63,
                "comparator"       : PCAComparator,
                "clusterAlgorithm" : meanShiftCluster,
                "k"                : 2,
                "cutoff"           : 1,
                "maxIterations"    : -1}

    for k, v in defaults.items():
        if k not in options:
            options[k] = v

    return options
