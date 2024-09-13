# Speech to text (STT) model 

import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import os
import threading
import click
import torch
import numpy as np
from pywinauto import application
import re
from datetime import timedelta
from datetime import datetime
import pywhatkit
import keyboard


# original repo
# https://github.com/mallorbc/whisper_mic/blob/main/mic.py
# default language now is English and model is tiny

@click.command()
@click.option("--write_place_notepad", default=False,
              help="where to write on notepad or everywhere default every where", is_flag=True, type=bool)
@click.option("--model", default="base", help="Model to use",
              type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--english", default=True, help="Whether to use English model", is_flag=True, type=bool)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True, type=bool)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False, is_flag=True, help="Flag to enable dynamic energy", type=bool)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--save_file", default=False, help="Flag to save file", is_flag=True, type=bool)
def main(model, english, verbose, energy, pause, dynamic_energy, save_file, write_place_notepad):
    # write to a file

    temp_dir = tempfile.mkdtemp() if save_file else None
    # there are no english models for large
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()
    threading.Thread(target=record_audio,
                     args=(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir)).start()
    threading.Thread(target=transcribe_forever,
                     args=(
                     audio_queue, result_queue, audio_model, english, verbose, save_file, write_place_notepad)).start()
    # while True:
    #     start = time.time()
    #    # print(result_queue.get())
    #     # print (time.time() - start )

    #    f1 = open("D:\\Dr Azad ai\\userr STT.txt", 'a')
    #   f1.write(result_queue.get()+ "\n")
    # f1.close()


def record_audio(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir):
    # load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        i = 0
        while True:
            # get and save audio to wav file
            audio = r.listen(source)
            if save_file:
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                filename = os.path.join(temp_dir, f"temp{i}.wav")
                audio_clip.export(filename, format="wav")
                audio_data = filename
            else:
                torch_audio = torch.from_numpy(
                    np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio

            audio_queue.put_nowait(audio_data)
            i += 1


def convert_action(word):
    word = word.lower()
    action = ""

    if "today" in word:
        date = str(datetime.today())
        word = (word.replace("today", date))

    elif "yesterday" in word:
        yesterday = str(datetime.today() - timedelta(days=1))
        word = (word.replace("yesterday", yesterday))

    elif "tomorrow" in word:
        yesterday = str(datetime.today() - timedelta(days=-1))
        word = (word.replace("tomorrow", yesterday))

    elif "next line" in word:
        word = (word.replace("next line", "\n"))

    elif "new paragraph" in word:
        word = (word.replace("new paragraph", "\n\n"))

    elif "space" in word:
        word = (word.replace("space", " "))

    elif "number" in word:
        word = (word.replace("number", "#"))

    # elif "stop dictation" in word:
    #     action = "turn off the mic"

    elif "period" in word:
        word = (word.replace("period", "."))


    elif "music" in word:
        word.replace("music", "")
        pywhatkit.playonyt(word)

    elif "message" in word:

        word.replace("whatsapp", "")
        number = word
        pywhatkit.sendwhatmsg(number, "Hello from our new system ", 4, 39)



    elif "question mark" in word or "questionmark" in word:
        word = (word.replace("question mark", "?").replace("questionmark", "?"))

    # elif "letter" in word:
    #     print(word.replace("letter", ""))

    return word


def transcribe_forever(audio_queue, result_queue, audio_model, english, verbose, save_file, write_place_notepad):
    # https://dev.to/duncandegwa/automating-notepad-and-excel-applications-in-python-28nh
    # https://python-forum.io/thread-17735.html\

    fileObject = open("D:\\DoctorAI\\DocAi_STT\\diagnoses_symptoms_drugs.txt", "r")
    # data = fileObject.read().split("\n")
    data = " ".join(fileObject.read().split("\n"))

    if write_place_notepad:
        app = application.Application(backend="uia").start("notepad.exe")  # open notepad app
    while True:
        audio_data = audio_queue.get()

        if english:
            result = audio_model.transcribe(audio_data, language='english', fp16=False, initial_prompt=data)
        #        f1.write( "text")
        else:
            result = audio_model.transcribe(audio_data, fp16=False)
        #        f1.write("text")

        if not verbose:
            # changing the selection to remove the dot [:-1]
            predicted_text = result["text"]
            predicted_text = re.sub(r'[^\w\s]', '', predicted_text)
            predicted_text = convert_action(predicted_text)
            predicted_text = (predicted_text).title()
            result_queue.put_nowait(predicted_text)
            if write_place_notepad:
                app.UntitledNotepad.type_keys(predicted_text, with_spaces=True)
                keyboard.send_keys('{ENTER}')
            else:
                keyboard.write(predicted_text)
                # keyboard.send_keys(predicted_text ,  with_spaces = True)
        #  f1.write(predicted_text)

        else:
            # [:-1]
            predicted_text = result["text"]
            predicted_text = re.sub(r'[^\w\s]', '', predicted_text)

            predicted_text = convert_action(predicted_text)
            predicted_text = predicted_text.title()

            result_queue.put_nowait(predicted_text)
            if write_place_notepad:
                app.UntitledNotepad.type_keys(predicted_text, with_spaces=True)
                keyboard.send_keys('{ENTER}')
            else:
                keyboard.write(predicted_text)
                # keyboard.send_keys(predicted_text, with_spaces=True)

        # f1.write(result)

        if save_file:
            os.remove(audio_data)


if __name__ == "__main__":
    main()
