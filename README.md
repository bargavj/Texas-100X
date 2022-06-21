# Texas-100X

Donor: Bargav Jayaraman (bj4nq@virginia.edu)

This repository contains the code to obtain an extended version of Texas-100 hospital data set. The data set consists of 925,128 patient records from 441 hospitals in Texas state from the year 2006. Each record consists of patient’s demographic information, such as age, gender, race and ethnicity, and medical information such as duration of hospitalization, type of admission, source of admission, admitting diagnosis, patient status, medical charges and principal surgical procedure. The machine learning task is to predict one of the 100 surgical procedures based on the patient’s health record. 

For a baseline, a 2-layer neural network (with 256 neurons in each layer and relu non-linear function) trained on a random 50,000 subset of records achieves 61% training accuracy and 46% test accuracy. 


## Obtaining the Data Set

To generate the data files, you would need to download the PUDF_base1q2006_tab.txt, PUDF_base2q2006_tab.txt, PUDF_base3q2006_tab.txt and PUDF_base4q2006_tab.txt files from https://www.dshs.texas.gov/THCIC/Hospitals/Download.shtm and store them in `data/` directory.

After this, you can run the process_texas.py file:
`$ python process_texas.py`

The resulting files will be generated in the `output/` directory.

Additionally, the generated Texas-100X data files can also be found in Texas-100X.zip file here: https://drive.google.com/drive/folders/1nDDr8OWRaliIrUZcZ-0I8sEB2WqAXdKZ?usp=sharing.


## Additional Notes

Although the data set contains Hospital ID (`THCIC_ID`) attribute, this is only used for sampling and visualizing the demographics. This feature is excluded from model training.

`texas_100x.csv` file contains the Hospital ID (`THCIC_ID`), the 10 demographic and medical features, and the prediction label `PRINC_SURG_PROC_CODE`.

`texas_100x_features.p` contains the Hospital ID (`THCIC_ID`) and the 10 demographic and medical features.

`texas_100x_labels.p` contains the prediction label `PRINC_SURG_PROC_CODE` for each record.

`texas_100x_feature_desc.p` contains three data structures: `attribute_idx`, `attribute_dict` and `max_attr_vals`.
- `attribute_idx` contains the index of each catrgorical feature in `texas_100x_features.p`.
- `attribute_dict` contains the feature dictionary with a label for each feature outcome.
- `max_attr_vals` contains the maximum value of each feature, since the feature values in `texas_100x_features.p` are normalized by dividing with the maximum value.


## Disclosure

This data set is only intended to be used as an academic benchmark data set for machine learning tasks and to analyze the privacy leakage of the models. The records in the data set are anonymized to protect the identity of the patients and only a numeric Hospital ID is provided for the sake of demographic visualization and data sampling. Any attempt to identify the individuals is strictly prohibited. Finally, no demographic conclusions or decisions should be made from the data set that harm the population. Any other use of the data set requires permission from the Texas Department of State Health Services (DSHS). 


## Source

Texas Hospital Inpatient Discharge Public Use Data File, [Quarters 1-4, 2006]. Texas Department of State Health Services, Austin, Texas. [June 21, 2022].
