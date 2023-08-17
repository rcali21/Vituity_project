# Vituity_project

This project was developed to address a technical project administered by Vituity.

## Getting Started - Setting up our environment and understanding the directory structure.

To begin, navigate to an empty directory on your system and run the following:

`git clone https://github.com/rcali21/Vituity_project.git`

You should now see the following directory structure within your directory:

- 📂 **Vituity_project**
- 📄 README.md
- 📄 ADT_sample.txt
- 📄 Sample_ORU.txt
- 📄 requirements.txt
- 📊 sampledata.csv
- 📄 Vituity RCM EDI Coding Assessment.pdf
  - 📂 **scripts**
    - 🐍 Utils.py <<<---- Functions used by the main script.
    - 🐍 make_sqlitedb.py <<<---- Bonus challenge script.
    - 🐍 process_data.py <<<---- Main script for running the pipeline.
  - 📂 **notebook**
    - 📓 main_walkthrough.ipynb <<<---- Main challenge notebook with markdown annotations for each step.
    - 📓 db_walkthrough.txt <<<---- Bonus challenge notebook with markdown annotations for each step.


Next, let's ensure we have the appropriate libraries installed to run the program (I assume you either A) have a conda environment already setup or B) are running this natively without one but at least have pip available on your system, as setting up environments would be beyond the scope of this challenge)

To download the script dependencies, simply run the following command from the top-level of this directory:

`pip install -r requirements.txt`


### Note: 
There are two ways that this challenge can be completed. Option (1) is using standard Python scripts located [here](https://github.com/rcali21/Vituity_project/tree/main/scripts) that sequentially call commands to address each part of the challenge. Option (2) is by opening up a Jupyter Notebook and launching the accompanying '.ipynb' notebooks located [here](https://github.com/rcali21/Vituity_project/tree/main/notebook). The second option offers a more granular explanation of the code chunks corresponding to each part of the challenge.


### Running the base scripts:

To run the scripts as outlined in Option (1), simply navigate to the 'scripts' directory and call the process_data.py script like so:

(Assuming you are at the top level 'Vituity_project' directory)

````md
cd scripts/

python3 process_data.py
````

### Outputs:
Upon running the scripts, you should now see an 'Archive' folder within the top-level directory. Within this folder, there are two subfolders 'Archive/Original' and 'Archive/Modified'.

The directory structure should now look like so:

- 📂 **Vituity_project**
- 📄 README.md
- 📄 ADT_sample.txt
- 📄 Sample_ORU.txt
- 📄 requirements.txt
- 📊 sampledata.csv
- 📄 Vituity RCM EDI Coding Assessment.pdf
  - 📂 **scripts**
    - 🐍 Utils.py 
    - 🐍 make_sqlitedb.py 
    - 🐍 process_data.py 
  - 📂 **notebook**
    - 📓 main_walkthrough.ipynb
    - 📓 db_walkthrough.txt
  - 📂 **Archive**
    - 📂 **Original**
      - 📄 ADT_sample.txt
      - 📄 Sample_ORU.txt
      - 📊 sampledata.csv
    - 📂 **Modified**
      - 📊 ADT_(TodaysDate)_Modified_file.csv
      - 📊 ORU_(TodaysDate)_Modified_file.csv
      - 📄 total_bill_sum.txt
     


### Bonus Challenge:

The bonus challenge involves creating a SQLite database using Python and the csv files that we generated in the previous step. To do so, simply navigate to the scripts directory once again and call the appropriate script like so:

````md
cd scripts/

python3 make_sqllitedb.py
````

After the script has finished running you will now see the following 'Bonus' subfolder and SQL database file within the 'Archive' folder that we previously created.

  - 📂 **Archive**
    - 📂 **Original**
      - 📄 ADT_sample.txt
      - 📄 Sample_ORU.txt
      - 📊 sampledata.csv
    - 📂 **Modified**
      - 📊 ADT_(TodaysDate)_Modified_file.csv
      - 📊 ORU_(TodaysDate)_Modified_file.csv
      - 📄 total_bill_sum.txt
    - 📂 **Bonus**
      - 💾 ADT.db
     

### Running the notebooks:
The notebooks can be run by installing Jupyter Notebooks or Jupyter Lab and the ipynb kernel on your system. For brevity, I will assume you know how to do this or I will walk through it with you myself.


## Re-running the scripts:
To re-run the scripts, simply run the following from the top-level directory before you begin a subsequent run:

`rm -rf Archive/`

Then you may start from the beginning.

