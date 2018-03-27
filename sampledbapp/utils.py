import os
from django.contrib.auth.models import Group

# Recursively check filename and add the iterator to the end.
def build_and_check_file_name(folder_path,iterator,file_name):

    if iterator == 0:

        full_path = os.path.join(folder_path,file_name)
    else:
        full_path = os.path.join(folder_path,file_name + "[" + str(iterator) + "]")

    # Check if its a file or not. If it is, call function again with increased iterator
    if os.path.isfile(full_path):
        file_name = build_and_check_file_name(folder_path,iterator+1,file_name)

    elif iterator == 0:
        file_name = file_name
    else:
        file_split = file_name.split('.')
        file_name = file_split[0]  + "[" + str(iterator) + "]." + file_split[1]

    return file_name

