#!/bin/bash

# 1. Navigate to your project's scripts directory
cd ~/projects/chatbot/scripts

# 2. Make the conda command available to this script
source ~/miniconda3/etc/profile.d/conda.sh

# 3. Activate your specific environment
conda activate chatbot

# 4. Update the environment based on your YAML file
conda env update --file chatbot.yml --prune