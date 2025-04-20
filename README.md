# fSync (Maya fSpy Importer)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

*A tool to sync fSpy camera data and projections with Maya scenes.*


Easily import camera data and create a projection shader from [fSpy](https://github.com/stuffmatic/fSpy) into Autodesk Maya!

## Features

- **Launch fSpy (Windows only):** Open the fSpy application directly from the script with a dedicated button (requires default installation path)
- Import camera parameters from fSpy JSON file
- Use a single image or an image sequence for static or animated projection
- Set an offset for image sequences
- Optionally specify camera and shader names
- Create camera and projection shader with one click
- Apply the created shader to selected objects
- Update camera or image settings at any time

## Installation

1. Download or clone this repository.
2. Copy the script file to your Maya scripts directory:  
```
Documents/maya/<version>/scripts/
```
3. In Maya, open the Script Editor and run:
```
import fSync
fSync.show_dockable_window()
```


## Usage

![fSync UI in Maya](https://github.com/user-attachments/assets/0e629e71-92af-4d83-8520-6ececf70fe0b)

1. **(Optional) Click "Launch fSpy"** (Windows only) to open fSpy directly.
2. **Export camera data from fSpy** as a JSON file.
3. **Run the script in Maya** to open the UI.
4. **Select the JSON file** and your projection image or image sequence.
5. (Optional) Enter custom camera and shader names, and set a sequence offset if needed.
6. Click **Create Scene** to automatically generate the camera, projection setup, and shader.
7. **Select objects** and click "Apply Shader" to assign the shader.
8. Use "Update" to change camera or image settings at any time.

Or watch the Demo here: [YouTube Video](https://youtu.be/1ouHB7DwsLI)

## Requirements

- Autodesk Maya (version 2025+)
- [fSpy](https://github.com/stuffmatic/fSpy)

## Credits

- Script by Mats Valgaeren
- Powered by [fSpy](https://github.com/stuffmatic/fSpy)

## License

[GNU 3.0]
