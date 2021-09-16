#Name: Eric Liu
#StudentID: 56277704

from pathlib import Path
from shutil import copyfile
#Part 1
#Read a line of input that specifies which files are eligible to be found

#Input
  #D, followed by a space, followed by the path to a directory 
  #R, followed by a space, followed by the path to a directory

#Output
  #Starts with D -> List of all files in that directory, but no subdirectories
  #Starts with R -> List of all files in that directory, along with all of the
  #files in its subdirectories, all of the files in their subdirectories, and so on

def find_files(directory: str) -> [Path]:
    """return a list of Path of files that are under consideration
    """
    p = Path(directory[2:])
    if p == Path(''): raise 
    if directory[0:2] == 'D ': return d_find_files(p)
    if directory[0:2] == 'R ': return r_find_files(p)
    else: raise
    
def d_find_files(directory: Path) -> [Path]:
    lst = []
    for thing in directory.iterdir():
        if thing.is_file(): lst.append(thing)
    lst.sort(key = lex_order)
    return lst

def r_find_files(directory: Path) -> [Path]:
    lst = []
    dlst = []
    for thing in directory.iterdir():
        if thing.is_file(): lst.append(thing)
        if thing.is_dir(): dlst.append(thing)
    lst.sort(key = lex_order)
    dlst.sort(key = lex_order)
    for folder in dlst:
            lst += r_find_files(folder)
    return lst

def lex_order(p: Path) -> str:
    """Because for Path object in Windows, when comparing two paths, paths are not case-sensitive.
    e.g. Path('a') == Path('A') -> True
    Therefore, this function uses as a key of the list.sort() function
    to make the Paths in a list are in lexicographical ordering.
    """
    if p.is_file(): return p.name
    if p.is_dir(): return p.parts[-1]

#Part 2
#reads a line of input that describes the search characteristics that will be
#used to decide whether files are "interesting"

#Input:
    #A
    #N, followed by a space, followed by the name of the files
    #E, followed by a space, followed by the desired extension
    #T, followed by a space, followed by the given text
    #<, followed by a space, followed by a non-negative integer(size threshold)
    #>, followed by a space, followed by a non-negative integer(size threshold)
#Output:
    #Starts with A -> a list of all files found in the previous step
    #Starts with N -> a list of all files whose names exactly match a particular name
    #Starts with E -> a list of all files with given extension
    #Starts with T -> a list of all files that contain the given text
    #Starts with < -> a list of all files whose size are less than a specified threshold
    #Starts with > -> a list of all files whose size are greater than a specified threshold

def choose_files(flst: [Path], fneed: str) -> [Path]:
    """Return a list of Path of files that are interesting
    """
    if fneed == 'A': return a_choose_files(flst)
    if fneed[0:2] == 'N ': return n_choose_files(flst, fneed[2:])
    if fneed[0:2] == 'E ': return e_choose_files(flst, fneed[2:])
    if fneed[0:2] == 'T ': return t_choose_files(flst, fneed[2:])
    if fneed[0:2] == '< ': return l_choose_files(flst, int(fneed[2:]))
    if fneed[0:2] == '> ': return g_choose_files(flst, int(fneed[2:]))
    else: raise

def a_choose_files(flst: [Path]) -> [Path]:
    return flst

def n_choose_files(flst: [Path], fname:  str) -> [Path]:
    lst = []
    for file in flst:
        if file.name == fname: lst.append(file)
    return lst

def e_choose_files(flst: [Path], fext:  str) -> [Path]:
    lst = []
    for file in flst:
        if file.suffix == fext or file.suffix == '.'+fext: lst.append(file)
    return lst

def t_choose_files(flst: [Path], ftxt:  str) -> [Path]:
    lst = []
    for file in flst:
        try:
            f = file.open()
            text = f.read()
            if ftxt in text: lst.append(file)
        except:
            continue
    return lst
            

def l_choose_files(flst: [Path], fsize:  int) -> [Path]:
    lst = []
    for file in flst:
        if file.stat().st_size < fsize: lst.append(file)
    return lst

def g_choose_files(flst: [Path], fsize:  int) -> [Path]:
    lst = []
    for file in flst:
        if file.stat().st_size > fsize: lst.append(file)
    return lst   

#Part 3
#reads a line of input that describes the action that will be taken on each interesting file

#Input:
    #F
    #D
    #T

#Output:
    #F -> print the first line of text from the file if it's a text file;
    #print NOT TEXT if it is not
    #D -> make a duplicate copy of the file and store it in the same directory where the original resides,
    #but the copy should have .dup (short for "duplicate") appended to its filename
    #T -> modify its last modified timestamp to be the current date/time

def action_handler(flst: [Path], act: str) -> None:
    """take an certain action of the files in a list
    """
    if act == 'F':
        for file in flst:
            try:
                with file.open('r') as f: text = f.readline()
                if text != '' and text[-1] == '\n': text = text[:-1]
                print(text)
            except:
                print('NOT TEXT')
    if act == 'D':
        for file in flst:
            suf = file.suffix + '.dup'
            dst = file.with_suffix(suf)
            copyfile(file, dst)
    if act == 'T':
        for file in flst:
            file.touch()
    else: raise      
        
    
#################################################################################       
if __name__ == '__main__':

    ##Find the files that are in consideration
    while True:
        directory = input()
        try:
            files_list = find_files(directory)
            for file in files_list: print(file)
            break
        except:
            print('ERROR')

    ##Find the files that are "interesting" and should have action taken on them later
    while True:
        files_needed = input()
        try:
            files_list = choose_files(files_list, files_needed)
            for file in files_list:print(file)
            break
        except:
            print('ERROR')

    ##Take action of the files
    while True:
        action = input()
       
        action_handler(files_list, action)
        break
        
    
