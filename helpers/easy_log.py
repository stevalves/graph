import datetime

def easy_log(status, message):
    status_list = {
        "INFO": "[!]",
        "WARNING": "[?]",
        "ERROR": "[X]",
        "SUCCESS": "[✓]",
        "OPTION": "[>]",
        "CASE": "[#]",
    }

    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    print(f"{agora} {status_list.get(status, '[⚪]')} {message}")