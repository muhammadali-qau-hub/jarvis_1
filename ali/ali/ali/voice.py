"""Optional voice: microphone in, speaker out."""
import pyttsx3
import speech_recognition as sr


class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.rec = sr.Recognizer()
        self.rec.pause_threshold = 0.8
        self.mic = sr.Microphone()
        with self.mic as src:
            self.rec.adjust_for_ambient_noise(src, duration=1)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=8, phrase_limit=15):
        """Returns recognised text, or '' if nothing understood."""
        with self.mic as src:
            try:
                audio = self.rec.listen(src, timeout=timeout, phrase_time_limit=phrase_limit)
            except sr.WaitTimeoutError:
                return ""
        try:
            return self.rec.recognize_google(audio)
        except (sr.UnknownValueError, sr.RequestError):
            return ""
