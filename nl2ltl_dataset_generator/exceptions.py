class InvalidDatasetType(Exception):
    def __init__(self, input_dataset_type: str):
        super(InvalidDatasetType, self).__init__(f"'{input_dataset_type}' is not a valid dataset type!")