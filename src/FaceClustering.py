from VideoWrapper import *
from cv2 import *
import sys

def readFaces(video):
    X = []
    biggestFace = (0, 0)
    
    for frame, faces in video.getFaces():
        f = video.getFrame(frame)
        
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

if __name__ == "__main__":
    faces = readFaces(VideoWrapper(VideoCapture(sys.argv[1]), 265, 400))

    sim = clusterFaces(faces)

    for cluster in sim:
        for i, face in enumerate(cluster):
            imshow(str(i), faces[face])
        waitKey(0)

    print sim

