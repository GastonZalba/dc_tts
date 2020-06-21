import librosa
import glob
import os
import re
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
import soundfile as sf
import unicodedata


import speech_recognition as sr
r = sr.Recognizer()


# folders
inputFolder = "moria"
tmpFolder = inputFolder + "/_tmp"  # for audio Chunks
outputFolder = "../voces_procesadas/{}/data/".format(inputFolder)

# merge files upon this seconds
maxduration = 7

# output files
outrate = 22050

# split_on_silence
min_silence_len = 200
silence_thresh = -16
keep_silence = 200


def splitFilesBySilence():
    exclude = set(['_tmp'])
    for dirpath, subdirs, files in os.walk(inputFolder, topdown=True):
        subdirs[:] = [d for d in subdirs if d not in exclude]
        for file in files:
            fileName = clean_filename(file)
            split(os.path.join(dirpath, file), fileName)


def mergePieces():
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

                if mixDuration <= maxduration:
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

                writeTranscript(dir, fileOutput, duration, outfile)

            print('Total files:', len(data))


def createTranscript():
    if not os.path.exists(outputFolder):
        os.makedirs(
            outputFolder)  # create output folder
    file = open(outputFolder + '/transcript.txt', 'w')
    file.close()
    print('transcript.txt creado.')


def writeTranscript(dir, fileOutput, duration, outfile):

    with sr.AudioFile(outfile) as source:
        audio_text = r.listen(source)

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text, language='es-AR')
            print(text)

        except:
            text = '*' # valor por defecto si no se pudo decodificar el texto
            print('No se pudo reconocer el audio')

        finally:
            line = dir.replace(" ", "_") + '/' + fileOutput + '|'  # file
            line += text + '|' # transcript 1
            line += text + '|' # transcript 2
            line += str(duration) # length in seconds
            line += "\n"
            file = open(outputFolder + '/transcript.txt', 'a')
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

    if not os.path.exists(tmpFolder):
        os.makedirs(tmpFolder)  # create tmp folder
    if not os.path.exists(tmpSubfolder):
        os.makedirs(tmpSubfolder)  # create output subfolder

    print('Created folder ', fileName)
    print('Splitted in', len(chunks), 'chunks')

    for i, chunk in enumerate(chunks):
        chunk.export(tmpFolder + '/' + fileName + '/' +
                     fileName + "_{:04d}.wav".format(i), format="wav")

# Remove accents, whitespaces and Uppercases


def clean_filename(s):
    s = os.path.splitext(s)[0]
    return strip_accents(s).replace(" ", "_").lower()


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


splitFilesBySilence()
mergePieces()
print('Done')
