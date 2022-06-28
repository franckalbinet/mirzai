# mirzai
> Making the research: "Prediction of Exchangeable Potassium in Soil through Mid-Infrared Spectroscopy and Deep Learning: from Prediction to Explainability, Albinet et al., 2022" reproducible. 


Making the following **research paper reproducible**:
> "Prediction of Exchangeable Potassium in Soil through Mid-Infrared Spectroscopy and Deep Learning:from Prediction to Explainability, Albinet et al., 2022" 

Link ... (upon acceptance)

## Paper with code

1. [Exploratory Data Analysis (EDA)](paper.eda.html)

2. [Data selection and transformation](paper.select_transform.html)

3. Baseline model (PLSR):
    * [Learning curve](paper.plsr.learning_curve.html)
    * [Validation curve](paper.plsr.validation_curve.html)
    * [Training & evaluation](paper.plsr.train_eval.html)

4. Convolutional Neural Network (CNN):
    * [Learning rate finder](paper.cnn.lr_finder.html)
    * [Learning curve](paper.cnn.learning_curve.html)
    * [Validation curve](paper.cnn.validation_curve.html)
    * [Training & evaluation](paper.cnn.train_eval.html)
    * [Overfitting in action](placeholder.html)
    
5. PLSR vs. CNN figures:
    * [Learning curves](paper.figures.learning_curves.html)
    * [Validation curves](paper.figures.validation_curves.html)
    * [Observed vs. predicted scatterplots](placeholder.html)
    * [Global vs. local modelling](placeholder.html)

6. Interpretability     
    * [GradientShap values](placeholder.html)
    * [GradientShap values correlation](placeholder.html)

## Install

`pip install mirzai`

## Setup

### Getting the data

A zipped archive of the data used in this study are available for download at the following link: [https://drive.google.com/file/d/1ozHZ8KHZeuaiv8lTycxe2-yo27BhFnUt/view?usp=sharing](https://drive.google.com/file/d/1ozHZ8KHZeuaiv8lTycxe2-yo27BhFnUt/view?usp=sharing)


### In a local environment

The preferred way it to use [Mamba](https://mamba.readthedocs.io)

### In Google Colab

...

## Acknowledgements

*This work was carried out in the context of the IAEA funded Coordinated Research Project (CRP D1.50.19) titled [“Remediation of Radioactive Contaminated Agricultural Land”](https://www.iaea.org/projects/crp/d15019), under IAEA Technical Contract n°23685. 

We also thank Richard Ferguson from Kellogg Soil Survey Laboratory for providing access to the USDA MIR soil spectra library and the r equired training sessions for its operation.*
