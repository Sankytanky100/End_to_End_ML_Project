import sys

def error_message_detail(error, error_detail: sys):
    print("Error detail:", error_detail)  # Print error_detail for debugging
    _, _, exc_tb = error_detail
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in Python script '{0}', line number '{1}', error message: '{2}'".format(
        file_name, exc_tb.tb_lineno, str(error))
    return error_message

class CustomException(Exception):
    def __init__(self, error, error_detail: sys):
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_detail=error_detail)
    
    def __str__(self):
        return self.error_message

# Example usage
#if __name__ == "__main__":
    #try:
        # Simulate an error
        #x = 1 / 0
    #except Exception as e:
        # Raise CustomException with detailed error message
        #raise CustomException(e, sys.exc_info())
