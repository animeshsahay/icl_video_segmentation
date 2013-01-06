import std.concurrency : thisTid, send, receive, Tid, spawn;
import std.container : SList;
import std.getopt  : getopt, config;
import std.process : shell, system;
import std.stdio : writefln, format, chomp;

auto videos = ["res/hungergames-720p.mp4", "res/skyfall.mp4", "res/tangled.mp4"];

void main(string[] args) {
  if(args.length != 2) {
    writefln("USAGE: %s <location of repo>");
    return;
  }

  auto location = args[1];

  auto compTid = spawn(&distributeComputers, thisTid);

  Tid[] threads;
  foreach(video; videos)
    threads ~= spawn(&runVideo, thisTid, compTid, location, video);

  foreach(i; 0..threads.length)
    receive((string s) { writefln("Video %s is done", s); },
            (bool b) { throw new Exception("Out of computers!"); });

  send(compTid, true);
}

void distributeComputers(Tid masterTid) {
  SList!string comps;

  foreach(i; 1..25)
    comps.insertFront("edge" ~ format("%02d", i));

  bool done = false;
  while(!done)
    receive((Tid tid) { if(comps.empty()) send(masterTid, false); send(tid, comps.removeAny()); },
            (bool s) { done = s; });
}

void runVideo(Tid masterTid, Tid compTid, string location, string video) {
  writefln(video);
  bool done = false;
  string comp = "";

  while(!done) {
    send(compTid, thisTid);
    receive((string s) { comp = s; });
    writefln("Trying on %s", comp);
    auto output = system("ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
                         ~ comp
                         ~ " \"cd '" ~ location ~ "' && make validate ARGS='-v " ~ video ~ "' 2>/dev/null > " ~ comp ~ ".output\"");
    done = output == 0;
  }

  send(masterTid, video);
}