# Classifier

- [Classifier](#classifier)
  - [Contains](#contains)
  - [Entry points](#entry-points)
    - [simple\_classification](#simple_classification)
    - [weighted\_classification](#weighted_classification)
  - [Conceptual explanation](#conceptual-explanation)
    - [simple classifier](#simple-classifier)
      - [Determination of a "confidence" (simple)](#determination-of-a-confidence-simple)
    - [weighted classifier](#weighted-classifier)
      - [Determination of a "confidence" (weighted)](#determination-of-a-confidence-weighted)

## Contains

Contains two main functions for age and gender classification.

- `simple classifier` for a simple classification by mean age and mode gender.
- `weighted classifier` for a weighted classification by weighted mean age and weighted mode gender.

A confidence value is also determined by both classifiers

## Entry points

### simple_classification

Use `simple_classifier()` for unweighted classification.

It contains the following steps:

- _classify_age()_: Calculation of mean age and mean similarity per region
- _classify_gender()_: Calculation of the mode of gender and mean similarity per region
- _ensemble_age()_: Calculation of the mean age and mean similarity from the mean values of the regions. Calculation of min and max mean values of the regions
- _ensemble_gender()_: Calculation of the mode of gender from the mode values of the regions
- _confidence_gender()_: Calculates the sum of neighbours with the same gender by the total number of neighbours

### weighted_classification

Use `weighted_classifier()` for weighted classification.

Weights within the regions are similarity values.
For ensemble, use of `ensemble_weight_dict_age` and `ensemble_weight_dict_gender`.

It contains the following steps:

- _weighted_classify_age()_: Calculation of weighted mean age per region
- _weighted_classify_gender()_: Calculates the weighted mode (most common value based on weights)
- _weighted_ensemble_age()_: Calculation of the weighted mean age from the weighted mean values of the regions. With `ensemble_weight_dict_age` as weights
- _confidence_intervall_age()_: Calculates the 5% and 95% quantile of the age values from all data
- _weighted_ensemble_gender()_: Calculation of the weighted mode gender from the weighted mode values of the regions. With `ensemble_weight_dict_gender` as weights
- _caculate_weighted_confidence_gender()_: Calculates the sum of the weights of the neighbours with the same gender as the predicted gender by the total number of weights

## Conceptual explanation

In both classification methods, age and gender are first classified per region. The final classification is based on these results.

### simple classifier

The mean value is calculated for age and the mode for gender. It is irrelevant how similar the embedding of the neighbour was.

#### Determination of a "confidence" (simple)

**AGE**
_Confidence_: Determining a meaningful value is difficult. For this reason, the mean value of the similarity is determined from the mean values of the regions for the first analysis. Note that this says nothing about the confidence of the age prediction, only about the mean similarity of the neighbours. The higher the value, the more similar were the neighbours.

_Interval_: An interval from the smallest mean value to the largest shows the range of the regions-predictions.

**GENDER**
_Confidence_: Determination of the percentage value of how many neighbours correspond to the predicted gender. e.g: 20/35 = 0,57 = 57%

### weighted classifier

The weighted mean value is calculated for age and the weighted mode for gender. The similarity of the neighbours is included by using the similarity as a weight within the regions' classifications.

**for region**:
weights = similarity
To include the results from nearest neighbour determination. The higher the similarity, the more similar are the images of the hands. Therefore, the data of this image is weighted higher than that of hands with low similarity

**ensemble**:
Determination of weights by `classifier_scenario` and `random_forest_feature_importance_scenario`:

- `random_forest_feature_importance_scenario`: determine which region is most relevant for age and gender classification separately
- `classifier_scenario`: test with the weights and check if classification has been improved.

Defaults are based on the results from the scenarios.

#### Determination of a "confidence" (weighted)

**AGE**
_Confidence_: Determination complex, therefore not currently calculated

_Percentile interval_: Optimisation of simple min and max: removing the outliers by removing the upper and lower 5 percent.

**GENDER**
_Confidence_: Total weights corresponding to the prediction/ total weights. Ratio of the weights. Neighbours with a higher weight contribute more to the result.
