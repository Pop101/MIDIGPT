from musthe import Note
from mido import MidiFile, MidiTrack, Message
import logging

def txt_to_midi(txt: str) -> MidiFile:
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    absolute_time_messages = list()
    for line in txt.strip().split("\n"):
        try:
            note, duration, start_beat = list(map(str.strip, line.split(",")))[0:3]
            note = Note(note)
            duration = float(duration)
            start_beat = float(start_beat)

            absolute_time_messages.append(("note_on", note.midi_note(), int(start_beat * mid.ticks_per_beat)))
            absolute_time_messages.append(
                ("note_off", note.midi_note(), int((start_beat + duration) * mid.ticks_per_beat))
            )
        except Exception as e:
            # Most likely a ValueError from the split or int conversion,
            # Try to recover by logging the error and skipping the line
            logging.error(f"Error processing line: {line} ({e})")

    # Convert absolute time to midi
    time = 0
    for msg_type, note, abstime in sorted(absolute_time_messages, key=lambda x: x[2]):
        delta_time = abstime - time
        if msg_type == "note_on":
            track.append(Message("note_on", note=note, velocity=64, time=delta_time))
        elif msg_type == "note_off":
            track.append(Message("note_off", note=note, velocity=64, time=delta_time))
        time = abstime

    return mid

if __name__ == "__main__":
    txt = """
        G, 1, 1
        C, 1, 2
        Eb, 1, 3
        F, 2, 4
        G, 1, 6
        C, 1, 7
        Eb, 1, 8
        F, 2, 9
        G, 1, 11
        C, 1, 12
        Eb, 1, 13
        F, 2, 14
        G, 1, 16
        C, 1, 17
        Eb, 1, 18
        F, 2, 19
    """
    
    file = txt_to_midi(txt)
    file.save("output.mid")