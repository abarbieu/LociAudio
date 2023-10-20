import fnmatch
import os
from termcolor import colored

"""
mkdir root
cd root
mkdir \
  d0 \
  d1 \  
  d0/d0_d1
touch \
  f0 \
  d0/d0_f0 \
  d0/d0_f1 \
  d0/d0_d1/d0_d1_f0
tree

OUTPUT:
.
├── d0
│   ├── d0_d1
│   │   └── d0_d1_f0
│   ├── d0_f0
│   └── d0_f1
├── d1
└── f0

OUTPUT:
'root', ['d0', 'd1'], ['f0']
'root/d0', ['d0_d1'], ['d0_f1', 'd0_f0']
'root/d0/d0_d1', [], ['d0_d1_f0']
'root/d1', [], []
"""
def simple_walk_example():
    for path, dirnames, filenames in os.walk('root'):
        print(f'{repr(path)}, {repr(dirnames)}, {repr(filenames)}')


def run_on_dir(input_path, file_func=None, folder_func=None, recursive=False, print_output=False, return_flat=False, file_types=['.*']):
    output_dict = {os.path.basename(input_path): {}}
    flat_output_dict = {}

    for root, dirs, files in os.walk(input_path):
        if not recursive and root != input_path:
            break

        rel_path = os.path.relpath(root, input_path)
        subdirs = rel_path.split(os.sep)
        current_dict = output_dict
        for subdir in subdirs:
            current_dict = current_dict.setdefault(subdir, {})

        folder_message = ""
        folder_output = folder_func(root) if folder_func else None
        if folder_output is not None:
            current_dict["output"] = folder_output[0]
            folder_message = folder_output[1] if len(folder_output) > 1 else ""
            if return_flat:
                flat_output_dict[root] = folder_output[0]

        if print_output:
            depth = root.count(os.sep) - input_path.count(os.sep)
            prefix = "│   " * (depth - 1) + "├── " if depth > 0 else ""
            folder_string = colored(f'{os.path.basename(root)} ({folder_message})')
            print(prefix + folder_string)

        for i, file in enumerate(files):
            file_extension = os.path.splitext(file)[1]
            if any(fnmatch.fnmatch(file_extension, file_type) for file_type in file_types):
                file_message = ""
                file_output = file_func(os.path.join(root, file)) if file_func else None
                if file_output is not None:
                    current_dict[file] = file_output[0]
                    file_message = file_output[1] if len(file_output) > 1 else ""
                    if return_flat:
                        flat_output_dict[os.path.join(root, file)] = file_output[0]

                if print_output:
                    prefix = "│   " * depth + ("└── " if i == len(files) - 1 else "├── ")
                    file_string = colored(f'{file} ({file_message})', 'green')
                    print(prefix + file_string)

    return flat_output_dict if return_flat else output_dict


# test run_on_dir
if __name__ == "__main__":
    input = './root'
    recursive = True
    print_output = True
    def folder_func(folder_path):
        # Perform some operations on the folder
        # Return a list with the output and an optional message
        return ["out " + os.path.basename(folder_path), f'{folder_path} fold message']

    def file_func(file_path):
        # Perform some operations on the file
        # Return a list with the output and an optional message
        return ["out " + os.path.basename(file_path), f'{file_path} file message']

    output_dict = run_on_dir(input, file_func, folder_func, recursive, print_output)
    print(output_dict)

def print_dir(input_path, recursive=False):
    run_on_dir(input_path, print_output=True, recursive=recursive)


# test print_dir
if __name__ == "__main__":
    input = './root'
    recursive = True
    print_dir(input, recursive)

# additional example
if __name__ == "__main__":
    input = './root'
    recursive = True

    def file_func(file_path):
        # Read the file
        with open(file_path, 'r') as f:
            content = f.read()

        # Reverse the content
        reversed_content = content[::-1]

        # Create the mirrored directory structure under ./reversed/root
        new_dir = os.path.join('./reversed', os.path.dirname(file_path))
        os.makedirs(new_dir, exist_ok=True)

        # Write the reversed content to a new file in the mirrored directory
        new_file_path = os.path.join(new_dir, os.path.basename(file_path))
        with open(new_file_path, 'w') as f:
            f.write(reversed_content)

        import time
        time.sleep(0.2)

        # Return the new file path and a message
        return [new_file_path, colored(reversed_content, 'yellow')]

    output_dict = run_on_dir(input, file_func, recursive=recursive, print_output=True)


"""
root (out root)
├── f0 (out f)
├── d0 (out d0)
│   d0_f1 (out d0_f1)
│   ├── d0_f0 (out d0_f0)
│   ├── d0_d1 (out d0_d1)
│   │   └── d0_d1_f0 (out d0_d1_f0)
├── d1 (out d1)
│   ├── d1_d1 (out d1_d1)

output_dict = {
    "root": {
        "output": "out root",
        "f0": f0_out,
        "d0": {
            "output": "out d0",
            "d0_f1": d0_f1_out,
            "d0_f0": d0_f0_out,
            "d0_d1": {
                "output": "out d0_d1",
                "d0_d1_f0": d0_d1_f0_out
            }
        },
        "d1": {
            "output": "out d1",
            "d1_d1": {
                "output": "out d1_d1"
            }
        }
    }
}
"""