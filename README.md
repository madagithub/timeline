# Timeline (Leonardo)

## General
This exhibit is part of the Leonardo ehibition.
It shows a timeline with various clickable numbers.
Upon clicking a number, text is shown to describe that historical event.
The ehibit supports Hebrew, English and Arabic and allows to change languages with buttons.
It is designed to work with a (large) touch screen but can be run using a mouse as well with a cursor.

## Installation & Run
The exhibit runs using python 3 on linux, using the pygame engine.

After the latest python 3 installation, use:

```
pip3 install pygame
pip3 install pyfribiditi
pip3 install evdev
```

To install all necessary packages.

Then, to run, go to the root project dir and run:

```
python3 Timeline.py
```

## Config
The exhibit supports a vast array of configurations using a config json file located in assets/config/config.json
Following is a complete description of all options:

### defaultLanguage

Specifies the default language loaded on startup (he/en/ar).
Note that the prefix to put here should be identical to the prefix defined in the language array (see details below).

### dots

This is an array specifying all timeline dots. Each dot has a header key and a text key (used to load up translations), and an x and y on the image where it shows.
As always, x is increasing left to right, and y is increasing top to bottom (so 0,0 is the top left corner of the screen).

So, each dot info looks like this:

```
{
    "headerKey": "DOT_1_HEADER",
    "textKey": "DOT_1_TEXT",
    "x": 1876,
    "y": 51
}
```

### languages

This is an array specifying all the language configurations the exhibit supports.
For each language, the buttonText key sets the text to show on the button used to choose that language, the prefix defines its prefix (en/he/ar) to be used in the defaultLanguage config (see above) and for defining texts in the texts config part (see below), and the rtl states if the language is rtl or not (true/false).
Finally, the fonts structure defines a ttf file and the size for the hader font, numbers font (shown on the map), small text font and text font (larger) used to display the info on each dot.

Here's an example of a language definition:

```
{
    "buttonText": "En",
    "fonts": {
        "headerFont": {
            "filename": "assets/fonts/SimplerPro_V3-Black.ttf",
            "size": 34
        },
        "numbersFont": {
            "filename": "assets/fonts/SimplerPro_V3-Black.ttf",
            "size": 30
        },
        "smallTextFont": {
            "filename": "assets/fonts/SimplerPro_V3-Regular.ttf",
            "size": 23
        },
        "textFont": {
            "filename": "assets/fonts/SimplerPro_V3-Regular.ttf",
            "size": 27
        }
    },
    "prefix": "en",
    "rtl": false
}
```

### showFPS

This key can be set to true to show an FPS (frames per second) value and measure performance issues. FPS should be ideally between 30 and 60.

### texts

This key contains a key for each langauge prefix, leading to an ojbect of key/value pairs, with the key being the text key and the value the translation for the current prefix.

Here is an example for an example texts object for one language and one two translated keys:

```
"ar": {
    "DOT_10_HEADER": "\u062a\u0635\u0645\u064a\u0645 \u062b\u0645\u062b\u0627\u0644 \u062d\u0635\u0627\u0646 \u0636\u062e\u0645 (1489-1494)",
    "DOT_10_TEXT": "\u0641\u064a \u0639\u0627\u0645 1493\u060c \u0642\u062f\u0645 \u0644\u064a\u0648\u0646\u0627\u0631\u062f\u0648 \u0646\u0645\u0648\u0630\u062c\u0627\u064b \u0645\u0646 \u0627\u0644\u0635\u0644\u0635\u0627\u0644 (\u0635\u062e\u0631 \u0637\u064a\u0646\u064a) \u0628\u0627\u0644\u062d\u062c\u0645 \u0627\u0644\u0643\u0627\u0645\u0644 (\u062d\u0648\u0627\u0644\u064a 7 \u0623\u0642\u062f\u0627\u0645) \u0644\u062a\u0645\u062b\u0627\u0644 \u0644\u0630\u0643\u0631\u0649 \u0641\u0631\n\u0627\u0646\u0634\u064a\u0633\u0643\u0648 \u0633\u0628\u0648\u0631\u0627\u0632\u0627\u060c \u0648\u0627\u0644\u062f \u062f\u0648\u0642 \u0645\u064a\u0644\u0627\u0646\u0648. \u0627\u0644\u062a\u0645\u062b\u0627\u0644 \u0627\u0644\u0646\u0647\u0627\u0626\u064a \u0627\u0644\u0645\u0635\u0646\u0648\u0639 \u0645\u0646 \u0627\u0644\u0628\u0631\u0648\u0646\u0632\u060c \u0644\u0645 \u064a\u062a\u0645 \u0635\u0628\u0647 \u0623\u0628\u062f\u0627\u064b \u0628\u0633\u0628\u0628 \u063a\u0632\u0648 \u0641\u0631\u0646\u0633\u0627 \u0644\u0644\u062f\u0648\u0642\u064a\u0629.\n\u062a\u0639\u062a\u0645\u062f \u0643\u062a\u0644\u0629 \u0631\u0623\u0633 \u0627\u0644\u062d\u0635\u0627\u0646 \u0627\u0644\u0630\u064a \u064a\u0642\u0641 \u062e\u0644\u0641\u0643\u0645 \u0639\u0644\u0649 \u062a\u0633\u062c\u064a\u0644 \u0648\u0631\u0633\u0645 \u0644\u064a\u0648\u0646\u0627\u0631\u062f\u0648 \u0644\u0642\u0648\u0627\u0644\u0628 \u0627\u0644\u062a\u0645\u062b\u0627\u0644 \u0627\u0644\u0628\u0631\u0648\u0646\u0632\u064a.",
}
```

Note: you can change this manually, but as with Hebrew and Arabic escaping to unicode is necessary, it's best to translate using the scripts provided for it (see the Translations section below).

### touch, touchDeviceName, touchMaxX, touchMaxY

These 4 keys define the characteristics of the touch screen connected to the exhibit.
touch should be set to true for the exhibit to use touch (otherwise a mouse is supported).
touchDeviceName is a partial name that is used to match the touch screen device. Use a partial name that is also unique.
You can enumerate all linux devices using this command:

```
lsinput
```

Finally, the touchMaxX and touchMaxY represent the logical screen resolution that evdev works with.
The exhibit will convert these coordinates to the actual screen resolution coordinates.
These usually change with the screen size, and are usually 4096x4096 but can also be 2048x2048 and 1024x1024, or other numbers potentially.
The best way to find out the proper value, is to add print statements in the TouchScreen.py file, in the readTouch method, in case the event type is ecodes.EV_ABS.

Like this:
```
elif event.type == ecodes.EV_ABS:
	absEvent = categorize(event)

	if absEvent.event.code == 0:
		currX = absEvent.event.value
	elif absEvent.event.code == 1:
		currY = absEvent.event.value

	print(currx, curry)
```

Then, run the exhibit, and touch various corners of the screen. It will be very easy to conclude on the max value sknowing they are a power of 2.

## Log
The exhibit supports a rotating log named timeline.log in the root directory, that logs the following events:
* START (the exhibit loads)
* INIT (exhibit initalization is done)
* DOT_CLICKED,N (dot numbered N was clicked)
* LANGUAGE_CHANGED,prefix (lngaugaed changed to prefix: en/ar/he)
* ERROR,Error occured! (when an error occured)


## Translations
The exhibit contains all texts in the config file.
However, to support an easy translation, there are two python scripts provided as well.
One takes the current translations and dumps them in a csv file that can be edited / completed.
The other one, takes the csv file and puts all text based in the config file (overwriting older texts).

So, if the translation needs updating, the best way to do so is first run the extraction script from assets/config:
```
python3 extract-translation-csv.py
```

Then, updated the csv externally, and when done, run this script to update the texts in the config file from assets/config as well:
```
python3 import-csv.py
```

Now, the exhibit will show the updated texts.
