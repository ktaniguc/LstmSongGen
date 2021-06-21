import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import sys

def num2note_on_off(num):
  if int(num, 10) == 1:
    return "note_on"
  else:
    return "note_off"

args = sys.argv 
inputName = args[1] + "_result.txt"
outputName = args[2] + "_result.mid"
f = open(inputName, 'r')
data = f.read()
print(data.split(","))
data_per_sound = data.split(",")
print("type of data_per_sound = ", type(data_per_sound))
#type(note_on=1, note_off=0)_note_velocity_time
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)
bpm = int(args[3])
track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
for i_data in data_per_sound:
  #print(i_data)
  if i_data == "":
    continue
  parts = i_data.split("_")
  if len(parts) != 4 or int(parts[0], 10) > 1:
    continue
  if parts[3] == "":
    continue
  if int(parts[2]) > 127:
    continue

  print(parts)
  track.append(Message(num2note_on_off(parts[0]), note=int(parts[1], 10), velocity=int(parts[2], 10), time=int(parts[3], 10)))

mid.save(outputName)
