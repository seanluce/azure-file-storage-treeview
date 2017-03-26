import azure.common
from azure.storage import CloudStorageAccount
import sys

##define Azure storage account details
source_account_name = '**insert your storage account name here**'
source_account_key = '**insert your key here**'

##create object that contains the cloud storage account
source_account = CloudStorageAccount(source_account_name, source_account_key)

##create object that contains the file service of the storage account
source_file_service = source_account.create_file_service()

##define the function to list all files and directories within a given folder 
##the function will call itself if there are nested folders, so we include a nest level to track how deep we are to create our indents
def list_file_and_dir(share, current_dir, nest_level): #receiving the current share, current direcotry if any, and nest level
    source_file_list = source_file_service.list_directories_and_files(share.name, current_dir) #build a directory and file list for the current working directory
    for file_or_dir in source_file_list: #interate through each file or directory in the current working directory
        file_type = file_or_dir.__class__.__name__ #get the file type of 'File' or 'Directory' for the current object
        for x in range(0, nest_level): #create our indents based on the current nest level
            sys.stdout.write(str('   ')) #prints a string without a carriage return for our indents
        print('|--' + file_or_dir.name) #the prefix for our file or directory name
        if file_type == 'Directory': #if the current object is a directory, we are going to call this function again
            if current_dir == '': #if we are in the root folder of the share, we don't want to pass a forward slash to the function. '/dirname' is not valid
                list_file_and_dir(share, file_or_dir.name, nest_level + 1)
            else:
                next_dir = current_dir + '/' + file_or_dir.name #if we are in a sub-folder, we want to add a forward slash. 'dirname/subdir' is valid
                list_file_and_dir(share, next_dir, nest_level + 1)

##this is where our main program starts
##build a list of shares within the storage account
source_share_list = source_file_service.list_shares()

##interate through each share and call our function above to enumerate and list all of the files and directories
for share in source_share_list:
    print(share.name + '*') #added '*' here to highlight the shares in the output
    list_file_and_dir(share, '', 1) #calling our function without a directory name speficied
