from Client import Client, SplitType
from Segmenter import Segmenter
from timeit import timeit
import traceback

videos = [("hungergames-720p.mp4", 120), ("skyfall.mp4", 96), ("tangled.mp4", 168)]
frameLengths = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

if __name__ == "__main__":
    for (vid, s) in videos:
        print("*** Video : " + vid)

        for length in frameLengths:
            try:
                print("   --- Length : " + str(s) + " -> " + str(s + length))
                client = Client("res/" + vid, SplitType.ON_FACE_CLUSTERS, start = s, end = s + length)
                t1 = timeit(lambda: client.run(Segmenter(), True, "THEO", "OGG", False, options = {"verbose" : 0, "write" : False}), number = 1)
                t2 = timeit(lambda: client.run(Segmenter(), True, "THEO", "OGG", False, options = {"verbose" : 0, "write" : False}), number = 1)
                print("   Total:                   %f" % t1)
                print("   Clustering/Segmentation: %f" % t2)
                print("   Facial recognition:      %f" % (t1 - t2))
            except Exception, err:
                print traceback.format_exc()
