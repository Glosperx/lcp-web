---
language: ['en', 'ca', 'fil', 'fr', 'de', 'it', 'ja', 'pt', 'si', 'es']
language_details: 'pt-BR'
pretty_name: 'Cleaned up dataset of the Multilingual Lexical Simplification Pipeline (MLSP) shared task hosted at BEA 2024'
tags:
- LS
- lexical simplification
- LCP
- lexical complexity prediction
- CWI
- complex word identification
- multilingual
- evaluation
- test
multilinguality:
- multilingual

language_creators:
- found
annotations_creators:
- crowdsourced, expert-generated

license: 'cc-by-sa-4.0'
size_categories:
- 1K<n<10K
task_categories:
- token-classification
- other
task_ids:
- text-simplification

dataset_info:
- config_name: catalan_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: catalan_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: japanese_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: japanese_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: german_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: german_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: sinhala_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: sinhala_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: all_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: all_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: italian_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: italian_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: english_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: english_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: portuguese_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: portuguese_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: french_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: french_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: spanish_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: spanish_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: filipino_combined_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: complexity
      dtype: float64
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string
- config_name: filipino_ls_labels
  features:
    - name: id
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: target
      dtype: string
    - name: substitution_1
      dtype: string
    - name: substitution_2
      dtype: string
    - name: substitution_3
      dtype: string
    - name: substitution_4
      dtype: string
    - name: substitution_5
      dtype: string
    - name: substitution_6
      dtype: string
    - name: substitution_7
      dtype: string
    - name: substitution_8
      dtype: string
    - name: substitution_9
      dtype: string
    - name: substitution_10
      dtype: string
    - name: substitution_11
      dtype: string
    - name: substitution_12
      dtype: string
    - name: substitution_13
      dtype: string
    - name: substitution_14
      dtype: string
    - name: substitution_15
      dtype: string
    - name: substitution_16
      dtype: string
    - name: substitution_17
      dtype: string
    - name: substitution_18
      dtype: string
    - name: substitution_19
      dtype: string
    - name: substitution_20
      dtype: string
    - name: substitution_21
      dtype: string
    - name: substitution_22
      dtype: string
    - name: substitution_23
      dtype: string
    - name: substitution_24
      dtype: string
    - name: substitution_25
      dtype: string
    - name: substitution_26
      dtype: string
    - name: substitution_27
      dtype: string
    - name: substitution_28
      dtype: string
    - name: substitution_29
      dtype: string
    - name: substitution_30
      dtype: string

configs:
- config_name: catalan_lcp_labels
  data_files:
  - split: test
    path: "Catalan/multils_test_catalan_lcp_labels.tsv"
  - split: trial
    path: "Catalan/multils_trial_catalan_lcp_labels.tsv"
- config_name: catalan_combined_labels
  data_files:
  - split: test
    path: "Catalan/multils_test_catalan_combined_labels.tsv"
  - split: trial
    path: "Catalan/multils_trial_catalan_combined_labels.tsv"
- config_name: catalan_lcp_unlabelled
  data_files:
  - split: test
    path: "Catalan/multils_test_catalan_lcp_unlabelled.tsv"
- config_name: catalan_ls_labels
  data_files:
  - split: test
    path: "Catalan/multils_test_catalan_ls_labels.tsv"
  - split: trial
    path: "Catalan/multils_trial_catalan_ls_labels.tsv"
- config_name: catalan_ls_unlabelled
  data_files:
  - split: test
    path: "Catalan/multils_test_catalan_ls_unlabelled.tsv"
- config_name: japanese_combined_labels
  data_files:
  - split: test
    path: "Japanese/multils_test_japanese_combined_labels.tsv"
  - split: trial
    path: "Japanese/multils_trial_japanese_combined_labels.tsv"
- config_name: japanese_lcp_labels
  data_files:
  - split: test
    path: "Japanese/multils_test_japanese_lcp_labels.tsv"
  - split: trial
    path: "Japanese/multils_trial_japanese_lcp_labels.tsv"
- config_name: japanese_ls_unlabelled
  data_files:
  - split: test
    path: "Japanese/multils_test_japanese_ls_unlabelled.tsv"
- config_name: japanese_lcp_unlabelled
  data_files:
  - split: test
    path: "Japanese/multils_test_japanese_lcp_unlabelled.tsv"
- config_name: japanese_ls_labels
  data_files:
  - split: test
    path: "Japanese/multils_test_japanese_ls_labels.tsv"
  - split: trial
    path: "Japanese/multils_trial_japanese_ls_labels.tsv"
- config_name: german_combined_labels
  data_files:
  - split: test
    path: "German/multils_test_german_combined_labels.tsv"
  - split: trial
    path: "German/multils_trial_german_combined_labels.tsv"
- config_name: german_lcp_unlabelled
  data_files:
  - split: test
    path: "German/multils_test_german_lcp_unlabelled.tsv"
- config_name: german_ls_labels
  data_files:
  - split: test
    path: "German/multils_test_german_ls_labels.tsv"
  - split: trial
    path: "German/multils_trial_german_ls_labels.tsv"
- config_name: german_ls_unlabelled
  data_files:
  - split: test
    path: "German/multils_test_german_ls_unlabelled.tsv"
- config_name: german_lcp_labels
  data_files:
  - split: test
    path: "German/multils_test_german_lcp_labels.tsv"
  - split: trial
    path: "German/multils_trial_german_lcp_labels.tsv"
- config_name: sinhala_ls_labels
  data_files:
  - split: test
    path: "Sinhala/multils_test_sinhala_ls_labels.tsv"
  - split: trial
    path: "Sinhala/multils_trial_sinhala_ls_labels.tsv"
- config_name: sinhala_lcp_labels
  data_files:
  - split: test
    path: "Sinhala/multils_test_sinhala_lcp_labels.tsv"
  - split: trial
    path: "Sinhala/multils_trial_sinhala_lcp_labels.tsv"
- config_name: sinhala_combined_labels
  data_files:
  - split: test
    path: "Sinhala/multils_test_sinhala_combined_labels.tsv"
  - split: trial
    path: "Sinhala/multils_trial_sinhala_combined_labels.tsv"
- config_name: sinhala_ls_unlabelled
  data_files:
  - split: test
    path: "Sinhala/multils_test_sinhala_ls_unlabelled.tsv"
- config_name: sinhala_lcp_unlabelled
  data_files:
  - split: test
    path: "Sinhala/multils_test_sinhala_lcp_unlabelled.tsv"
- config_name: all_ls_unlabelled
  data_files:
  - split: test
    path: "All/multils_test_all_ls_unlabelled.tsv"
- config_name: all_ls_labels
  data_files:
  - split: test
    path: "All/multils_test_all_ls_labels.tsv"
  - split: trial
    path: "All/multils_trial_all_ls_labels.tsv"
- config_name: all_combined_labels
  data_files:
  - split: test
    path: "All/multils_test_all_combined_labels.tsv"
  - split: trial
    path: "All/multils_trial_all_combined_labels.tsv"
- config_name: all_lcp_unlabelled
  data_files:
  - split: test
    path: "All/multils_test_all_lcp_unlabelled.tsv"
- config_name: all_lcp_labels
  data_files:
  - split: test
    path: "All/multils_test_all_lcp_labels.tsv"
  - split: trial
    path: "All/multils_trial_all_lcp_labels.tsv"
- config_name: italian_ls_unlabelled
  data_files:
  - split: test
    path: "Italian/multils_test_italian_ls_unlabelled.tsv"
- config_name: italian_lcp_labels
  data_files:
  - split: test
    path: "Italian/multils_test_italian_lcp_labels.tsv"
  - split: trial
    path: "Italian/multils_trial_italian_lcp_labels.tsv"
- config_name: italian_lcp_unlabelled
  data_files:
  - split: test
    path: "Italian/multils_test_italian_lcp_unlabelled.tsv"
- config_name: italian_ls_labels
  data_files:
  - split: test
    path: "Italian/multils_test_italian_ls_labels.tsv"
  - split: trial
    path: "Italian/multils_trial_italian_ls_labels.tsv"
- config_name: italian_combined_labels
  data_files:
  - split: test
    path: "Italian/multils_test_italian_combined_labels.tsv"
  - split: trial
    path: "Italian/multils_trial_italian_combined_labels.tsv"
- config_name: english_lcp_unlabelled
  data_files:
  - split: test
    path: "English/multils_test_english_lcp_unlabelled.tsv"
- config_name: english_ls_unlabelled
  data_files:
  - split: test
    path: "English/multils_test_english_ls_unlabelled.tsv"
- config_name: english_lcp_labels
  data_files:
  - split: test
    path: "English/multils_test_english_lcp_labels.tsv"
  - split: trial
    path: "English/multils_trial_english_lcp_labels.tsv"
- config_name: english_combined_labels
  data_files:
  - split: test
    path: "English/multils_test_english_combined_labels.tsv"
  - split: trial
    path: "English/multils_trial_english_combined_labels.tsv"
- config_name: english_ls_labels
  data_files:
  - split: test
    path: "English/multils_test_english_ls_labels.tsv"
  - split: trial
    path: "English/multils_trial_english_ls_labels.tsv"
- config_name: portuguese_ls_labels
  data_files:
  - split: test
    path: "Portuguese/multils_test_portuguese_ls_labels.tsv"
  - split: trial
    path: "Portuguese/multils_trial_portuguese_ls_labels.tsv"
- config_name: portuguese_lcp_unlabelled
  data_files:
  - split: test
    path: "Portuguese/multils_test_portuguese_lcp_unlabelled.tsv"
- config_name: portuguese_ls_unlabelled
  data_files:
  - split: test
    path: "Portuguese/multils_test_portuguese_ls_unlabelled.tsv"
- config_name: portuguese_lcp_labels
  data_files:
  - split: test
    path: "Portuguese/multils_test_portuguese_lcp_labels.tsv"
  - split: trial
    path: "Portuguese/multils_trial_portuguese_lcp_labels.tsv"
- config_name: portuguese_combined_labels
  data_files:
  - split: test
    path: "Portuguese/multils_test_portuguese_combined_labels.tsv"
  - split: trial
    path: "Portuguese/multils_trial_portuguese_combined_labels.tsv"
- config_name: french_lcp_labels
  data_files:
  - split: test
    path: "French/multils_test_french_lcp_labels.tsv"
  - split: trial
    path: "French/multils_trial_french_lcp_labels.tsv"
- config_name: french_lcp_unlabelled
  data_files:
  - split: test
    path: "French/multils_test_french_lcp_unlabelled.tsv"
- config_name: french_combined_labels
  data_files:
  - split: test
    path: "French/multils_test_french_combined_labels.tsv"
  - split: trial
    path: "French/multils_trial_french_combined_labels.tsv"
- config_name: french_ls_labels
  data_files:
  - split: test
    path: "French/multils_test_french_ls_labels.tsv"
  - split: trial
    path: "French/multils_trial_french_ls_labels.tsv"
- config_name: french_ls_unlabelled
  data_files:
  - split: test
    path: "French/multils_test_french_ls_unlabelled.tsv"
- config_name: spanish_lcp_labels
  data_files:
  - split: test
    path: "Spanish/multils_test_spanish_lcp_labels.tsv"
  - split: trial
    path: "Spanish/multils_trial_spanish_lcp_labels.tsv"
- config_name: spanish_ls_labels
  data_files:
  - split: test
    path: "Spanish/multils_test_spanish_ls_labels.tsv"
  - split: trial
    path: "Spanish/multils_trial_spanish_ls_labels.tsv"
- config_name: spanish_ls_unlabelled
  data_files:
  - split: test
    path: "Spanish/multils_test_spanish_ls_unlabelled.tsv"
- config_name: spanish_combined_labels
  data_files:
  - split: test
    path: "Spanish/multils_test_spanish_combined_labels.tsv"
  - split: trial
    path: "Spanish/multils_trial_spanish_combined_labels.tsv"
- config_name: spanish_lcp_unlabelled
  data_files:
  - split: test
    path: "Spanish/multils_test_spanish_lcp_unlabelled.tsv"
- config_name: filipino_combined_labels
  data_files:
  - split: test
    path: "Filipino/multils_test_filipino_combined_labels.tsv"
  - split: trial
    path: "Filipino/multils_trial_filipino_combined_labels.tsv"
- config_name: filipino_lcp_labels
  data_files:
  - split: test
    path: "Filipino/multils_test_filipino_lcp_labels.tsv"
  - split: trial
    path: "Filipino/multils_trial_filipino_lcp_labels.tsv"
- config_name: filipino_lcp_unlabelled
  data_files:
  - split: test
    path: "Filipino/multils_test_filipino_lcp_unlabelled.tsv"
- config_name: filipino_ls_unlabelled
  data_files:
  - split: test
    path: "Filipino/multils_test_filipino_ls_unlabelled.tsv"
- config_name: filipino_ls_labels
  data_files:
  - split: test
    path: "Filipino/multils_test_filipino_ls_labels.tsv"
  - split: trial
    path: "Filipino/multils_trial_filipino_ls_labels.tsv"

extra_gated_prompt: 'To avoid leaking the dataset to LLM training data, it is not distributed on the open web.'
extra_gated_fields:
  I agree not to make the MLSP2024 dataset, or any part of it, available on the open web: checkbox
---

The MultiLS dataset was created as part of the MLSP2024 shared task. 
The dataset contains 5,624 instances across 10 target languages. 
Each instance consists of a sentence from an educational text, with a marked target word. 
For each target word in the given context, two annotations are given. 
Firstly, an aggregate complexity score derived from asking 10 annotators to mark the level of difficulty of the target token on a scale of 1-5.
Secondly, a list of possible substitutions for the target word which would make the original sentence easier to understand whilst retaining the original meaning. 
These two tasks constitute important steps in the lexical simplification pipeline, a method of simplifying texts in a targeted manner for end users.
Further information on the dataset and the protocols used to create it are available at the following references. Please provide citations using the bibtex entries below.

**Updated 2024/6/16:**
- Corrected complexity values for Japanese (values originally used in the shared task were 4/5 of the actual values due to a mistake in normalization).
- Added trial data for all languages (available as "trial" split).

Note that in the shared task the Japanese complexity values were downscaled to 4/5 consistently across trial and test split, so the effect on the shared task results should be minimal, if any.

# Shared Task Report

```
@inproceedings{shardlow2024bea,
title={{The BEA 2024 Shared Task on the Multilingual Lexical Simplification Pipeline}},
author={Shardlow, Matthew and Alva-Manchego, Fernando and Batista-Navarro, Riza and Bott, Stefan and Calderon Ramirez, Saul and Cardon, Rémi and François, Thomas and Hayakawa, Akio and Horbach, Andrea and Huelsing, Anna and Ide, Yusuke and Imperial, Joseph Marvin and Nohejl, Adam and North, Kai and Occhipinti, Laura and Peréz Rojas, Nelson and Raihan, Nishat and Ranasinghe, Tharindu and Solis Salazar, Martin and \v{S}tajner, Sanja and Zampieri, Marcos and Saggion, Horacio},
booktitle={Proceedings of the 19th Workshop on Innovative Use of NLP for Building Educational Applications (BEA)},
year={2024}
}
```

# Datasets
```
@inproceedings{shardlow2024readi,
title={{An Extensible Massively Multilingual Lexical Simplification Pipeline Dataset using the MultiLS Framework}},
author={Shardlow, Matthew and Alva-Manchego, Fernando and Batista-Navarro, Riza and Bott, Stefan and Calderon Ramirez, Saul and Cardon, Rémi and François, Thomas and Hayakawa, Akio and Horbach, Andrea and Huelsing, Anna and Ide, Yusuke and Imperial, Joseph Marvin and Nohejl, Adam and North, Kai and Occhipinti, Laura and Peréz Rojas, Nelson and Raihan, Nishat and Ranasinghe, Tharindu and Solis Salazar, Martin and Zampieri, Marcos and Saggion, Horacio},
booktitle={Proceedings of the 3rd Workshop on Tools and Resources for People with REAding DIfficulties (READI)},
year={2024}
}
```
# MultiLS Framework ([link](https://arxiv.org/abs/2402.14972))
```
@article{north2024multils,
  title={MultiLS: A Multi-task Lexical Simplification Framework},
  author={North, Kai and Ranasinghe, Tharindu and Shardlow, Matthew and Zampieri, Marcos},
  journal={arXiv preprint arXiv:2402.14972},
  year={2024}
}
```
# Spanish and Catalan Datasets
```
@misc{bott2024multilsspca,
      title={MultiLS-SP/CA: Lexical Complexity Prediction and Lexical Simplification Resources for Catalan and Spanish},
      author={Stefan Bott and Horacio Saggion and Nelson Peréz Rojas and Martin Solis Salazar and Saul Calderon Ramirez},
      year={2024},
      eprint={2404.07814},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```