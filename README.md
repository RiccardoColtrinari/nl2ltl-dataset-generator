# NL2LTL Synthetic Dataset Generator


This project provides a generator for synthetic pairs of Linear Temporal Logic formulas and the corresponding Natural Language phrases.

The tool is a command-line utility which has been developed and used for the paper "Neural Machine Translation: from Natural Language requirements to Linear Temporal Logic formulas” by Riccardo Coltrinari, Flavio Corradini, Marco Piangerelli and Barbara Re.

## Overview

This section will contain an overview of the tool, its inputs and outputs.

## Usage

To use the tool, run main.py with the following syntax:

```cmd
main.py [OPTIONS] DATASET_TYPE
```

### Arguments

The tool requires one argument:

- DATASET_TYPE: The type of dataset to generate. This is a required argument and should be one of the following values: *restricted* or *unrestricted*. If the latter is passed then you also must pass the '--identifiers-file-path' option.

### Options

The tool supports the following optional parameters:

- '-s', '--number-of-samples': The number of samples to generate. This should be an integer value. If not provided, the default value is 10000.
- '-o', '--dataset-save-path': The file path to save the generated dataset. If not provided, the default save path is './results/dataset.csv'.
- '-i', '--identifiers-file-path': The file path to the identifiers file. This should be a txt file containing the identifiers expressed in a specific notation. This path is mandatory to generate unrestricted samples, otherwise it can be omitted.
- '-r', '--seed': The random seed to use for generating the dataset. If not provided, a random seed will be used.

## License

This tool is licensed under the MIT license. Please see the LICENSE file for details.

## Support

I am currently working to further improve documentation. However, if you have questions, comments, or you want to report a bug, please open an issue and I will address it as soon as possible.
As a further note, consider that the tool has been created with the sole purpose of meeting the requirements needed to properly run the paper's experiments.
This means that the code may sometimes appear not well engineered and not optimized, as code robustness was not the primary focus of the tool.
However, I will try to improve code's quality where necessary, in the meantime advices and modifications are welcome via pull requests.
