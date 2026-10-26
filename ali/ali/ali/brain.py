import anthropic
from . import config, memory, tools
from .tools import get_time

PERSONALITY = """You are ALI, a personal AI assistant in the style of J.A.R.V.I.S. from Iron Man.
You are loyal, calm, quick, and dryly witty - never rude, never rambling.
Address the user as "{owner}" or "sir/ma'am" occasionally, not in every sentence.
Keep replies SHORT (1-3 sentences) because they are often spoken aloud. No markdown, no emojis, no lists.
Use your tools whenever the user wants an action (open things, search, notes, time, system info).
When you learn something lasting about the user, store it with the remember tool.
If you can't do something, say so briefly and suggest an alternative.

Current time: {now}
What you remember about the user:
{facts}
"""


class Ali:
    def __init__(self):
        if not config.API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY missing. Copy .env.example to .env and add your key.")
        self.client = anthropic.Anthropic(api_key=config.API_KEY)
        self.history = []

    def _system(self):
        return PERSONALITY.format(owner=config.OWNER, now=get_time(), facts=memory.facts_summary())

    def _trim(self):
        # keep history bounded, cutting only at a plain user message so tool pairs stay intact
        while len(self.history) > 40:
            self.history.pop(0)
            while self.history and not (
                self.history[0]["role"] == "user" and isinstance(self.history[0]["content"], str)
            ):
                self.history.pop(0)

    def ask(self, text):
        self.history.append({"role": "user", "content": text})
        for _ in range(8):  # max tool-use rounds
            resp = self.client.messages.create(
                model=config.MODEL,
                max_tokens=600,
                system=self._system(),
                tools=tools.SCHEMAS,
                messages=self.history,
            )
            self.history.append({"role": "assistant", "content": resp.content})
            if resp.stop_reason != "tool_use":
                self._trim()
                return "".join(b.text for b in resp.content if b.type == "text").strip()
            results = []
            for b in resp.content:
                if b.type == "tool_use":
                    print(f"   [tool] {b.name} {b.input}")
                    results.append({"type": "tool_result", "tool_use_id": b.id, "content": tools.run(b.name, b.input)})
            self.history.append({"role": "user", "content": results})
        return "I got stuck in a loop on that one. Could you rephrase?"
