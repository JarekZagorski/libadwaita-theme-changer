#!/bin/python3

############################################
#
# Libadwaita Theme Changer
# created by OdzioM
#
############################################

import sys
import os
import subprocess as sp

import argparse as ap


parser = ap.ArgumentParser(
                    prog='Libadwaita theme changer',
                    description='Changes gtk-4 theme')

parser.add_argument(
    '--theme',
    help='Takes name of the theme you want to set',
    required=False,
)
parser.add_argument(
    '--reset',
    help='Resets theme',
    required=False,
    action='store_true'
)
parser.add_argument(
    '--gsettings',
    help='Gets theme name from gsettings',
    required=False,
    action='store_true'
)
args = parser.parse_args()

# gsettings get org.gnome.desktop.interface gtk-theme

def remove_old_theme(config_dir: str):
    sp.run(["rm", f'{config_dir}/gtk-4.0/gtk.css'])
    sp.run(["rm", f'{config_dir}/gtk-4.0/gtk-dark.css'])
    sp.run(["rm", f'{config_dir}/gtk-4.0/assets'])
    sp.run(["rm", f'{config_dir}/assets'])

def set_theme(config_dir: str, theme_dir: str):
    sp.run(["ln", "-s", f'{theme_dir}/gtk-4.0/gtk.css', f'{config_dir}/gtk-4.0/gtk.css'])
    sp.run(["ln", "-s", f'{theme_dir}/gtk-4.0/gtk-dark.css', f'{config_dir}/gtk-4.0/gtk-dark.css'])
    sp.run(["ln", "-s", f'{theme_dir}/gtk-4.0/assets', f'{config_dir}/gtk-4.0/assets'])
    sp.run(["ln", "-s", f'{theme_dir}/assets', f'{config_dir}/assets'])

if __name__ == "__main__":
    # my try
    home_dir = os.getenv('HOME')
    configs = f'{home_dir}/.config'
    themes = f'{home_dir}/.themes'
    try:
        if args.reset:
            print(f'\n***\nResetting theme to default!\n***\n')
            remove_old_theme(configs)
        elif args.gsettings:
            name = (sp.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], stdout=sp.PIPE)
                .stdout.decode()
                .replace("'", "")
                .removesuffix('\n')
            )
            theme_dir =f'{themes}/{name}'
            print(theme_dir)
            remove_old_theme(configs)
            set_theme(configs, theme_dir)
        elif args.theme:
            theme_dir =f'{themes}/{args.theme}'
            remove_old_theme(configs)
            set_theme(configs, theme_dir)
        else:
            all_themes = str(sp.run(["ls", f'{themes}/'], stdout=sp.PIPE).stdout.decode("UTF-8")).split()
            print("Select theme: ")
            for i, theme in enumerate(all_themes):
                print(f'{i+1}. {theme}')
            print("e. Exit")
            choice = input("Your choice: ")
            if choice == 'e':
                sys.exit()
            else:
                remove_old_theme(configs)
                set_theme(configs, f'{themes}/{all_themes[int(choice)]}')
    except ValueError as e:
        print("Incorrect value! Please try again!")
