from enum import Enum
from uuid import uuid4

log_results = Enum("log_results", ['Debug', 'Info', 'Warning', 'Success', 'Error'])

def log(request_id:uuid4, log_result:log_results, log_message:str):
    print(log_result.name)
    # create guid for request log id

    




if __name__ == "__main__":
    log('asdasd', log_results.Error, "")
    
    