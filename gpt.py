from g4f.client import Client
from modules.midi_to_txt import midi_to_txt
from modules.txt_to_midi import txt_to_midi
from mido import MidiFile
from textwrap import dedent

# Construct the prompt
def create_prompt(input_: str, example:str):
    return dedent(f"""
    You are midiAI, an assistant designed to output MIDI for use in digital audio workstations. When given a prompt consisting of a mood and feel, output midi notes in the following format:
    note, duration in beats, start beat

    For example, a trap piano pattern would look like this:
    {midi_to_txt(MidiFile(example))[0]}

    Ensure output consists only of that format. Anything that isn't Note,duration,start beat will result in an error.
    Patterns should be musically appealing and variated. Write in 4/4 time and only for a single instrument at a time.
    You can extend existing patterns, write chord progressions, variate existing patterns or progressions, and any other functionality to create new music.
    
    Make sure your output is always at least 4 bars (16 beats) long.
    All music generated should be original and end on a tonic note or be loopable.
    {input_}
    """).replace('    ', '')
    
def str_to_filename(s: str) -> str:
    s = s.replace(" ", "_")
    return "".join([c for c in s if c.isalnum() or c in "_-"])

client = Client()

if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys, os
    
    parser = ArgumentParser(description="Prompt the AI to generate MIDI!")
    parser.add_argument("-i", "--input", help="Path to a MIDI file to use as an example pattern", default="./midi/Trap Piano 01.mid")
    parser.add_argument("-o", "--output-dir", help="Path to save the output MIDI file", default="./")
    parser.add_argument("-p", "--print", help="Print raw LLM output to stdout", action="store_true")
    parser.add_argument("-r", "--repetitions", help="Number of times to repeat each prompt", type=int, default=1)
    parser.add_argument("prompt", nargs="*", help="The prompt to give the AI")
    args = parser.parse_args()
    
    # Construct the prompt
    iterator = [' '.join(args.prompt)] if args.prompt else sys.stdin
    for line in iterator:
        prompt = create_prompt(line, args.input)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        
        # Get X iterations of the output and save to midi
        for i in range(args.repetitions):
            output = response.choices[i].message.content
            
            if args.print:
                print(response.choices[i].message.content)
            
            filename = str_to_filename(line)
            if args.repetitions > 1:
                filename += f"-{i}"
            
            mid = txt_to_midi(response.choices[i].message.content)
            mid.save(os.path.join(args.output_dir, f"{filename}.mid"))
    