# fSync

![fSpy_image_v002](https://github.com/user-attachments/assets/1620cf67-0e20-4408-9a12-3a8f20a7c6ea)

[![Build Status](https://img.shields.io/github/actions/workflow/status/username/repo/ci.yml?branch=main)](https://github.com/MatsValgaeren/FrameForge/actions)
[![Coverage](https://img.shields.io/codecov/c/github/username/repo)](https://codecov.io/gh/username/repo)
[![Latest Release](https://img.shields.io/github/v/release/username/repo)](https://github.com/MatsValgaeren/FrameForge/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/username/repo)](https://github.com/MatsValgaeren/FrameForge/issues)

</div>

<details>
<summary>Table of Contents</summary>

- [About](#about)
- [Features](#features)
- [Installation](#installation)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap & Contributing](#roadmap--contributing)
- [Credits](#credits)
- [License](#license)

</details>


## About

A tool to sync fSpy camera data and projections with Maya scenes.

*Watch Demo Video Here: [YouTube Video](https://youtu.be/1ouHB7DwsLI)*


## Features

- **Launch fSpy Instantly:** Open the fSpy application directly from the script with a single click (Windows default installation required).
- **Import Camera Data:** Load camera parameters seamlessly from an fSpy JSON file.
- **Flexible Image Support:** Work with either a single image or an image sequence for static or animated projections.
- **Custom Naming:** Specify custom names for cameras and shaders.
- **One-Click Setup:** Automatically create both the camera and projection shader.
- **Quick Shader Assignment:** Apply the generated shader to selected objects instantly.
- **Update button:** Modify camera or image settings with the click of a button.


## Installation

#### Requirements

-   Autodesk Maya (version 2025+)
-   [fSpy](https://github.com/stuffmatic/fSpy)

#### Maya Scipt Setup

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

![fSync UI in Maya](https://github.com/user-attachments/assets/cc538fbe-fecc-4ecf-a57b-4449d4437c73)

1. (Optional) Click "Launch fSpy" (Windows only) to open fSpy directly.
2. Export camera data from fSpy as a JSON file.
3. **Run fSync in Maya** to open the UI.
4. **Select the JSON file and your projection image or image sequence.**
5. (Optional) Enter custom camera and shader names, and set a sequence offset if needed.
6. **Click Create Scene** to automatically generate the camera, projection setup, and shader.
7. **Select objects and click "Apply Shader"** to assign the shader.
8. Use "Update" to change camera or image settings at any time.

***Watch the Demo here: [YouTube Video](https://youtu.be/1ouHB7DwsLI)***


## Roadmap & Contributing


See the [open issues](https://github.com/MatsValgaeren/FrameForge/issues) to track planned features, known bugs, and ongoing work.

If you encounter any bugs or have feature requests, please submit them as new issues there.  Your feedback and contributions help improve RefUp!


## Credits

-   Script by Mats Valgaeren
-   Powered by:
    -   [fSpy](https://github.com/stuffmatic/fSpy)
    -   [PyQt6](https://pypi.org/project/PyQt6/)


## License

[GNU General Public License v3.0](LICENSE)
