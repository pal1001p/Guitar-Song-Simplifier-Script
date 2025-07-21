import librosa
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from chord_extractor.extractors import Chordino
import os

# os.environ['VAMP_PATH'] = '/Users/Polina/Library/Audio/Plug-Ins/Vamp'
file = '/Users/Polina/Downloads/converts/og.wav'
min_length = 1.0  # seconds to keep as a stable chord

# # MADMOM - EASY CHORD DETECTION FOR INPUT FILE
# dcp = DeepChromaProcessor()
# decode = DeepChromaChordRecognitionProcessor()
# chroma = dcp(file)
# chords = decode(chroma)
# print(chords)
# smoothed_chords = []
# for start, end, chord in chords:
#         if end - start >= min_length and chord != 'N' and chord is not None:
#             smoothed_chords.append((start, end, chord))
# for index, (start, end, chord) in enumerate(smoothed_chords):
#     print(f"MADMOM:      Chord {index + 1} of {len(smoothed_chords)}: {chord}   Start: {start:.2f}s   End: {end:.2f}s")
# unique_madmom = []
# for (start,end,chord) in smoothed_chords:
#     if chord not in unique_madmom:
#         unique_madmom.append(chord)
#     else:
#         continue

# for index,chord in enumerate(unique_madmom):
#      print(f'UNIQUE CHORD IN MADMOM:       Chord {index + 1} of {len(unique_madmom)}: {chord}')


# # CHORDINO - COMPLEX CHORD DETECTION FOR INPUT FILE
# chordino = Chordino(roll_on = 1)
# #note: .wavs used
# chords = chordino.extract(file)
# smoothed_chords_chordino = []
# for index,chord in enumerate(chords):
#     if chord.chord != 'N' and chords[index+1].timestamp - chord.timestamp >= min_length:
#         smoothed_chords_chordino.append(chord)
        
# for index, chord in enumerate(smoothed_chords_chordino): 
#         print(f"CHORDINO:       Chord {index + 1} of {len(chords)}: {chord.chord}  Start: {chord.timestamp:.2f}s")

# unique_chordino = []
# for chord in smoothed_chords_chordino:
#     if chord.chord not in unique_chordino:
#         unique_chordino.append(chord.chord)
#     else:
#         continue

# for index,chord in enumerate(unique_chordino):
#      print(f'UNIQUE CHORD IN CHORDINO:       Chord {index + 1} of {len(unique_chordino)}: {chord}')


# LIBROSA - TEMPO AND BEAT DETECTION FOR INPUT FILE
audio, sampling_rate = librosa.load(file)
tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sampling_rate)
print(f'Estimated tempo: {tempo} beats per minute')
beat_times_librosa = librosa.frames_to_time(beat_frames, sr=sampling_rate)
for beat in beat_times_librosa:
    print(f'LIBROSA beat time: {beat:.2f}s')


# # PYAUDIO and MADMOM - REAL TIME AUDIO BEATS WITH TIMESTAMPING
# import pyaudio
# p = pyaudio.PyAudio()
# num_devices = p.get_device_count()
# for i in range(num_devices): 
#     print(p.get_device_info_by_index(i))
# Note: permission needed to record from mic
# DBNBeatTracker online --device 1
from madmom.features.beats import DBNBeatTrackingProcessor, RNNBeatProcessor
from madmom.models import BEATS_LSTM
from madmom.processors import IOProcessor, process_online

# kwargs = dict(
#     fps = 100,
#     correct = True,
#     infile = None,
#     outfile = None,
#     max_bpm = 170,
#     min_bpm = 10,
#     nn_files =  [BEATS_LSTM[0], BEATS_LSTM[1], BEATS_LSTM[2],  BEATS_LSTM[3], BEATS_LSTM[4]],
#     num_frames = 1,
#     online = True,
#     list_stream_input_device = False,
#     device = 1
#     #verbose = 1
# )

# def beat_callback(beats, output=None):
#     if beats.size > 0:
#         print(beats)

# in_processor = RNNBeatProcessor(**kwargs)
# beat_processor = DBNBeatTrackingProcessor(**kwargs)
# out_processor = [beat_processor, beat_callback]
# processor = IOProcessor(in_processor, out_processor)
# process_online(processor, **kwargs)
def get_beats(file):
    kwargs = dict(
        fps = 100,
        correct = True,
        infile = file,
        outfile = None,
        max_bpm = 170,
        min_bpm = 10,
        nn_files =  [BEATS_LSTM[0]],
        num_frames = 1,
        online = False
        #verbose = 1
    )

    # def beat_callback(beats, output=None):
    #     if beats.size > 0:
    #         print(beats)

    # in_processor = RNNBeatProcessor()
    # file_intake = in_processor(file)
    # print("past file_intake")
    # beat_processor = DBNBeatTrackingProcessor(**kwargs)
    # print("beats processing started")
    # beats = beat_processor(file_intake)
    # print(beats)


    proc = DBNBeatTrackingProcessor(fps=100)
    act = RNNBeatProcessor()(file)
    beats = proc(act)
    # print(beats)
    for beat in beats:
        print(f"MADMOM beat time: {beat}s")
    
    return beats

beat_times_madmom = get_beats(file)
import numpy as np
print(np.array_equiv(beat_times_librosa, beat_times_madmom))


# IDEAS: 
# 1) Check whether chords-recognition (second repo I found) detects more types of chords better. Print all the chords to terminal as well, add timestamping and also storage
# ^ It does (major 7th chords, bass notess). Might train on more chords (for complex playing)?
# 2) ~~Combine with MADMOM to pick out certain notes and detect other chords (this is basically templating, like done by chord-recognition (first one))~~
# ^ Too much work but maybe?
# 3) Create a PYAUDIO w/ CHORDINO collab, since CHORDINO can detect lots of chords, following design pattern of other PYAUDIO + 1 algos

# NEXT STEPS: 
# Look into 1 and 3
# Create script that combines beat detection with chord-recognition repo (easy version, only major and minor chords)
# Include timestamping, printing to terminal and to a new file whose updates could be viewed in real time?