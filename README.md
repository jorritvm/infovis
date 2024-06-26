# Infovis
## Introduction 
Repository for the infovis project at VUB 2024.   
Implements an interactive visualisation to explore global wind power.

## Setting up your local copy
1. Clone the repo
1. Make sure you're using python 3.11
1. Set up a virtual environment

    ```python -m venv venv```

1. Restore the dependencies

    ```pip install -r requirements.txt```
    
2. Copy `.env.template` to `.env` and configure the required secrets (e.g. port, ...)


## Running the notebook(s)
1. Get the jupyter extension for vs code
1. Run the notebook from vs code using the ipython kernel.

## Running the dashboard from the IDE
1. Run the dash app in `app/app.py` from your IDE of choice
2. Explore the app using your web browser.

## Running the dashboard from the CLI
1. Activate the venv: `venv\Scripts\activate`
2. Navigate to the app directory: `cd app`
3. Run the dash app: `python app.py` 
4. Explore the app using your web browser.

## Contribute
1. Read the documentation in the `doc/` folder
1. Create your own feature branch 
1. Create your feature and use sensible commit messages
1. Do a pull request to `main`

## Notes
* use black for automated python code formatting
* do not commit secrets
* do not commit IDE config files
* do not commit data unless limited in size

## Author & contributors
* Jorrit Vander Mynsbrugge
* Ruth Vandeputte
* Mishkat Chowdhury

