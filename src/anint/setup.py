# Anint
from .config import data
from .models import Translator

t: Translator = Translator(
    data["locales"],
    data["locale"],
    data.get("fallback", None),
    data["translations"]
)
