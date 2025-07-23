from core.usgs_data_download import download_earthquake_data

def main():
    print("Type 'Start' to start downloading data and 'Quit' to exit")
    
    while True:
        command = input("->").strip().lower()
        
        if command == 'start':
            download_earthquake_data()
            
        elif command == 'quit':
            print("Exiting Program")
            break
        
        else:
            print ("INVALID COMMAND")
            
if __name__ == "__main__":
    main()    