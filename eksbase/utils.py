import sys

# A basic exception handling function that allows known errors
def exceptionHandler(exception):
    errorCode = exception.response["Error"]["Code"]
    errorMessage = exception.response["Error"]["Message"]
    
    if errorCode == "NoSuchEntity":
        print("INFO: " + errorMessage)
    elif errorCode == "ResourceNotFoundException":
        print("INFO: " + errorMessage)
    else:
        print("ERROR: An " + errorCode + " exception occurred")
        print("ERROR: " + errorMessage)
        sys.exit()
