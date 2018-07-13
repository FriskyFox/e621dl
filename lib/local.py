# Internal Imports
import configparser
import datetime
import os

# Personal Imports
from lib import constants

def make_config(name='config.ini'):
    with open(name, 'wt', encoding = 'utf_8_sig') as outfile:
        outfile.write(constants.DEFAULT_CONFIG_TEXT)
        if name == 'config.ini':
            print("[i] New default config file created. Please add tag groups to this file.'")
            input("Press ENTER to continue...")
            raise SystemExit

def migrate_config():
    configOld = configparser.ConfigParser()
    configNew = configparser.ConfigParser()
    with open('config.ini', 'rt', encoding = 'utf_8_sig') as oldFile:
        configOld.read_file(oldFile)
    make_config('configMigration.ini')
    with open('configMigration.ini', 'wt', encoding = 'utf_8_sig') as newFile:
        configNew.read_file(newFile)

    #Simple accessor and mutator methods
    for section in config.sections():
        if section.lower() == 'other':
            for option, value in config.items(section):
                if option.lower() == 'include_md5':
                        configNew['Other']['include_md5'] = value
                elif option.lower() == 'organize_by_type':
                        configNew['Other']['organize_by_type'] = value
        elif section.lower() == 'defaults':
            for option, value in config.items(section):
                if option.lower() in {'days_to_check', 'days'}:
                    configNew['Defaults']['days'] = value
                elif option.lower() in {'min_score', 'score'}:
                    configNew['Defaults']['min_score'] = value
                elif option.lower() in {'min_favs', 'favs'}:
                    configNew['Defaults']['min_favs'] = value
                elif option.lower() in {'ratings', 'rating'}:
                    configNew['Defaults']['ratings'] = value
        elif section.lower() == 'blacklist':
            configNew['Blacklist']['tags'] = value
        else:
            configNew[section] = {}
            for option, value in config.items(section):
                configNew[section][option] = value

def get_config():
    config = configparser.ConfigParser()

    if not os.path.isfile('config.ini'):
        print("[!] No config file found.")
        make_config()

    with open('config.ini', 'rt', encoding = 'utf_8_sig') as infile:
        config.read_file(infile)

    return config

def get_date(days_to_check):
    ordinal_check_date = datetime.date.today().toordinal() - (days_to_check - 1)

    if ordinal_check_date < 1:
        ordinal_check_date = 1
    elif ordinal_check_date > datetime.date.today().toordinal():
        ordinal_check_date = datetime.date.today().toordinal()

    return datetime.date.fromordinal(ordinal_check_date).strftime(constants.DATE_FORMAT)

def substitute_illegals(char):
    illegals = ['\\', ':', '*', '?', '\"', '<', '>', '|', ' ']

    return '_' if char in illegals else char

def make_path(dir_name, filename, ext):
    clean_dir_name = ''.join([substitute_illegals(char) for char in dir_name]).lower()

    if not os.path.isdir(f"downloads/{clean_dir_name}"):
        os.makedirs(f"downloads/{clean_dir_name}")

    return f"downloads/{clean_dir_name}/{filename}.{ext}"
