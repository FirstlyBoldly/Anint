# Anint

![Tests](https://github.com/FirstlyBoldly/Anint/actions/workflows/tests.yaml/badge.svg)
[![PyPI](https://img.shields.io/pypi/pyversions/anint.svg)](https://pypi.org/project/anint/)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)

Ankha's Internationalization and Localization for Python

# Prerequisites

Python 3.11.x or newer.

# Installation

`pip install anint`

# Configuration

## Via Configuration Files (Recommended)

At the root of the project, create and configure one of the following files:
\
*Listed by order of precedence*

- `anint.ini`
- `.anint.ini`
- `pyproject.toml`
- `anint.cfg`

For example:

```ini
; ${PROJECT_ROOT}/anint.ini

[anint]
locales = en, mn
locale = mn
fallbacks = en
path = locales
```

Then you can import the `t` method and get translations immediately:

```python
# your_file.py

from anint import t


print(t('greetings.hello'))
```

**Note**:
- Use this if you do not need to change localization settings during runtime
  \
  ***Will be changed to allow for runtime localization setting***

## Manually (For More Control)

Import the modules that we need

```python
from anint import translations, Translator
```

Load translations

```python
translations.load('path_to_your_locale_directory')
```

Instantiate `Translator` object

```python
my_translator = Translator(
    locales=['en', 'mn'],
    locale='mn',
    fallbacks=['en']
)
```

Call on its `translate` method
```python
>>> my_translator.translate("greetings.hello")
'Сайн байна уу'
```

Change its locale

```python
>>> my_translator.set_locale('en')
>>> my_translator.translate("greetings.hello")
'Hello'
```

## Anint Recipes

To add more functionality to the base `Translator` class, one may do the following:

```python
# One may place this class at the root
# of your project directory for easier import.


class TranslatorRecipes(Translator):
    def before_after(self, before=None, after=None):
        """Returns a tuple of strings as (before, after) of the key translation.
        Both values are None by default and will be assigned as empty strings if not given further arguments.
        """
        before_translation = self.translate(before) if before else ""
        after_translation = self.translate(after) if after else ""
        return before_translation, after_translation

    def attention(self, attention):
        """Returns an attention translation if attention is True, otherwise empty string."""
        return self.translate("symbol.attention") if attention else ""

    def encapsulate(self, encapsulate):
        """Returns a tuple of encapsulations as (before, after) if encapsulate is True,
        otherwise tuple of empty strings.
        """
        _encapsulate_before = ""
        _encapsulate_after = ""
        if encapsulate:
            # Not all encapsulations need to be the same for every locale.
            if self.locale == "ja":
                _encapsulate_before = self.translate("symbol.left_black_lenticular_bracket")
                _encapsulate_after = self.translate("symbol.right_black_lenticular_bracket")
            else:
                _encapsulate_before = self.translate("symbol.left_square_bracket")
                _encapsulate_after = self.translate("symbol.right_square_bracket")

        return _encapsulate_before, _encapsulate_after

    def translate(self, key, *args, before = None, after = None, attention = False, encapsulate = False):
        """Returns the translation for the specified key.

        :param key: A string sequence of dict keys connected by dots.
        :param args: Passed onto the translation to be formatted if there are any placeholders.
        :param before: Optional key to be included to the left of the key translation.
        :param after: Optional key to be included to the right of the key translation.
        :param attention: To give attention to the translated key or not. False by default.
        :param encapsulate: To encapsulate the translated key or not. False by default
        :return: The translation for the currently specified language setting.
        """
        _before, _after = self.before_after(before, after)
        _attention = self.attention(attention)
        _encapsulate_before, _encapsulate_after = self.encapsulate(encapsulate)
        # Call on the base class to get the translated text.
        translation = super(TranslatorRecipes, self).translate(key, *args)
        return _attention + _encapsulate_before + _before + translation + _after + _encapsulate_after
```