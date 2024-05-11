# Description: Constants used in the project
from fastapi import status

#################################### Routes ##############################

# Códigos de status HTTP
OK_200 = status.HTTP_200_OK
CREATED_201 = status.HTTP_201_CREATED
BAD_REQUEST_400 = status.HTTP_400_BAD_REQUEST
INTERNAL_SERVER_ERROR_500 = status.HTTP_500_INTERNAL_SERVER_ERROR

#################################### File #####################################

# Descrição de tipos válidos para leitura de arquivo
VALID_CONTENT_TYPES = [
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]
VALID_FILE_TYPES = ["csv", "xls", "xlsx"]

#################################### Security #################################

# Username requirements
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20

# Password requirements
MIN_PASSWORD_LENGTH = 8
PASSWORD_REQUIREMENTS_DICT = {
    "min_length": MIN_PASSWORD_LENGTH,
    "min_uppercase": 1,
    "min_lowercase": 1,
    "min_digits": 1,
    "min_special_chars": 1,
}

#################################### Logs ####################################

# Número máximo de arquivos de log
MAX_LOG_FILES = 10
MAX_LOG_FOLDER_SIZE_MB = 10

#################################### MISC ####################################

DEFAULT_TOKEN_LENGTH = 10
