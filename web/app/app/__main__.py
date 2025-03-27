from app.smartScript import main
import sys

if __name__ == "__main__":  
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
        if fileName.endswith('.jjs'):
            with open(fileName, 'r') as file:
                args = file.read()
        else:
            raise Exception("Invalid file type")
    else:
        args = None

    main(args)