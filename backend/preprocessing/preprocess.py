# -*-coding:utf-8 -*-
import os
import pretty_midi
from config import *

seperate_power = 32

def extract_drum(midi_dir, f):
    global seperate_power
    midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + f)
    extracted_drum = pretty_midi.PrettyMIDI()
    generated_drum = pretty_midi.Instrument(program=0)
    generated_drum.is_drum = True

    drums = []
    for inst in midi_data.instruments:
        if inst.is_drum:
            drums.append(inst)
    
    beats = midi_data.get_downbeats()
    for i in range(len(beats)-1):
        start = beats[i]
        end = beats[i+1]
        interval = float((end-start)) / seperate_power
        
        part = []
        for j in range(seperate_power):
            part.append(start)
            start += interval
        part.append(end)
        
        for time_i in range(len(part)-1):
            for drum in drums:
                for note in drum.notes:
                    if (note.start > part[time_i]) and (note.start < part[time_i+1]):
                        new_note = pretty_midi.Note(velocity=100,
                            pitch=note.pitch,
                            start=part[time_i],
                            end=part[time_i]+.3)
                        generated_drum.notes.append(new_note)

    extracted_drum.instruments.append(generated_drum)
    extracted_drum.write('drum/' + f[:-4] + '.mid')


def drum_midi_to_text(midi_dir, f):
    global seperate_power

    midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + f)

    extracted_drum = pretty_midi.PrettyMIDI()
    generated_drum = pretty_midi.Instrument(program=0)
    generated_drum.is_drum = True

    fd = open('./drum/'+f[:-4]+'.txt', 'w')
    drums = []
    for inst in midi_data.instruments:
        if inst.is_drum:
            drums.append(inst)
    
    beats = midi_data.get_downbeats()
    for i in range(len(beats)-1):
        start = beats[i]
        end = beats[i+1]
        interval = float((end-start)) / seperate_power
        
        part = []
        for j in range(seperate_power):
            part.append(start)
            start += interval
        part.append(end)
        
        for time_i in range(len(part)-1):
            text = '000000000'
            note_list = []
            for drum in drums:
                for note in drum.notes:
                    if (note.start > part[time_i]) and (note.start < part[time_i+1]):
                        note_list.append(note.pitch)

            for pitch in note_list:
                if pitch in drum_conversion:
                    note_list.append(drum_conversion[pitch])
                    note_list.remove(pitch)
            note_list = set(note_list)
            for pitch in note_list:
                if pitch in allowed_pitch:
                    new_note = pretty_midi.Note(velocity=100,
                        pitch=pitch,
                        start=part[time_i],
                        end=part[time_i]+.3)
                    generated_drum.notes.append(new_note)
                    idx = allowed_pitch.index(pitch)
                    lst = list(text)
                    lst[idx] = '1'
                    text = ''.join(lst)
            fd.write(text + ' ')

    extracted_drum.instruments.append(generated_drum)
    extracted_drum.write('drum/' + f[:-4] + '.mid')
    fd.close()


if __name__ == '__main__':
    if os.path.exists('./drum/') == False:
        os.makedirs('./drum/')
    if os.path.exists('./melody/') == False:
        os.makedirs('./melody/')
    if os.path.exists('./midi/') == False:
        os.makedirs('./midi/')
        print 'please input .mid files to ./midi directory!'
        exit()

    midi_dir = 'midi'
    midi_filenames = os.listdir(midi_dir)

    midi_filenames = [f for f in midi_filenames if f.endswith('.mid')]
    midi_filenames = [f for f in midi_filenames if os.path.getsize(midi_dir + '/' + f) != 0]

    for f in midi_filenames:
        extract_drum(midi_dir, f)
        drum_midi_to_text(midi_dir, f)

    print 'done! for %d files' % len(midi_filenames)