from Client import Client, SplitType
from optparse import OptionParser
from Segmenter import Segmenter
from timeit import timeit
import traceback

unspecifiedVideos = ["res/hungergames-720p.mp4", "res/skyfall.mp4", "res/tangled.mp4"]
unspecifiedFrameLengths = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-v", "--videos", dest = "videos"      , type = "string", action = "append", default = [])
    parser.add_option("-s", "--start" , dest = "start"       , type = "int"   , action = "store" , default = 250)
    parser.add_option("-f", "--frames", dest = "frameLengths", type="int"     , action = "append", default = [])
    opts, args = parser.parse_args()

    if opts.videos is None or opts.videos == []:
        opts.videos = unspecifiedVideos

    if opts.frameLengths is None or opts.frameLengths == []:
        opts.frameLengths = unspecifiedFrameLengths

    for vid in opts.videos:
        print("*** Video : ", vid)

        for length in opts.frameLengths:
            try:
                print("   --- Length : " + str(opts.start) + " -> " + str(opts.start + length))
                client = Client(vid, SplitType.ON_FACE_CLUSTERS, start = opts.start, end = opts.start + length)
                t1 = timeit(lambda: client.run(Segmenter(), True, "THEO", "OGG", False, options = {"verbose" : 0, "write" : False}), number = 1)
                t2 = timeit(lambda: client.run(Segmenter(), True, "THEO", "OGG", False, options = {"verbose" : 0, "write" : False}), number = 1)
                print("   Total:                   %f" % t1)
                print("   Clustering/Segmentation: %f" % t2)
                print("   Facial recognition:      %f" % (t1 - t2))
            except Exception, err:
                print traceback.format_exc()
