import sys
import random
import time
import datetime

# Versioning settings
ENVIRONMENT = "github"
VERSION = '0.0.1-%s' % ENVIRONMENT

# Global init, default settings below.
FAST_MODE = False
NUMBER_OF_PROGRESS_INDIC_UPDATES = 500


# Colors for print().
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ShowNoArgumentsMessage():
    print("You have not specified any argument.")
    print("Usage: python3 search.py [file_path] [wanted_email(s)] [option(s)]")
    print("Type '-h' or '--help' to find out more about search.py.")

def ShowHelp():
    print("Search.py, version %s" % VERSION)
    print("Type '-h' or '--help' to see this list.")
    print("Usage:")
    print("    python3 search.py [file_path] [wanted_email(s)] [option(s)]")
    print("Wanted emails can also be loaded from text files.")
    print("To do so, the first argument must be the path to that file.")
    print("Options and arguments:")
    print("    FAST MODE: '-f' or '--fast'")
    print("        Skips checking the file's length and skips having a progress indicator.")
    print("        Defaults to %s." % FAST_MODE)
    print("    PROGRESS BAR UPDATES: '-up=[n]' or '--progress-update=[n]'")
    print("        The amount of updates of the percentage when checking lines in a file.")
    print("        Cannot be used in FAST MODE.")
    print("        Defaults to %d." % NUMBER_OF_PROGRESS_INDIC_UPDATES)
    print("Example usage:")
    print("    python3 search.py canva.txt wanted_emails.txt -f")
    print("    python3 search.py ./Canvas/canva.txt myemail@gmail.com youremail@gmail.com")
    print("    python3 search.py passuser-file.txt myemail@gmail.com -up=100")


"""
Returns the read FILE_PATH and given array of WANTED_EMAILS.
"""
def ReadArguments():
    # Remove first argument, as that is the name of the file (search.py).
    sys.argv.pop(0)

    # If no argument is given, show basic help.
    try:
        if sys.argv[0] == "-h" or sys.argv[0] == "--help":
            ShowHelp()
            exit()
        # The next argument must be the file.
        FILE_PATH = sys.argv[0]
        sys.argv.pop(0)
    except IndexError:
        ShowNoArgumentsMessage()
        exit()

    # Look for valid arguments and remove them from sys.argv[],
    # therefore later all the given arguments can be used as emails.
    # This avoids having set e.g "-f" as a wanted email.
    toPop = []
    WANTED_EMAILS = []
    areEmailsInFile = False

    for i in range(0, len(sys.argv)):
        # FAST_MODE
        if sys.argv[i] == "-f" or sys.argv[i] == "--fast":
            global FAST_MODE
            FAST_MODE = True
            toPop.append(i)
        # NUMBER_OF_PROGRESS_INDIC_UPDATES
        elif "-up=" in sys.argv[i] or "--progress-update=" in sys.argv[i]:
            value = sys.argv[i].split("=")[1]
            global NUMBER_OF_PROGRESS_INDIC_UPDATES
            NUMBER_OF_PROGRESS_INDIC_UPDATES = int(value)
            toPop.append(i)
        # WANTED_EMAILS TEXTFILE
        elif ".txt" in sys.argv[i]:
            areEmailsInFile = True
            with open(sys.argv[i], "r") as f:
                for line in f:
                    if "@" in line:
                        wanted_email = line.replace("\n", "")
                        WANTED_EMAILS.append(wanted_email)
                    else:
                        print(bcolors.FAIL + "Wrong email format in the file %s" % sys.argv[2] + bcolors.ENDC)
                        exit()
    # Only popping from array after finished looping, thus avoiding
    # unexpected errors.
    for i in toPop:
        sys.argv.pop(i)

    # If there are no remaining arguments and emails after parsing for
    # other options, exit with error.
    if not areEmailsInFile and len(sys.argv) == 0:
        print(bcolors.FAIL + "ERROR: No wanted email given!" + bcolors.ENDC)
        exit()

    if not areEmailsInFile:
        # Loop through all remaining given arguments and expect them to be emails.
        for i in range(0, len(sys.argv)):
            WANTED_EMAILS.append(sys.argv[i])

    return (FILE_PATH, WANTED_EMAILS)

def CheckLine(line, lineNumber):
    # Check if any wanted email is in line
    for email in WANTED_EMAILS:
        if email in line:
            print(bcolors.OKCYAN + "ooo Found %s at line %s" % (email, lineNumber) + bcolors.ENDC)
            print(bcolors.OKCYAN + "ooo The exact line is: %s" % line.replace("\n","") + bcolors.ENDC)

def PrintWelcomeMessage():
    print("\n")
    print(bcolors.FAIL + "Welcome to ...\n" + bcolors.ENDC)
    print(bcolors.FAIL + "  ______   ________   ______   _______    ______   __    __      _______  __      __ " + bcolors.ENDC)
    print(bcolors.FAIL + " /      \ |        \ /      \ |       \  /      \ |  \  |  \    |       \|  \    /  \\" + bcolors.ENDC)
    print(bcolors.FAIL + "|  $$$$$$\| $$$$$$$$|  $$$$$$\| $$$$$$$\|  $$$$$$\| $$  | $$    | $$$$$$$\\$$\  /  $$" + bcolors.ENDC)
    print(bcolors.FAIL + "| $$___\$$| $$__    | $$__| $$| $$__| $$| $$   \$$| $$__| $$    | $$__/ $$ \$$\/  $$ " + bcolors.ENDC)
    print(bcolors.FAIL + " \$$    \ | $$  \   | $$    $$| $$    $$| $$      | $$    $$    | $$    $$  \$$  $$  " + bcolors.ENDC)
    print(bcolors.FAIL + " _\$$$$$$\| $$$$$   | $$$$$$$$| $$$$$$$\| $$   __ | $$$$$$$$    | $$$$$$$    \$$$$   " + bcolors.ENDC)
    print(bcolors.FAIL + "|  \__| $$| $$_____ | $$  | $$| $$  | $$| $$__/  \| $$  | $$ __ | $$         | $$    " + bcolors.ENDC)
    print(bcolors.FAIL + " \$$    $$| $$     \| $$  | $$| $$  | $$ \$$    $$| $$  | $$|  \| $$         | $$    " + bcolors.ENDC)
    print(bcolors.FAIL + "  \$$$$$$  \$$$$$$$$ \$$   \$$ \$$   \$$  \$$$$$$  \$$   \$$ \$$ \$$          \$$    " + bcolors.ENDC)
    print("\n")

def LoadFileIntoMemory(FILE_PATH):
    lines = []
    beginLoading = time.time()

    currentLine = 0
    with open(FILE_PATH, "r") as file:
        print(bcolors.OKBLUE + "OOO Loading file into memory ..." + bcolors.ENDC, end="\r")
        for line in file:
            currentLine += 1
            lines.append(line)
    
    endLoading = time.time()
    timeForLoading = endLoading - beginLoading

    fileLength = currentLine
    print(bcolors.OKGREEN + "ooo Successfully loaded file into memory in %d seconds." % timeForLoading + bcolors.ENDC)
    print(bcolors.OKGREEN + "ooo The file has a length of %d lines." % fileLength + bcolors.ENDC)
    return (lines, fileLength)

if __name__ == '__main__':
    FILE_PATH, WANTED_EMAILS = ReadArguments()


    PrintWelcomeMessage()
    print(bcolors.OKCYAN + "Starting searching with the following arguments:" + bcolors.ENDC)
    print(bcolors.HEADER, end="")
    print("ooo FILE_PATH        = %s" % FILE_PATH)
    print("ooo WANTED_EMAILS    = %d" % len(WANTED_EMAILS))
    print("ooo FAST_MODE        = %s" % FAST_MODE)
    print("ooo PROGRESS_UPDATES = %s" % NUMBER_OF_PROGRESS_INDIC_UPDATES + bcolors.ENDC)
    print()
    print(bcolors.BOLD + bcolors.OKGREEN + "Vamos!" + bcolors.ENDC)

    if not FAST_MODE:
        lines, fileLength = LoadFileIntoMemory(FILE_PATH)
        

        begin = time.time()
        # Check lines from memory.
        for lineNumber, line in enumerate(lines):

            CheckLine(line, lineNumber)
            # Update progress
            if not lineNumber % round(fileLength / NUMBER_OF_PROGRESS_INDIC_UPDATES):
                percentage = str(round( lineNumber / fileLength * 100, 2)) + r"%"
                print(bcolors.OKBLUE + "OOO Checking lines from memory ... %s" % percentage + bcolors.ENDC, end = "\r")

        end = time.time()
        timeToCheck = end - begin

        print(bcolors.OKGREEN + "ooo Checking lines from memory ... 100.00%" + bcolors.ENDC, end = "\r")
        print()
        print(bcolors.OKGREEN + "ooo Done checking file in %d seconds." % timeToCheck + bcolors.ENDC)

    else:
        # Read the file.
        print(bcolors.OKBLUE + "OOO Checking lines from file ..." + bcolors.ENDC, end = "\r")

        begin = time.time()
        currentLine = 0
        with open(FILE_PATH, "r") as file:
            for line in file:
                currentLine += 1
                CheckLine(line, currentLine)
        
        end = time.time()
        timeToCheck = end - begin

        print(bcolors.OKGREEN + "ooo Checking lines from file ..." + bcolors.ENDC, end = "\r")
        print()
        print(bcolors.OKGREEN + "ooo Done checking file in %d seconds." % timeToCheck + bcolors.ENDC)

    print()
    print(bcolors.BOLD + "Thank you for using SEARCH.PY!" + bcolors.ENDC)
