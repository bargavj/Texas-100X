# Texas-100X
This repository contains the code to obtain an extended version of Texas-100 hospital data set. The data set consists of 925,128 patient records from 441 hospitals in Texas state from the year 2006. Each record consists of patient’s demographic information, such as age, gender, race and ethnicity, and medical information such as duration of hospitalization, type of admission, source of admission, admitting diagnosis, patient status, medical charges and principal surgical procedure. The machine learning task is to predict one of the 100 surgical procedures based on the patient’s health record. 

To generate the data files, you would need to download the PUDF_base1q2006_tab.txt, PUDF_base2q2006_tab.txt, PUDF_base3q2006_tab.txt and PUDF_base4q2006_tab.txt files from https://www.dshs.texas.gov/THCIC/Hospitals/Download.shtm and store them in `data/` directory.

After this, you can run the process_texas.py file:
`$ python process_texas.py`

The resulting files will be generated in the `output/` directory.

The generated Texas-100X data files can also be found in Texas-100X.zip file here: https://drive.google.com/drive/folders/1nDDr8OWRaliIrUZcZ-0I8sEB2WqAXdKZ?usp=sharing
