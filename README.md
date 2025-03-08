# Anint

![Tests](https://github.com/FirstlyBoldly/Anint/actions/workflows/tests.yaml/badge.svg)
[![PyPI](https://img.shields.io/pypi/pyversions/anint.svg)](https://pypi.org/project/anint/)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)

Ankha's Internationalization and Localization for Python

# Prerequisites

Python 3.11.x or newer.

# Installation

`pip install anint`

# Setup

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

*Refer to the tests directory for further configuration file examples.*

Then you can import the `t` method and get translations immediately:

```python
# your_file.py

from anint import t


print(t("greetings.hello"))
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
translations.load("path_to_your_locale_directory")
```

Instantiate `Translator` object

```python
my_translator = Translator(
    locales=["en", "mn"],
    locale="mn",
    fallbacks=["en"]
)
```

Call on its `translate` method
```python
>>> my_translator.translate("greetings.hello")
"Сайн байна уу"
```

Change its locale

```python
>>> my_translator.set_locale("en")
>>> my_translator.translate("greetings.hello")
"Hello"
```

## Anint Recipes

To add more functionality to the base `Translator` class, one may do the following:

```python
# ${{PROJECT_ROOT}}/custom_model.py

class TranslatorPlus(Translator):
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

And to initialize the translator:

```python
# ${{PROJECT_ROOT}}/custom_model.py

# If any config file exists, the arguments are stored inside this dict.
from anint.config import instance_data
from anint import Translator


# See above.
class TranslatorPlus(Translator):
    .
    .
    .


# If a config file exists.
my_translator_class0 = TranslatorPlus(**instance_data)

# Or define it here.
my_translator_class1 = TranslatorPlus(
    locales=["en", "mn"],
    locale="mn",
    fallbacks=["en"]
)

t_alias = my_translator_class1.translate
```

#  Localization Files

## YAML/YML

```yaml
models:
  member: "Member"
attributes:
  member:
    name: "Name"
    student_id: "Student ID"
    grade: "Grade"
    department: "Department"
    course: "Course"
    role:
      user: "User"
      mod: "Mod"
      admin: "Admin"
    grades:
      freshman: "Freshman"
      sophomore: "Sophomore"
      junior: "Junior"
      senior: "Senior"
      graduate: "Graduate"
    departments:
      information_technology: "Information Technology"
      digital_entertainment: "Digital Entertainment"
    courses:
      ai_strategy: "AI Strategy"
      iot_systems: "IoT Systems"
      robotics_development: "Robotics Development"
      game_production: "Game Production"
      cg_animation: "CG Animation"
      selection_in_progress: "Selection in Progress"
```

## JSON

```json
{
  "models": {
    "member": "メンバー"
  },
  "attributes": {
    "member": {
      "name": "名前",
      "student_id": "学籍番号",
      "grade": "学年",
      "department": "学科",
      "course": "コース",
      "role": {
        "user": "ユーザー",
        "mod": "Mod",
        "admin": "管理者"
      },
      "grades": {
        "freshman": "1年生",
        "sophomore": "2年生",
        "junior": "3年生",
        "senior": "4年生",
        "graduate": "OM"
      },
      "departments": {
        "information_technology": "情報工学科",
        "digital_entertainment": "デジタルエンタテインメント学科"
      },
      "courses": {
        "ai_strategy": "AI戦略コース",
        "iot_systems": "IoTシステムコース",
        "robotics_development": "ロボット開発コース",
        "game_production": "ゲームプロデュースコース",
        "cg_animation": "CGアニメーションコース",
        "selection_in_progress": "選択中"
      }
    }
  }
}
```

These locales files are read as dicts.
As such, when specifying the value to get, the keys to the value are lined together with dots.

```python
>>> from anint import t
>>> t("attributes.member.name")
"Name"
```

**Notes:**

- If two files with the same locale exist, then a MultipleSameLocaleError exception will be raised.
- If no value can be found, then the fallback locale will be used. Only if that also fails will a TranslationError be raised.

# Problem?

Actually, I don't expect anyone else other than me to use this package.
\
But if you find it useful enough to want to contribute, be my guest!