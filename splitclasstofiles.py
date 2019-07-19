#!/usr/bin/python

from pathlib import Path
from os import path, makedirs
from re import search, findall

# extract classname from string
def get_class_str_by_type(reg, string):
    # define regex
    reg_coding_chars = "`~@#$%^&*\(\)-_=+\[\]\{\}\\|;:'\",.\<\>/?"
    reg_comment = "(/\*+[\n\t\w\s*@/.]+\*{1,}/\n)?"
    reg_class = "class\s\w+" + reg
    reg_comment_and_class = "(" + reg_comment + reg_class + ")"
    # set defaults and attempt
    string_after_captured_class = None
    captured_class = string
    try:
        class_first_char = search(reg_comment_and_class, string).start()
        class_last_char = search("\n}", string).end()
        captured_class = string[class_first_char:class_last_char]
        string_after_captured_class = string[class_last_char:]
    except:
        # Probably a None value was tried and failed
        pass
    return captured_class, string_after_captured_class


# Split file to return separate model and controller classes
def split_model_and_controller(f):
    str_file = "".join(f)
    model, str_file = get_class_str_by_type("Page", str_file)
    controller, str_file = get_class_str_by_type("Controller", str_file)
    return model, controller


# Split and reverse a path name to return file name
def get_current_classname(filepath):
    return str(filepath).split("/")[::-1][0].split(".")[0]


# Write clss string to a given file
def write_class_to_file(filepath, filename, class_):
    if not path.exists("app/src/" + filepath):
        makedirs("app/src/" + filepath)
    fullpath = "app/src/" + filepath
    fullpathtofile = fullpath + "/" + filename + ".php"
    fullphpfile = "<?php\n\n" + class_
    file = open(fullpathtofile, "w")
    file.write(fullphpfile)
    file.close()
    print("Write success: " + fullpathtofile)


# Display error message if no classes found
def display_error_if_no_classes(d):
    for classtype, entries in d.items():
        if 0 == len(entries):
            print(
                "No " + classtype + " classes found in location '" + path_to_files + "'"
            )


# Add a index and value to dictionary
def add_to_dict(dict, i, v):
    if v != None:
        dict[i] = v


# Actions start
print("Splitting model and controller classes:")

# Prompt user for path
path_to_files = input("Please enter the path of your files (e.g. mysite/code): ")

all_models = {}
all_controllers = {}
# loop and read all php files then print containing classes
for filepath in Path(path_to_files).glob("**/*.php"):
    filename = get_current_classname(filepath)
    with open(filepath.absolute()) as f:
        model, controller = split_model_and_controller(f.readlines())
        # store only if not None
        add_to_dict(all_models, filename, model)
        add_to_dict(all_controllers, filename, controller)

display_error_if_no_classes({"model": all_models, "controller": all_controllers})

# write all classes to file
for filename, model in all_models.items():
    write_class_to_file("Model", filename, model)
for filename, controller in all_controllers.items():
    write_class_to_file("Control", filename + "Controller", controller)

# Actions end
print("Class splitting complete.")
