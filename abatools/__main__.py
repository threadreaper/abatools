#!/usr/bin/env python
"""
zipanimation
Simple command line utility for making Android-compliant
bootanimation.zip archives
(c) 2020 Michael Podrybau
threadreaper@gmail.com
https://github.com/threadreaper/zipanimation
"""

import sys
import os
import zipfile
import argparse
import shutil
from pathlib import Path
from PIL import Image


def get_args():
    """Get command line arguments"""
    description = "Utility to create sorted zip files for Android boot" \
                  "animations"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("-a", metavar="[filename.zip]",
                     help="zip all files/folders in current directory to"
                          "target [filename.zip]")
    arg.add_argument("-g", metavar="[gif file] [filename]", nargs='*',
                     help="creates a boot animation from target .gif "
                          "and saves it to [filename.zip]")

    return arg


def parse_args_exit(parser):
    """Process arguments and exit."""
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.a:
        if args.a[-4:] != '.zip':
            fail("Output target must be a .zip file.  (Did you forget the"
                 " extension?)")
        if permission(args.a) != 1:
            sys.exit(1)
        if not Path('desc.txt').is_file():
            fail("Error: desc.txt must be present to create a boot "
                 "animation.")
        dirs = [x for x in sorted(os.listdir()) if not Path(x).is_file()]
        if not dirs:
            fail("Error: no directories found to add to the archive.")
        add2zip('desc.txt', args.a)
        for this_dir in dirs:
            add2zip(this_dir, args.a)
        print("Boot animation generated successfully!")
        sys.exit(0)

    if args.g:
        if len(args.g) != 2:
            fail("-g option requires two arguments.")
        try:
            gif = Image.open(args.g[0])
        except FileNotFoundError:
            fail("Invalid path to .gif file")
        finally:
            if gif.n_frames < 2:
                fail("Target does not appear to be an animated .gif.")
        if args.g[1][-4:] != '.zip':
            fail("Output target must be a .zip file.  (Did you forget the"
                 " extension?)")
        if permission(args.g[1]) != 1:
            sys.exit(1)
        try:
            os.mkdir('part0')
        except FileExistsError:
            if permission('part0'):
                os.mkdir('part0')
        finally:
            for i, frame in enumerate(iter_frames(gif)):
                frame.save("part0/" + f"{i:02d}.png")
        width, height, fps = get_specs()
        img_width, img_height = gif.size

        if img_width != width or img_height != height:
            print("Image size and target resolution differ. \n"
                  "Would you prefer to:\n"
                  "[s]tretch, [f]it, or [c]enter your image?")
            answer = get_valid_input('s', 'f', 'c')
            resize_images(answer, width, height, img_width, img_height)

        with open('desc.txt', 'w') as file:
            lines = list('%s %s %s\n' % (str(width), str(height),
                                         str(fps)))
            lines.append('p 0 0 part0\n')
            file.writelines(lines)
        add2zip('desc.txt', args.g[1])
        add2zip('part0', args.g[1])
        print('Boot animation successfully produced!')
        sys.exit(0)


def resize_images(method, width, height, img_width, img_height):
    """resizes animation frames based on user selected settings"""
    if method.lower() == 's':
        for i, frame in enumerate(sorted(os.listdir('part0'))):
            img = Image.open('part0/' + frame)
            newframe = img.resize((width, height), Image.BILINEAR)
            newframe.save("part0/" + f"{i:02d}.png")
    if method.lower() == 'f':
        for i, frame in enumerate(sorted(os.listdir('part0'))):
            img = Image.open('part0/' + frame)
            wpercent = (height / float(img_height))
            width = int(img_width * float(wpercent))
            newframe = img.resize((width, height), Image.BILINEAR)
            newframe.save("part0/" + f"{i:02d}.png")
    if method.lower() == 'c':
        return 0


def get_valid_input(*args):
    """given a list of args as input, refuses to return until
    user input matches something in the list"""
    answer = input()
    if answer in args:
        return answer
    while True:
        for arg in args:
            if answer.lower() == arg.lower():
                return answer
            print("Choose from: ", end='')
            print(args)
            answer = input()


def get_specs():
    """Acquire user settings from stdin"""
    width = input_number("Enter target device resolution width: ")
    height = input_number("Enter target device resolution height: ")
    fps = input_number("Enter target frame rate: ")
    while True:
        if width < 320 or width > 3840:
            print("Value for width is outside acceptable range.")
            width = input_number("Enter target device resolution width: ")
        elif height < 360 or height > 2560:
            print("Value for height is outside acceptable range.")
            height = input_number("Enter target device resolution height: ")
        elif fps > 60:
            print("Frame rates greater than 60fps not recommended.")
            fps = input_number("Enter target frame rate: ")
        else:
            return width, height, fps


def input_number(message):
    """forces user input to an integer number"""
    while True:
        try:
            value = int(input(message))
        except ValueError:
            print("Value must be an integer.")
            continue
        else:
            return value


def iter_frames(img):
    """iterator function for extracted frames"""
    try:
        i = 0
        while 1:
            img.seek(i)
            frame = img.copy()
            if i == 0:
                palette = frame.getpalette()
            else:
                frame.putpalette(palette)
            yield frame
            i += 1
    except EOFError:
        pass


def fail(emsg):
    """Print an error message and exit with an error"""
    print(emsg)
    sys.exit(1)


def permission(file):
    """ask permission before overwriting existing zip file"""
    while Path(file).exists():
        answer = input("%s exists and will be OVERWRITTEN.  Proceed?"
                       " (y/n)" % file)
        if answer.lower() == 'n':
            fail("Please rename/relocate %s or choose a different"
                 "filename." % file)
        elif answer.lower() == 'y':
            try:
                os.remove(file)
            except IsADirectoryError:
                shutil.rmtree(file)
        else:
            print("Sorry, I didn't get that.")
    return 1


def add2zip(target, zfile):
    """append target to the the named zip file, if target is a
    directory, also sort and append the contents"""
    zipf = zipfile.ZipFile("%s" % zfile, mode='a',
                           compression=zipfile.ZIP_STORED)
    zipf.write(target)
    if not Path(target).is_file():
        contents = os.listdir(target)
        for frame in sorted(contents):
            add2zip("%s/%s" % (target, frame), zfile)
    zipf.close()


def main():
    """come on, pylint this is the main function..."""
    parser = get_args()
    parse_args_exit(parser)


if __name__ == "__main__":
    main()
