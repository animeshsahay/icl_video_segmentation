import std.concurrency : thisTid, send, receive, Tid, spawn;
import std.container : SList;
import std.process : shell, system;
import std.stdio : writefln, format, chomp;

auto videos = ["res/hungergames-720p.mp4", "res/skyfall.mp4", "res/tangled.mp4"];

void main() {
  auto compTid = spawn(&distributeComputers);

  Tid[] threads;
  foreach(video; videos)
    threads ~= spawn(&runVideo, thisTid, compTid, video);

  foreach(i; 0..threads.length)
    receive((string s) { writefln("Video %s is done", s); });

  send(compTid, true);
}

void distributeComputers() {
  SList!string comps;

  foreach(i; 1..25)
    comps.insertFront("edge" ~ format("%02d", i));

  bool done = false;
  while(!done)
    receive((Tid tid) { writefln("Sending.."); send(tid, comps.removeAny()); },
            (bool s) { done = s; });
}

void runVideo(Tid masterTid, Tid compTid, string video) {
  writefln(video);
  bool done = false;
  string comp = "";

  while(!done) {
    send(compTid, thisTid);
    receive((string s) { comp = s; });
    writefln("Trying on %s", comp);
    auto output = system("ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
                         ~ comp
                         ~ " \"cd Development/Python/icl_video_segmentation && make validate ARGS='-v " ~ video ~ " -f 10' 2>/dev/null > " ~ comp ~ ".output\"");
    done = output == 0;
  }

  send(masterTid, video);
}