"""ALI - your personal JARVIS-style assistant.

  python main.py          -> text chat
  python main.py --voice  -> say "Ali, ..." out loud (needs microphone)
"""
import sys

from ali.brain import Ali
from ali.config import OWNER

WAKE = "ali"


def text_mode(ali):
    print(f"ALI online. Good to see you, {OWNER}. (type 'exit' to quit)\n")
    while True:
        try:
            msg = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not msg:
            continue
        if msg.lower() in ("exit", "quit", "bye"):
            break
        print("Ali:", ali.ask(msg), "\n")
    print("Ali: Powering down. Goodbye.")


def voice_mode(ali):
    from ali.voice import Voice

    v = Voice()
    v.speak(f"Ali online. Say my name when you need me, {OWNER}.")
    print(f'Listening... say "{WAKE}" followed by your request. Ctrl+C to quit.')
    try:
        while True:
            heard = v.listen()
            if not heard:
                continue
            low = heard.lower()
            print("Heard:", heard)
            if WAKE not in low.split() and not low.startswith(WAKE):
                continue
            cmd = low.split(WAKE, 1)[1].strip(" ,.") if WAKE in low else low
            if not cmd:
                v.speak("Yes?")
                cmd = v.listen()
                if not cmd:
                    continue
            if cmd in ("exit", "quit", "goodbye", "shut down"):
                v.speak("Powering down. Goodbye.")
                break
            reply = ali.ask(cmd)
            print("Ali:", reply)
            v.speak(reply)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    try:
        brain = Ali()
    except RuntimeError as e:
        print(e)
        sys.exit(1)
    voice_mode(brain) if "--voice" in sys.argv else text_mode(brain)
