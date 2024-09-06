import ctypes as _ctypes
import json
import srt
import datetime
import os
import requests
from pathlib import Path
from tqdm import tqdm
from urllib.request import urlretrieve

# Define constants for model directories and URLs
MODEL_DIRS = ['models']  # Update this list with your actual model directories
MODEL_LIST_URL = 'https://api.example.com/models'  # Update with your actual model list URL
MODEL_PRE_URL = 'https://api.example.com/download/'  # Update with your actual model download URL

# Load the shared library
# _lib = _ctypes.CDLL('libvosk_recognizer.so')
_lib = _ctypes.CDLL('./vosk_lab/c/libvosk_recognizer.so')


# Define the C function prototypes for Model
_lib.vosk_model_new.argtypes = [_ctypes.c_char_p]
_lib.vosk_model_new.restype = _ctypes.c_void_p

_lib.vosk_model_free.argtypes = [_ctypes.c_void_p]
_lib.vosk_model_free.restype = None

_lib.vosk_model_find_word.argtypes = [_ctypes.c_void_p, _ctypes.c_char_p]
_lib.vosk_model_find_word.restype = _ctypes.c_int

# Define the C function prototypes for KaldiRecognizer
_lib.vosk_recognizer_new.argtypes = [_ctypes.c_void_p, _ctypes.c_float]
_lib.vosk_recognizer_new.restype = _ctypes.c_void_p

_lib.vosk_recognizer_new_spk.argtypes = [_ctypes.c_void_p, _ctypes.c_float, _ctypes.c_void_p]
_lib.vosk_recognizer_new_spk.restype = _ctypes.c_void_p

_lib.vosk_recognizer_new_grm.argtypes = [_ctypes.c_void_p, _ctypes.c_float, _ctypes.c_char_p]
_lib.vosk_recognizer_new_grm.restype = _ctypes.c_void_p

_lib.vosk_recognizer_free.argtypes = [_ctypes.c_void_p]
_lib.vosk_recognizer_free.restype = None

_lib.vosk_recognizer_set_max_alternatives.argtypes = [_ctypes.c_void_p, _ctypes.c_int]
_lib.vosk_recognizer_set_max_alternatives.restype = None

_lib.vosk_recognizer_set_words.argtypes = [_ctypes.c_void_p, _ctypes.c_int]
_lib.vosk_recognizer_set_words.restype = None

_lib.vosk_recognizer_set_partial_words.argtypes = [_ctypes.c_void_p, _ctypes.c_int]
_lib.vosk_recognizer_set_partial_words.restype = None

_lib.vosk_recognizer_set_nlsml.argtypes = [_ctypes.c_void_p, _ctypes.c_int]
_lib.vosk_recognizer_set_nlsml.restype = None

_lib.vosk_recognizer_set_spk_model.argtypes = [_ctypes.c_void_p, _ctypes.c_void_p]
_lib.vosk_recognizer_set_spk_model.restype = None

_lib.vosk_recognizer_set_grm.argtypes = [_ctypes.c_void_p, _ctypes.c_char_p]
_lib.vosk_recognizer_set_grm.restype = None

_lib.vosk_recognizer_accept_waveform.argtypes = [_ctypes.c_void_p, _ctypes.c_char_p, _ctypes.c_int]
_lib.vosk_recognizer_accept_waveform.restype = _ctypes.c_int

_lib.vosk_recognizer_result.argtypes = [_ctypes.c_void_p]
_lib.vosk_recognizer_result.restype = _ctypes.c_char_p

_lib.vosk_recognizer_partial_result.argtypes = [_ctypes.c_void_p]
_lib.vosk_recognizer_partial_result.restype = _ctypes.c_char_p

_lib.vosk_recognizer_final_result.argtypes = [_ctypes.c_void_p]
_lib.vosk_recognizer_final_result.restype = _ctypes.c_char_p

_lib.vosk_recognizer_reset.argtypes = [_ctypes.c_void_p]
_lib.vosk_recognizer_reset.restype = None

# Model class
class Model:
    def __init__(self, model_path=None, model_name=None, lang=None):
        if model_path is not None:
            self._handle = _lib.vosk_model_new(model_path.encode("utf-8"))
        else:
            model_path = self.get_model_path(model_name, lang)
            self._handle = _lib.vosk_model_new(model_path.encode("utf-8"))
        
        if self._handle == _ctypes.c_void_p():
            raise Exception("Failed to create a model")

    def __del__(self):
        if hasattr(self, '_handle'):
            _lib.vosk_model_free(self._handle)

    def vosk_model_find_word(self, word):
        return _lib.vosk_model_find_word(self._handle, word.encode("utf-8"))

    def get_model_path(self, model_name, lang):
        if model_name is None:
            model_path = self.get_model_by_lang(lang)
        else:
            model_path = self.get_model_by_name(model_name)
        return str(model_path)

    def get_model_by_name(self, model_name):
        for directory in MODEL_DIRS:
            if directory is None or not Path(directory).exists():
                continue
            model_file_list = os.listdir(directory)
            model_file = [model for model in model_file_list if model == model_name]
            if model_file:
                return Path(directory, model_file[0])
        
        response = requests.get(MODEL_LIST_URL, timeout=10)
        result_model = [model["name"] for model in response.json() if model["name"] == model_name]
        if not result_model:
            print(f"Model name {model_name} does not exist")
            sys.exit(1)
        else:
            self.download_model(Path(directory, result_model[0]))
            return Path(directory, result_model[0])

    def get_model_by_lang(self, lang):
        for directory in MODEL_DIRS:
            if directory is None or not Path(directory).exists():
                continue
            model_file_list = os.listdir(directory)
            model_file = [model for model in model_file_list if
                    re.match(r"vosk-model(-small)?-{}".format(lang), model)]
            if model_file:
                return Path(directory, model_file[0])
        
        response = requests.get(MODEL_LIST_URL, timeout=10)
        result_model = [model["name"] for model in response.json() if
                model["lang"] == lang and model["type"] == "small" and model["obsolete"] == "false"]
        if not result_model:
            print(f"Language {lang} does not exist")
            sys.exit(1)
        else:
            self.download_model(Path(directory, result_model[0]))
            return Path(directory, result_model[0])

    def download_model(self, model_name):
        if not (model_name.parent).exists():
            (model_name.parent).mkdir(parents=True)
        with tqdm(unit="B", unit_scale=True, unit_divisor=1024, miniters=1,
                desc=(MODEL_PRE_URL + str(model_name.name) + ".zip").rsplit("/",
                    maxsplit=1)[-1]) as t:
            reporthook = self.download_progress_hook(t)
            urlretrieve(MODEL_PRE_URL + str(model_name.name) + ".zip",
                    str(model_name) + ".zip", reporthook=reporthook, data=None)
            t.total = t.n
            with ZipFile(str(model_name) + ".zip", "r") as model_ref:
                model_ref.extractall(model_name.parent)
            Path(str(model_name) + ".zip").unlink()

    def download_progress_hook(self, t):
        last_b = [0]
        def update_to(b=1, bsize=1, tsize=None):
            if tsize not in (None, -1):
                t.total = tsize
            displayed = t.update((b - last_b[0]) * bsize)
            last_b[0] = b
            return displayed
        return update_to

# KaldiRecognizer class
class KaldiRecognizer:
    def __init__(self, model, sample_rate, spk_model=None, grammar=None):
        if spk_model:
            self._handle = _lib.vosk_recognizer_new_spk(model._handle, sample_rate, spk_model._handle)
        elif grammar:
            self._handle = _lib.vosk_recognizer_new_grm(model._handle, sample_rate, grammar.encode('utf-8'))
        else:
            self._handle = _lib.vosk_recognizer_new(model._handle, sample_rate)
        
        if not self._handle:
            raise Exception("Failed to create KaldiRecognizer")

    def __del__(self):
        if hasattr(self, '_handle'):
            _lib.vosk_recognizer_free(self._handle)

    def SetMaxAlternatives(self, max_alternatives):
        _lib.vosk_recognizer_set_max_alternatives(self._handle, max_alternatives)

    def SetWords(self, enable_words):
        _lib.vosk_recognizer_set_words(self._handle, 1 if enable_words else 0)

    def SetPartialWords(self, enable_partial_words):
        _lib.vosk_recognizer_set_partial_words(self._handle, 1 if enable_partial_words else 0)

    def SetNLSML(self, enable_nlsml):
        _lib.vosk_recognizer_set_nlsml(self._handle, 1 if enable_nlsml else 0)

    def SetSpkModel(self, spk_model):
        _lib.vosk_recognizer_set_spk_model(self._handle, spk_model._handle)

    def SetGrammar(self, grammar):
        _lib.vosk_recognizer_set_grm(self._handle, grammar.encode('utf-8'))

    def AcceptWaveform(self, data):
        res = _lib.vosk_recognizer_accept_waveform(self._handle, data, len(data))
        if res < 0:
            raise Exception("Failed to process waveform")
        return res

    def Result(self):
        return _ctypes.string_at(_lib.vosk_recognizer_result(self._handle)).decode('utf-8')

    def PartialResult(self):
        return _ctypes.string_at(_lib.vosk_recognizer_partial_result(self._handle)).decode('utf-8')

    def FinalResult(self):
        return _ctypes.string_at(_lib.vosk_recognizer_final_result(self._handle)).decode('utf-8')

    def Reset(self):
        _lib.vosk_recognizer_reset(self._handle)

    def SrtResult(self, stream, words_per_line=7):
        results = []

        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if self.AcceptWaveform(data):
                results.append(self.Result())
        results.append(self.FinalResult())

        subs = []
        for res in results:
            jres = json.loads(res)
            if not "result" in jres:
                continue
            words = jres["result"]
            for j in range(0, len(words), words_per_line):
                line = words[j : j + words_per_line]
                s = srt.Subtitle(index=len(subs),
                        content=" ".join([l["word"] for l in line]),
                        start=datetime.timedelta(seconds=line[0]["start"]),
                        end=datetime.timedelta(seconds=line[-1]["end"]))
                subs.append(s)

        return srt.compose(subs)

# Example usage:
# model = Model(model_path="path_to_model")
# recognizer = KaldiRecognizer(model, 16000)
# recognizer.SetWords(True)
# recognizer.AcceptWaveform(audio_data)
# print(recognizer.Result())




