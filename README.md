# MusicGPT

Generate raw MIDI with GPT-3.5

## Table of Contents

- [MusicGPT](#musicgpt)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Technologies](#technologies)
  - [Getting Started](#getting-started)
  - [The prompt](#the-prompt)
  - [Usage](#usage)

## Overview

This project creates MIDI files using GPT-3.5's few-shot learning capabilities. We establish a text-midi format that we convert both to and from, then supply the model with a prompt that includes key information, including example MIDI patterns as well as the output's format and desired mood and feel. The model then generates text output that we convert back to MIDI.

This model is not trained on the specific task, meaning the output is questionable at best. As such, this is mostly a proof-of-concept and should not be used.

## Technologies

This project is created with:

- [musthe](https://github.com/gciruelos/musthe): ^1.0.0
- [mido](https://pypi.org/project/mido/): ^1.3.2
- [GPT4Free](https://github.com/xtekky/gpt4free): ^0.2.9.8
  
## Getting Started

To get a local copy up and running follow these simple steps:

Clone the Repo \
```git clone https://github.com/Pop101/MIDIGPT```

Enter the repo and Install requirements \
```cd MIDIGPT && poetry install```

Run the project \
```poetry run python gpt.py```

## The prompt

Your prompt is automatically wrapped with the following text:

```
You are midiAI, an assistant designed to output MIDI for use in digital audio workstations. When given a prompt consisting of a mood and feel, output midi notes in the following format:
note, duration in beats, start beat

For example, a trap piano pattern would look like this:
<Example Midi>

Ensure output consists only of that format. Anything that isn't Note,duration,start beat will result in an error.
Patterns should be musically appealing and variated. Write in 4/4 time and only for a single instrument at a time.
You can extend existing patterns, write chord progressions, variate existing patterns or progressions, and any other functionality to create new music.

Make sure your output is always at least 4 bars (16 beats) long.
All music generated should be original and end on a tonic note or be loopable.

<Your prompt>
```

Feel free to add any additional information to your prompt, but make sure to include the mood and feel of the music you want to generate. If you find a preset that works better, submit a [pull request](https://github.com/Pop101/MIDIGPT/pulls)!

## Usage

```
usage: gpt.py [-h] [-i INPUT] [-o OUTPUT_DIR] [-p] [-r REPETITIONS] [prompt ...]

Prompt the AI to generate MIDI!

positional arguments:
  prompt                The prompt to give the AI

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to a MIDI file to use as an example pattern
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Path to save the output MIDI file
  -p, --print           Print raw LLM output to stdout
  -r REPETITIONS, --repetitions REPETITIONS
                        Number of times to repeat each prompt
```
