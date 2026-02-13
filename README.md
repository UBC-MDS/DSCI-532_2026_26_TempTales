# Climate Change Explorer Dashboard

## Overview

This project is an interactive dashboard that allows users to explore global and country-level temperature trends over time while connecting these trends to major historical events. Users can select a country, view seasonal and monthly temperature patterns, and see how significant events like industrialization or world wars align with temperature changes. A world heatmap provides a spatial view of temperatures for selected years, making regional patterns immediately clear. This tool consolidates climate data from over two centuries into a user-friendly interface for researchers, students, policy makers, and environmentally conscious individuals.

## Developers

### Development Setup

Clone the repo, create conda environment and activate it.

```bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_26_TBD.git
cd UBC-MDS/DSCI-532_2026_26_TBD 

conda env create -f environment.yml
conda activate 532_project
```

### Dynamic Data Download

This project relies on the **Berkeley Earth Climate Change dataset** from Kaggle. To download the data dynamically using the provided script (`download_data.py`), follow these steps:

1. **Create a Kaggle API Token**
   - Go to your Kaggle account → **Account** → **API** → **Create New API Token**.
   - This will download a file named `kaggle.json`.
   - If the file is not created automatically, you can manually create it on your computer with the following content:

   ```json
    {
       "username": "YOUR_KAGGLE_USERNAME",
       "key": "YOUR_KAGGLE_API_TOKEN"
   }
   ```

2. **Save your API Token**
Move `kaggle.json` to your home directory under `~/.kaggle/` (create the `.kaggle` folder if it doesn’t exist):

     ```bash
     mkdir -p ~/.kaggle
     mv /path/to/kaggle.json ~/.kaggle/
     chmod 600 ~/.kaggle/kaggle.json
     ```

3. **Run the data download script**
From the project root, run:

    ```bash
     python scripts/download_data.py
    ```

This script will:
    - Authenticate with Kaggle
    - Download the latest version of the dataset
    - Extract the CSV files into `data/raw/`

4. **Verify**
After running the script, you should see the CSV files in `data/raw/`.

## Contributors

Contributors are expected to follow the guidelines outlined in **[CONTRIBUTING.md](./CONTRIBUTING.md)**. Please review this document before submitting issues or pull requests.

## Copyright

- Copyright © 2026 Emily Jin, Ian Gault, Purity Jangaya, Yusheng Li.
- Free software distributed under the [MIT License](./LICENSE).

