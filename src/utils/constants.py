# Description: Constants used in the application utilitary functions.
from fastapi import status

# Confidence level for lists on histograms
PLOT_CONFIDENCE = 0.99

# HTTP status codes
OK_200 = status.HTTP_200_OK
CREATED_201 = status.HTTP_201_CREATED
BAD_REQUEST_400 = status.HTTP_400_BAD_REQUEST
INTERNAL_SERVER_ERROR_500 = status.HTTP_500_INTERNAL_SERVER_ERROR
