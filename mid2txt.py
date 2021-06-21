import mido
from mido import Message, MidiFile
from pathlib import Path
import sys

# 各トラック毎の全メッセージを表示する
def dump_track(track_obj):
    for msg in track_obj:
        print(msg)

# 全トラックの全メッセージをトラック毎に表示する
def dump_smf(midi_obj):
    for i, track in enumerate(midi_obj.tracks):
        print(f"Track {i}: {track.name}")
        dump_track(track)

def note_on_off(msg_type):
  if msg_type == "note_on":
    return "1_"
  else:
    return "0_"

args = sys.argv
pathlist = Path(args[1]).glob('**/*.mid')
outputname = args[2] + ".txt"
f = open(outputname, 'w')

for path in pathlist:
  print(path)
  mid = MidiFile(path)
  dump_smf(mid)
  for i, track in enumerate(mid.tracks):
    for msg in track:
      chunk = ""
      if msg.type == "note_on" and msg.velocity == "0":
        msg.type = "note_off"

      if msg.type == "note_on" or msg.type == "note_off":
        chunk = note_on_off(msg.type)
        chunk += str(msg.note) + "_"
        chunk += str(msg.velocity) + "_"
        chunk += str(msg.time) + ","

        f.write(chunk)

        print(chunk)

f.close()

