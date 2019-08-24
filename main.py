"""
Labels reformatter for car detected from pictures taken from moving UAV (drone)


Permission is hereby granted, free of charge, 
to any person obtaining a copy of this software 
and associated documentation files (the "Software"), 
to deal in the Software without restriction, 
including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice 
shall be included in all copies or substantial portions 
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF 
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
from os import walk


def read_file(root, file_name):
    """
    given a text file, read the file and return a file handle
    :param root: path to the folder
    :param file_name: the original file name
    :return: the file handle corresponding to the file, and the file name
    """
    # todo:  ensure the file exist
    return open(root+file_name), file_name


def label_available(original_file_name, new_label_folder="./new_label/"):
    """
    Check whether the label modified file has already been created
    :return: boolean
    """
    for root_dir in new_label_folder:
        if os.path.exists(root_dir + original_file_name):
            return True
        return False


def record(new_label, original_file_name, new_label_folder="./new_label/"):
    """
    Write the new label in the corresponding new file
    :param new_label: created new version of the label
    :param original_file_name: the same name as the original file name
    :param new_label_folder: the new folder to store the new file with new labels
    :return: void
    """
    file_handle = open(new_label_folder + original_file_name, "a+")
    file_handle.write(new_label+"\r\n")
    file_handle.close()


def convert_labelling(file_handle, original_file_name):
    """
    Convert the labelling for top left xy bottom right xy to
    match the labelling using in https://github.com/VisDrone/VisDrone2018-DET-toolkit
    Expected outcome e.g.: 708,471,74,33,1,4,0,1
        The x coordinate of the top-left
        The y coordinate of the top-left
        The width in pixels of the predicted object bounding box
        The height in pixels of the predicted object bounding box
        The score: 1
        The object category: 4
        The score in the DETECTION: 0
        The score in the DETECTION: 0

    :param file_handle: from the original label file
    :param original_file_name: the original label file name
    :return: void
    """
    # read each line in the file
    ignore_flag = 1
    for line in file_handle:
        # remove trailing spaces
        line = str(line).strip()
        # ignore the first line
        if ignore_flag > 0:
            ignore_flag -= 1
            continue
        # get all 4 values from the file
        needed_values = line.split()[0:-1]
        elements = [int(x) for x in needed_values]
        x = elements[0]
        y = elements[1]
        width = abs(elements[2] - elements[0])
        height = abs(elements[3] - elements[1])
        # new label e.g.: 708,471,74,33,1,4,0,1
        new_label = f'{x},{y},{width},{height},1,4,0,0'
        # record change
        record(new_label, original_file_name, "./new_label/")
        print(f'{line} \t - \t {new_label}')


if __name__ == '__main__':
    root_dir_source = os.path.dirname(os.path.realpath(__file__)) + "/original_labels/"
    file_names_ = list()
    for (dir_path, dir_names, file_names) in walk(root_dir_source):
        file_names_ = file_names
    for file_name_source in file_names_:
        f_handle, file_name = read_file(root_dir_source, file_name_source)
        convert_labelling(f_handle, file_name)
    print("Completed")

