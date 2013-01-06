from Client import Client, SplitType
from Segmenter import Segmenter
from timeit import timeit

videos = [("hungergames-720p.mp4", 120), ("skyfall.mp4", 96), ("tangled.mp4", 168)]
frameLengths = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

if __name__ == "__main__":
    for (vid, s) in videos:
        print("*** Video : " + vid)

        for length in frameLengths:
            print("   --- Length : " + str(s) + " -> " + str(s + length))
            client = Client("res/" + vid, SplitType.ON_FACE_CLUSTERS, start = s, end = s + length)
            print("   Total: ")
            timeit(lambda: client.run(Segmenter(), True, "THEO", "OGG", False), number = 1)
            print("   Clustering/Segmentation: ")
            timeit(lambda: client.run(Segmenter(), True, "THEO", "OGG", False), number = 1)
