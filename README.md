# Foreign Language Number Trainer

This tool is designed to help you practice numbers in foreign languages.

This script is built based on my finding on nice google translate API
https://translate.google.com/translate_tts?ie=UTF-8&tl=nl&client=tw-ob&q=acht

[Listening module](https://raw.githubusercontent.com/timkrysta/just-learn-numbers/main/listening-module.gif)
[Speaking module](https://raw.githubusercontent.com/timkrysta/just-learn-numbers/main/speaking-module.gif)

### Installation

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

### Usage

To start the program, run:

```bash
python3 just-learn-numbers.py
```

The program will prompt you to enter a range of numbers to practice. You can enter a specific range (e.g. 1-10), or enter "all" to practice all numbers up to 1 billion.

The program will start presenting you with random numbers in the range you specified. You'll be prompted to enter the correct number in the target language. If you get the answer correct, the program will play a sound and show the next number. If you get the answer wrong, the correct answer will be displayed and you'll be given another chance to answer.

### Credits

This program uses the following libraries:

- PyInquirer
- gTTS
- pydub

### TODO
- get `_lang` variable from user input instead of being hardcoded
- add support for versions newer than python 3.9

### License

This project is licensed under the MIT License. See the LICENSE file for details.

