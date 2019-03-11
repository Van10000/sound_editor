
# Sound editor

Developed by Smirnov Ivan

# Description
A simple sound editor, including very basic features of sound processing.

1. Copy/Paste of track fragments
- Ctrl+C --- copy
- Ctrl+V --- paste
- Ctrl+A --- select all
- Ctrl+> --- go to the end of the track
- Ctrl+< --- go to the beginning of the track

2. Reverse part of track.
- Select part of track
- Use Ctrl+R to reverse it
3. Effects on the right panel of the track:
- Fade in/ fade out.
- Change loudness for part of track.
	- Select part of track
	- Adjust loudness
- Mixing multiple tracks.
	- Every track has on/off button.
	- To get a mix of all 'on' tracks, press Alt+S.
- Change speed of track (changing the pitch proportionally).
- Sound compression.
	- ratio (between 0 and 1) controlls the level of compression
	- The bigger ratio - the more compressed sound will be

4. There is a console version.
Use --help to see usage.

## Requirements
- Python >= 3.5.1
- PyQt4.
- numpy

## Components
- GUI version GuiEditor.py
- Console version ConsoleEditor.py
- Core of application, processing all sound operations Core/... (usable as a standalone library)
- Tests Tests/...
- Graphic view model ViewModel/...
- Console view model ConsoleModel/...
- Graphic view appearence View/...
