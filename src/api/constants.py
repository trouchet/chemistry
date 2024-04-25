# Description: Constants used in the project

# Time horizon to check for item metrics
DEFAULT_AGE = 12

# Array with valid age months
VALID_AGE_MONTHS = [6, 12, 24, 36]

############ Valid file extensions and content types ############

# CSV content type and extension
CSV_CONTENT_TYPE = "text/csv"
CSV_EXTENSION = "csv"

# XLS content type and extension
XLS_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
XLS_EXTENSION = "xls"
XLSX_EXTENSION = "xlsx"

# Map with file extensions and content types
CONTENT_TYPE_MAP = {
    CSV_EXTENSION: CSV_CONTENT_TYPE,
    XLS_EXTENSION: XLS_CONTENT_TYPE,
    XLSX_EXTENSION: XLS_CONTENT_TYPE
}

# Array with valid content types
VALID_CONTENT_TYPES = [
    CSV_CONTENT_TYPE, XLS_CONTENT_TYPE
]

# Array with valid file types
VALID_EXTENSION_TYPES = [
    CSV_EXTENSION, XLS_EXTENSION, XLSX_EXTENSION
]


