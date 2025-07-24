# Guitar-Song-Simplifier-Script
A WIP repo for scripts I'm building for a personal project focused on simplifying guitar songs.

The long-term goal is to develop a full-stack application.
A user will be able to upload any song, and have its timestamped chords and beats extracted and visualized as a roadmap, along with transcribed lyrics.
The user can then play their guitar along with the analyzed upload of the song, and have their own chords, times and beats processed in real time to see how well they match with the analyzed upload.

This is meant to be used a tool that makes it easier to learn and play a new song on guitar, especially in terms of syncing rhythm and singing.

To create virtual environment and install dependencies:

`python3.9 -m venv venv`

`source venv/bin/activate`

`pip install numpy==1.23.5`

`export PIP_NO_BUILD_ISOLATION=1`

`pip install -r requirements.txt`

Then move to the src directory and run:

python3 realtime_combo.py `/path/to/wav/file`

This will load in the .wav file provided in the 3rd argument, and process that audio file to extract the chord sequence, beat sequence and list of unique chords used in the song. Immediately after, real-time audio processing will begin. As the user plays their guitar, real-time beats and chords will be extracted and printed to the terminal, along with feedback characterizing whether beats/chords were on time/properly played.

Credits:
Inspiration taken from madmom, librosa and chords-recognition on GitHub
