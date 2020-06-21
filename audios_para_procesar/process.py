import librosa
import glob
import os
import sys

import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
import soundfile as sf
import unicodedata

import speech_recognition as sr
r = sr.Recognizer()

# merge files upon this seconds
max_duration = 10

# output files
outrate = 22050

# split_on_silence
min_silence_len = 200
silence_thresh = -16
keep_silence = 200

# use Google to convert speech to Text
speech_to_text = True
language = 'es-AR'

transcript_name = 'transcript.txt'


def splitFilesBySilence():

    print('File splitting started')

    exclude = set(['_tmp'])
    for dirpath, subdirs, files in os.walk(inputFolder, topdown=True):
        subdirs[:] = [d for d in subdirs if d not in exclude]
        for file in files:
            fileName = clean_filename(file)
            print('Splitted', fileName)
            split(os.path.join(dirpath, file), fileName)


def mergePieces():

    print('File merging started')

    createTranscript()

    for dirpath, subdirs, files in os.walk(tmpFolder):

        for dir in subdirs:

            outputSubfolder = outputFolder + dir
            infiles = glob.glob(tmpFolder + '/' + dir +
                                "/*.wav")  # wav files only
            data = [[]]
            durations = [[]]
            mixDuration = 0
            outputNum = 0

            for infile in infiles:

                duration = librosa.get_duration(filename=infile)
                mixDuration += duration

                y, sr = librosa.load(infile, sr=outrate,
                                     mono=True)  # Downsample

                if mixDuration <= max_duration:
                    data[outputNum] = np.append(data[outputNum], y)
                    durations[outputNum] = mixDuration
                else:
                    outputNum += 1
                    mixDuration = duration
                    data.append(np.append([], y))
                    durations.append(mixDuration)

            if not os.path.exists(outputSubfolder):
                os.makedirs(
                    outputSubfolder)  # create output subfolder

            for i, d in enumerate(data):
                duration = round(durations[i], 2)
                fileOutput = dir + "_{:04d}.wav".format(i)

                outfile = outputSubfolder + '/' + fileOutput

                sf.write(outfile, d, outrate, 'PCM_32')

                print('Created file', fileOutput)

                writeTranscript(dir, fileOutput, duration, outfile)

            print('Total files:', len(data))


def createTranscript():   
    file = open(outputFolder + '/' + transcript_name, 'w')
    file.close()
    print('Created transcript')


def speechToText(outfile):

    with sr.AudioFile(outfile) as source:
        audio_text = r.listen(source)

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text, language=language)
            print(text)

        except:
            text = '*' # valor por defecto si no se pudo decodificar el texto
            print('Speech not recognized')

        finally:
            return text


def writeTranscript(dir, fileOutput, duration, outfile):

    if speech_to_text:
        text = speechToText(outfile)
    else:
        text = '*'

    line = dir.replace(" ", "_") + '/' + fileOutput + '|'  # file
    line += text + '|' # transcript 1
    line += text + '|' # transcript 2
    line += str(duration) # length in seconds
    line += "\n"
    file = open(outputFolder + '/' + transcript_name, 'a')
    file.write(line)
    file.close()


def split(filepath, fileName):
    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(
        sound,

        # split on silences longer than
        min_silence_len=min_silence_len,

        # anything under this is considered silence
        silence_thresh=dBFS + silence_thresh,

        # keep ms of leading/trailing silence
        keep_silence=keep_silence
    )

    tmpSubfolder = tmpFolder + "/" + fileName
    if not os.path.exists(tmpSubfolder):
        os.makedirs(tmpSubfolder)  # create output subfolder

    print('Created folder', fileName)
    print('Splitted in', len(chunks), 'chunks')

    for i, chunk in enumerate(chunks):
        chunk.export(tmpFolder + '/' + fileName + '/' +
                     fileName + "_{:04d}.wav".format(i), format="wav")


inputFolder
tmpFolder
outpuFolder

def prepareFolders():
    global inputFolder
    global tmpFolder
    global outpuFolder

    inputFolder = str(sys.argv[1])
    
    if not os.path.exists(inputFolder):
        print('Folder not found')
        exit()

    tmpFolder = inputFolder + "/_tmp" # for audio Chunks
    outputFolder = "../voces_procesadas/{}/data/".format(inputFolder)
    
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)  # create output folder

    if not os.path.exists(tmpFolder):
        os.makedirs(tmpFolder)  # create tmp folder


# Remove accents, whitespaces and Uppercases
def clean_filename(s):
    s = os.path.splitext(s)[0]
    return strip_accents(s).replace(" ", "_").lower()


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


prepareFolders()
splitFilesBySilence()
mergePieces()
print('Done')