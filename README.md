# AI Remove Background GIMP Plugin

This GIMP plugin allows users to remove image backgrounds using AI-powered tools like [rembg](https://github.com/danielgatis/rembg). The plugin integrates with GIMP to offer a simple way to remove backgrounds, optionally apply the result as a mask, flatten the image, and resize the canvas to make the image square. It can process a single image or all open images in GIMP.

## Features

- **AI-Powered Background Removal:** Removes the background using the `rembg` tool, an AI-powered background removal library.
- **Mask Option:** Choose to apply the background removal as a non-destructive layer mask.
- **Make Square Option:** Optionally resize the canvas to make the image square by extending the shorter side to match the longest side.
- **Flatten Image:** Automatically flatten the image after processing, merging visible layers and removing any non-visible ones.
- **Batch Process:** Process all open images in GIMP with a single click.

## Requirements

- **GIMP 2.10+**
- **Python 2.7** (GIMP uses Python 2.7 for its plugins)
- **Python 3.x** (For `rembg` to work)
- **rembg**: You need to have the `rembg` package installed in Python 3.x.

## Installation

1. **Clone or Download** this repository.
   ```bash
   git clone https://github.com/your-username/ai-remove-bg-gimp-plugin.git
Install rembg in your Python 3 environment.

1.  **Install `rembg`** in your Python 3 environment.

    bash

    Copy code

    `pip install rembg[cli]`

2.  **Copy the Plugin to GIMP**:

    -   Move the `remove_background.py` file to your GIMP plugins folder:
        -   **Windows:** `C:\Users\YourUserName\AppData\Roaming\GIMP\2.10\plug-ins`
        -   **Linux:** `/home/YourUserName/.config/GIMP/2.10/plug-ins`
3.  **Restart GIMP** to load the plugin.

Usage
-----

1.  **Open GIMP** and load an image.
2.  Go to **Python-Fu > AI Remove Background...**.
3.  Configure the options as per your needs:
    -   **Use as Mask:** Apply the background removal as a non-destructive mask.
    -   **Model:** Choose which AI model to use for background removal.
    -   **Alpha Matting:** Enable alpha matting for smoother edges.
    -   **Make Square:** Optionally make the canvas square.
    -   **Process all Open Images:** Process all open images in GIMP in batch mode.
4.  Click **OK** to run the plugin.

Plugin Options
--------------

| Option | Description |
| --- | --- |
| **Use as Mask** | Apply the background removal as a non-destructive mask on the current layer. |
| **Model** | Select from different AI models (e.g., `u2net`, `sam`, `isnet-anime`). |
| **Alpha Matting** | Refine the edges of the background removal using alpha matting. |
| **Alpha Matting Erode Size** | Set the size for edge refinement when using alpha matting. |
| **Make Square** | Resize the canvas to make the image square by adjusting the shortest side. |
| **Process all Open Images** | Apply the plugin to all open images in GIMP. |

Example Workflow
----------------

1.  Open an image in GIMP that you want to remove the background from.
2.  Select **AI Remove Background** from the Python-Fu menu.
3.  Choose to apply the removal as a mask or flatten the image, and whether to resize the image to be square.
4.  Run the plugin and watch as the background is removed and the image is processed.

Contributing
------------

Feel free to open issues or submit pull requests to improve this plugin! Contributions are always welcome.

License
-------

This project is licensed under the **GPLv3** License - see the <LICENSE> file for details.

Acknowledgments
---------------

-   **rembg**: This plugin integrates with [rembg](https://github.com/danielgatis/rembg) to handle AI-powered background removal.
-   **GIMP**: The GNU Image Manipulation Program, a free and open-source image editor.
