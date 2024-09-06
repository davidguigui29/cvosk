#include <vosk_api.h>
#include <stdlib.h>
#include <string.h>

// Define a struct to hold the KaldiRecognizer
typedef struct {
    VoskRecognizer *recognizer;
} KaldiRecognizer;

// Function to create a new KaldiRecognizer
KaldiRecognizer* KaldiRecognizer_new(VoskModel *model, float sample_rate) {
    KaldiRecognizer *recognizer = (KaldiRecognizer*)malloc(sizeof(KaldiRecognizer));
    if (!recognizer) return NULL;
    
    recognizer->recognizer = vosk_recognizer_new(model, sample_rate);
    if (recognizer->recognizer == NULL) {
        free(recognizer);
        return NULL;
    }
    
    return recognizer;
}

// Function to create a new KaldiRecognizer with a speaker model
KaldiRecognizer* KaldiRecognizer_new_spk(VoskModel *model, float sample_rate, VoskSpkModel *spk_model) {
    KaldiRecognizer *recognizer = (KaldiRecognizer*)malloc(sizeof(KaldiRecognizer));
    if (!recognizer) return NULL;

    recognizer->recognizer = vosk_recognizer_new_spk(model, sample_rate, spk_model);
    if (recognizer->recognizer == NULL) {
        free(recognizer);
        return NULL;
    }
    
    return recognizer;
}

// Function to create a new KaldiRecognizer with a grammar
KaldiRecognizer* KaldiRecognizer_new_grm(VoskModel *model, float sample_rate, const char *grammar) {
    KaldiRecognizer *recognizer = (KaldiRecognizer*)malloc(sizeof(KaldiRecognizer));
    if (!recognizer) return NULL;

    recognizer->recognizer = vosk_recognizer_new_grm(model, sample_rate, grammar);
    if (recognizer->recognizer == NULL) {
        free(recognizer);
        return NULL;
    }

    return recognizer;
}

// Function to free a KaldiRecognizer
void KaldiRecognizer_free(KaldiRecognizer *recognizer) {
    if (recognizer) {
        if (recognizer->recognizer) {
            vosk_recognizer_free(recognizer->recognizer);
        }
        free(recognizer);
    }
}

// Function to set the maximum number of alternatives
void KaldiRecognizer_set_max_alternatives(KaldiRecognizer *recognizer, int max_alternatives) {
    if (recognizer && recognizer->recognizer) {
        vosk_recognizer_set_max_alternatives(recognizer->recognizer, max_alternatives);
    }
}

// Function to enable or disable words
void KaldiRecognizer_set_words(KaldiRecognizer *recognizer, int enable_words) {
    if (recognizer && recognizer->recognizer) {
        vosk_recognizer_set_words(recognizer->recognizer, enable_words);
    }
}

// Function to enable or disable partial words
void KaldiRecognizer_set_partial_words(KaldiRecognizer *recognizer, int enable_partial_words) {
    if (recognizer && recognizer->recognizer) {
        vosk_recognizer_set_partial_words(recognizer->recognizer, enable_partial_words);
    }
}

// Function to enable or disable NLSML
void KaldiRecognizer_set_nlsml(KaldiRecognizer *recognizer, int enable_nlsml) {
    if (recognizer && recognizer->recognizer) {
        vosk_recognizer_set_nlsml(recognizer->recognizer, enable_nlsml);
    }
}

// Function to set the speaker model
void KaldiRecognizer_set_spk_model(KaldiRecognizer *recognizer, VoskSpkModel *spk_model) {
    if (recognizer && recognizer->recognizer) {
        vosk_recognizer_set_spk_model(recognizer->recognizer, spk_model);
    }
}

// Function to set the grammar
void KaldiRecognizer_set_grm(KaldiRecognizer *recognizer, const char *grammar) {
    if (recognizer && recognizer->recognizer) {
        vosk_recognizer_set_grm(recognizer->recognizer, grammar);
    }
}

// Function to accept waveform data
void KaldiRecognizer_accept_waveform(KaldiRecognizer *recognizer, const char *data, int length) {
    if (recognizer && recognizer->recognizer) {
        vosk_recognizer_accept_waveform(recognizer->recognizer, data, length);
    }
}

// Function to get the result
const char* KaldiRecognizer_result(KaldiRecognizer *recognizer) {
    if (recognizer && recognizer->recognizer) {
        return vosk_recognizer_result(recognizer->recognizer);
    }
    return NULL;
}

// Function to get the partial result
const char* KaldiRecognizer_partial_result(KaldiRecognizer *recognizer) {
    if (recognizer && recognizer->recognizer) {
        return vosk_recognizer_partial_result(recognizer->recognizer);
    }
    return NULL;
}

// Function to get the final result
const char* KaldiRecognizer_final_result(KaldiRecognizer *recognizer) {
    if (recognizer && recognizer->recognizer) {
        return vosk_recognizer_final_result(recognizer->recognizer);
    }
    return NULL;
}

// Function to reset the recognizer
void KaldiRecognizer_reset(KaldiRecognizer *recognizer) {
    if (recognizer && recognizer->recognizer) {
        vosk_recognizer_reset(recognizer->recognizer);
    }
}



