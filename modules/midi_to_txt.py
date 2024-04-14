from musthe import Note
from mido import MidiFile

# We need to be able to convert a midi note to a musthe Note
note_mapping = {
    n.midi_note(): n
    for n in Note.all(min_octave=0, max_octave=8)
    if 0 <= n.midi_note() <= 127
}


def midi_to_txt(file: MidiFile) -> list[str]:
    """Convert a MidiFile to a list of strings in the format:
    note, duration in beats, start beat
    
    Each track will be a separate string in the list.
    """
    track_notes = dict()
    for i, track in enumerate(file.tracks):
        track_notes[i] = list()

        curr_beat = 0
        curr_pressed_notes = dict()  # note -> start beat
        for msg in track:
            if msg.type == "note_on":
                if msg.note not in curr_pressed_notes:
                    curr_pressed_notes[msg.note] = curr_beat

            if msg.type == "note_off":
                if msg.note in curr_pressed_notes:
                    start_beat = curr_pressed_notes[msg.note]
                    track_notes[i].append(
                        (note_mapping[msg.note], start_beat, curr_beat)
                    )
                    del curr_pressed_notes[msg.note]

            curr_beat += round(msg.time / file.ticks_per_beat)

        # Push all remaining notes
        for note, start_beat in curr_pressed_notes.items():
            track_notes[i].append((note_mapping[note], start_beat, curr_beat))

    # Convert each track's list to string
    all_track_notes = list()
    for _, notes in track_notes.items():
        track_notes = str()
        for note, start_beat, end_beat in sorted(notes, key=lambda x: x[1]):
            if end_beat - start_beat > 0:
                track_notes += f"{note}, {end_beat - start_beat}, {start_beat}\n"
        all_track_notes.append(track_notes)
    return all_track_notes
