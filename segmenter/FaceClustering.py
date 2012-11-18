import cv2
import numpy as np

import sys
from VideoWrapper import VideoWrapper, VideoCapture

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
        face1 = cv2.cvtColor(face1, cv2.COLOR_RGB2GRAY)
        face2 = cv2.cvtColor(face2, cv2.COLOR_RGB2GRAY)
        return compareFaces(self.project(face1), self.project(face2))

    def project(self, iface):
        face = np.asarray([(iface - self.mean).flatten()]).transpose()
        return np.asarray([np.dot(self.eigvecs[0], faceval) for faceval in face]).reshape(iface.shape).astype(np.uint8)

    def recompute(self):
        _faces = [face.flatten() for face in self.faces]
        faces  = np.asarray(_faces)

        mean          = faces.mean(axis = 0)
        unbiasedFaces = faces - mean

        cov              = np.dot(unbiasedFaces, unbiasedFaces.transpose()) / unbiasedFaces.shape[0]
        eigvals, eigvecs = np.linalg.eig(cov)

        sortedidxs   = np.argsort(-eigvals)
        self.eigvals = eigvals[sortedidxs][0:1]
        self.eigvecs = eigvecs[:, sortedidxs][0:, 0:1]

        self.mean = mean.reshape(self.faces[0].shape)

def convertFaces(video, faceList = None):
    X = []
    biggestFace = (0, 0)

    if faceList is None:
        faceList = video.getFaces()
    
    for frame, faces in faceList:
        f = video.getFrame(frame)
        
        for face in faces:
            if face[2]*face[3] > biggestFace[0]*biggestFace[1]:
                biggestFace = (face[2], face[3])
            
            X.append((frame, f[face[1]:(face[1]+face[3]), face[0]:(face[0]+face[2])]))

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

def clusterFaces(faces, t = 0.75, comparator = HistogramComparator):
    similarities = {}
    clusters = []

    group = comparator(faces)

    for i, f in enumerate(faces):
        for i2_, f2 in enumerate(faces[i:]):
            i2 = i2_ + i

            v = 1.0 - group.compare(f, f2)

            if v > t:
                for (a, b) in [(i, i2), (i2, i)]:
                    try:
                        similarities[a].add(b)
                    except:
                        similarities[a] = set([b])

    t = tarjan(similarities)
    return [[faces[i] for i in l] for l in t]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        faces = [(i, cv2.imread("pics/img%d.jpg" % i)) for i in range(12)]
    else:
        faces = convertFaces(VideoWrapper(VideoCapture(sys.argv[1]), 360, 380))

    print clusterFaces(faces, comparator = HistogramComparator)
