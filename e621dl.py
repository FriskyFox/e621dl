#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
TODO:
+ Add Updated Config Parsing without conditionals and allow for auto migration of configuration file (With User choice of Y/N)
+ Add debug option to config other as an invisible modifier
'''
debug = True #Enabling of Debug provides more in-depth 'per file' Parsing - Temporary option

# Internal Imports
import os
from fnmatch import fnmatch
from distutils.version import StrictVersion

# Personal Imports
from lib import constants
from lib import local
from lib import remote

# This block will only be read if e621dl.py is directly executed by python. Not if it is imported.
if __name__ == '__main__':

    # Create the requests session that will be used throughout the run and set the user-agent.
    # The user-agent requirements are specified at (https://e621.net/help/show/api#basics).
    with remote.requests_retry_session() as session:
        session.headers['User-Agent'] = constants.USER_AGENT

        # Check if a new version is released on github. If so, notify the user.
        if StrictVersion(constants.VERSION) < StrictVersion(remote.get_github_release(session)):
            print('A NEW VERSION OF e621dl IS AVAILABLE ON GITHUB AT https://github.com/FriskyFox/e621dl/releases.')
            if debug: print(f"[i] The current release version is {remote.get_github_release(session)}, while current version running is {constants.VERSION}")
        print(f"[i] Running e621dl version {constants.VERSION}.\n[i] Checking for partial downloads...")

        remote.finish_partial_downloads(session)

        print("\n[i] Parsing config...")
        config = local.get_config()

        # Initialize the lists that will be used to filter posts.
        blacklist = []
        searches = []

        # Initialize user configured options in case any are missing.
        include_md5 = False # The md5 checksum is not appended to file names.
        default_date = local.get_date(1) # Get posts from one day before execution.
        default_score = -0x7F_FF_FF_FF # Allow posts of any score to be downloaded.
        default_favs = 0
        default_ratings = ['s'] # Allow only safe posts to be downloaded.
        organize_file = False #Allows for organization of files by type (images/video/swf)

        # Iterate through all sections (lines enclosed in brackets: []).
        for section in config.sections():

            # Get values from the "Other" section.
            if section.lower() == 'other':
                try:
                    for option, value in config.items(section):
                        if option.lower() == 'include_md5' and value.lower() == 'true':
                                include_md5 = True
                        elif option.lower() == 'organize_by_type' and value.lower() == 'true':
                            print("[!] Organizing Files by Type")
                            organize_file = True
                        elif option.lower() == 'version' and value.lower() == local.VERSION:
                                pass
                except KeyError:
                    #Not Set Up Yet!!!
                    print(f'[!] It Appears that you have an old version\'s config file. Now attempting to migrate config to the latest version...')
                    local.migrate_config()

            # Get values from the "Defaults" section. This overwrites the initialized default_* variables.
            elif section.lower() == 'defaults':
                for option, value in config.items(section):
                    if option.lower() in {'days_to_check', 'days'}:
                        default_date = local.get_date(int(value))
                    elif option.lower() in {'min_score', 'score'}:
                        default_score = int(value)
                    elif option.lower() in {'min_favs', 'favs'}:
                        default_favs = int(value)
                    elif option.lower() in {'ratings', 'rating'}:
                        default_ratings = value.replace(',', ' ').lower().strip().split()

            # Get values from the "Blacklist" section. Tags are aliased to their acknowledged names.
            elif section.lower() == 'blacklist':
                blacklist = [remote.get_tag_alias(tag.lower(), session) for tag in config.get(section, 'tags').replace(',', ' ').lower().strip().split()]

            # If the section name is not one of the above, it is assumed to be the values for a search.
            else:

                # Initialize the list of tags that will be searched.
                section_tags = []

                # Default options are set in case the user did not declare any for the specific section.
                section_date = default_date
                section_score = default_score
                section_favs = default_favs
                section_ratings = default_ratings

                # Go through each option within the section to find search related values.
                for option, value in config.items(section):

                    # Get the tags that will be searched for. Tags are aliased to their acknowledged names.
                    if option.lower() in {'tags', 'tag'}:
                        section_tags = [remote.get_tag_alias(tag.lower(), session) for tag in value.replace(',', ' ').lower().strip().split()]

                    # Overwrite default options if the user has a specific value for the section
                    elif option.lower() in {'days_to_check', 'days'}:
                        section_date = local.get_date(int(value))
                    elif option.lower() in {'min_score', 'score'}:
                        section_score = int(value)
                    elif option.lower() in {'min_favs', 'favs'}:
                        section_favs = int(value)
                    elif option.lower() in {'ratings', 'rating'}:
                        section_ratings = value.replace(',', ' ').lower().strip().split()

                # Append the final values that will be used for the specific section to the list of searches.
                # Note section_tags is a list within a list.
                searches.append({'directory': section, 'tags': section_tags, 'ratings': section_ratings, 'min_score': section_score, 'min_favs': section_favs, 'earliest_date': section_date})

        for search in searches:
            print('')

            # Creates the string to be sent to the API.
            # Currently only 5 items can be sent directly so the rest are discarded to be filtered out later.
            if len(search['tags']) > 5:
                search_string = ' '.join(search['tags'][:5])
            else:
                search_string = ' '.join(search['tags'])

            # Initializes last_id (the last post found in a search) to an enormous number so that the newest post will be found.
            # This number is hard-coded because on 64-bit archs, sys.maxsize() will return a number too big for e621 to use.
            last_id = 0x7F_FF_FF_FF

            #Values to be reported back to the User
            total_files = 0
            downloaded = 0
            skipped = 0
            total_queries = 0

            #In order: already have, missing rating, blacklisted, missing tag, low score, low fav
            skipped_details = [0,0,0,0,0,0]
            # Sets up a loop that will continue indefinitely until the last post of a search has been found.
            while True:
                total_queries += 1 #Debug stuff
                print("[i] Getting posts...\n")
                if debug: print("Post Acquirement #{total_queries}")
                results = remote.get_posts(search_string, search['earliest_date'], last_id, session)

                # Gets the id of the last post found in the search so that the search can continue.
                # If the number of results is less than the max, the next searches will always return 0 results.
                # Because of this, the last id is set to 0 which is the base case for exiting the while loop.
                if len(results) < constants.MAX_RESULTS:
                    last_id = 0
                else:
                    last_id = results[-1]['id']

                for post in results:
                    #Orders posts as dictated by type
                    if organize_file:
                        if post['file_ext'] in ['png','jpg']:
                            fileDirectory = search['directory']+'/images'
                        elif post['file_ext'] == 'gif':
                            fileDirectory = search['directory']+'/gifs'
                        elif post['file_ext'] == 'webm':
                            fileDirectory = search['directory']+'/videos'
                        elif post['file_ext'] == 'swf':
                            fileDirectory = search['directory']+'/swfs'
                        else:
                            print(f"[!] Could not determine the file type of Post {post['id']}. The type was listed as {post['file_ext']}")
                    else:
                        fileDirectory = directory

                    if include_md5:
                        path = local.make_path(fileDirectory, f"{post['id']}.{post['md5']}", post['file_ext'])
                    else:
                        path = local.make_path(fileDirectory, post['id'], post['file_ext'])

                    if os.path.isfile(path):
                        if debug: print(f"[✗] Post {post['id']} was already downloaded.")
                        skipped += 1 #Increment Skipped Files
                        skipped_details[0] += 1
                    elif post['rating'] not in search['ratings']:
                        if debug: print(f"[✗] Post {post['id']} was skipped for missing a requested rating.")
                        skipped += 1 #Increment Skipped Files
                        skipped_details[1] += 1
                    # Using fnmatch allows for wildcards to be properly filtered.
                    elif [x for x in post['tags'].split() if any(fnmatch(x, y) for y in blacklist)]:
                        if debug: print(f"[✗] Post {post['id']} was skipped for having a blacklisted tag.")
                        skipped += 1 #Increment Skipped Files
                        skipped_details[2] += 1
                    elif not set(search['tags'][4:]).issubset(post['tags'].split()):
                        if debug: print(f"[✗] Post {post['id']} was skipped for missing a requested tag.")
                        skipped += 1 #Increment Skipped Files
                        skipped_details[3] += 1
                    elif int(post['score']) < search['min_score']:
                        if debug: print(f"[✗] Post {post['id']} was skipped for having a low score.")
                        skipped += 1 #Increment Skipped Files
                        skipped_details[4] += 1
                    elif int(post['fav_count']) < search['min_favs']:
                        if debug: print(f"[✗] Post {post['id']} was skipped for having a low favorite count.")
                        skipped += 1 #Increment Skipped Files
                        skipped_details[5] += 1
                    else:
                        if debug: print(f"[✓] Post {post['id']} was downloaded.")
                        remote.download_post(post['file_url'], path, session)
                        downloaded += 1 #Increment total downloaded
                    if debug and total_files % 10 == 0 and total_files != 0: #More debug
                        print(f"{total_files} Posts Parsed... ({downloaded} Downloaded). Please wait for completion...")
                    total_files += 1 #Increment Total Files

                # Break while loop. End program.
                if last_id == 0:
                    break
            print(f"\nFor Search {directory} a total of [add session files] were parsed with [add session downloads] files downloaded. ([add percentage of downloads to parsing])")
        print(f"\nA Total of {total_files} files were parsed with {downloaded} downloads and {skipped} files skipped.")
        print(f"Skipped file details:\n{skipped_details[0]} Already Downloaded, {skipped_details[1]} Incorrect Rating, {skipped_details[2]} Blacklisted, {skipped_details[3]} Missing Requested Tags, {skipped_details[4]} Score lower than threshhold, and {skipped_details[5]} Favorite count lower than threshhold.")
    # End program.
    input("\n[✓] All searches complete. Press ENTER to exit...")
    #raise SystemExit
