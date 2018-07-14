# What is **e621dl**?

**e621dl** is an automated script, originally by [**@wwyaiykycnf**](https://github.com/wwyaiykycnf), which downloads images from e621.net. It can be used to create a local mirror of your favorite searches, and keep these searches up to date as new posts are uploaded.


# How does **e621dl** work?

Put very simply, when **e621dl** starts, it determines the following based on the `config.ini` file:

- Which tags you would like to avoid seeing by reading the blacklist section.
- Which searches you would like to perform by reading your search group sections.

Once it knows these things, it goes through the searches one by one, and downloads _only_ content that matches your search request, and has passed through all specified filters.

# Installing and Setting Up **e621dl**

- Download [the latest executable release of **e621dl**](https://github.com/FriskyFox/e621dl/releases).

*or*

- Download and install [the latest release of Python 3](https://www.python.org/downloads/).
- Download [the latest *source* release of **e621dl**](https://github.com/FriskyFox/e621dl/releases).
    - Decompress the archive into any directory you would like.

# Running **e621dl**
## Running **e621dl** from the Windows executable.

- Double click the e621dl.exe icon to run the program.
    - If you would like to read the output after the execution is complete, alternatively run the program through the command prompt in the directory that you placed the .exe file.
    ```
    C:[Directory of Executable]> e621dl.exe
    ```

## Running **e621dl** from source.

You must install all of this program's python dependencies for it to run properly from source. They can be installed by running the following command in your command shell: `pip install [package name]`.
*You must run your command shell with admin/sudo permissions for the installation of new packages to be successful.*

**NOTE**: If neither python, py, pip etc. work and you are on Windows, ensure that python is registered as a PATHENV variable. A guide to do this is at the end of the readme if required

The required packages for **e621dl** are currently:
- [requests](https://python-requests.org) `pip install requests`

Open your command shell in the directory you decompressed e621dl into, and run the command `py e621dl.py`. Depending on your system, the command `py` may default to Python 2. In this case you should run `py -3 e621dl.py`. Sometimes, your system may not recognize the `py` command at all. In this case you should run `python3 e621dl.py`. In some cases where Python 3 was the first installed version of Python, the command `python e621dl.py` will be used.
    - The most common error that occurs when running a Python 3 program in Python 2 is `SyntaxError: Missing parentheses in call to 'print'`.

## First Run

The first time you run **e621dl**, you will see the following errors:

```
[i] Running e621dl version X.X.X.
[i] Checking for partial downloads...
[i] New default config file created. Please add tag groups to this file.
Press ENTER to exit...
```

**e621dl** on first run creates a configuration file for you to edit. Please open this file in your preferred text editor.

## Add search groups to the config file.

Create sections in the `config.ini` to specify which posts you would like to download. In the default config file, an example is provided for you. This example is replicated below. Each section will have its own directory inside the downloads folder.

```
;;;;;;;;;;;;;;;;;;;
;; SEARCH GROUPS ;;
;;;;;;;;;;;;;;;;;;;

; New search groups can be created by writing the following. (Do not include semicolons.):
; [Directory Name]
; days = 1
; ratings = s, q, e
; min_score = -100
; tags = tag1, tag2, tag3, ...

; Example:
; [Cute Cats]
; days = 30
; ratings = s
; min_score = 5
; tags = cat, cute
```

The following characters are not allowed in search group names: `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`, and ` ` as they can cause issues in windows file directories. If any of these characters are used, they will be replaced with the `_` character. The `/` character *is* allowed to be used in section names, but **it will be understood as a sub-directory**. This may be useful to some users for organization. For example: separating `[Canine/Fox]` and `[Canine/Wolf]`, and separating `[Feline/Tiger]` and `[Feline/Lion]`

Commas should be used to separate tags and ratings, but this is not strictly enforced in current versions of **e621dl**. But *please ensure there is separation via spaces if there are no commas otherwise tags will be ignored*.

One side effect of the workaround used to search an unlimited number tags is that you may only use up to 4 meta tags `:`, negative tags `-`, operational tags `~`, or wildcard tags `*` per group, and they must be the **first 4 items in the group**. See [the e621 cheatsheet](https://e621.net/help/show/cheatsheet) for more information on these special types of tags.

### Search Group Keys, Values, and Descriptions

Key                   | Acceptable Values               | Description
--------------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------
[]                    | Nearly Anything                 | The search group name which will be used to title console output and name folders. See above for restrictions.
days                  | Integer from `1` to ∞           | How many days into the past to check for new posts.
ratings               | Characters `s`, `q`, and/or `e` | Acceptable explicitness ratings for downloaded posts. Characters stand for safe, questionable, and explicit, respectively.
min_score             | Integer from -∞ to ∞            | Lowest acceptable score for downloaded posts. Posts with higher scores than this number will also be downloaded.
min_favs | Integer from -∞ to ∞ | Lowest acceptable favorite count for downloaded posts. Anything above this is also downloaded.
tags                  | Nearly Anything                 | Tags which will be used to perform the post search. See above for restrictions

## [Optional] Add blacklisted tags to the config file.

Add any tags for posts you would like to avoid downloading to the blacklist section of the `config.ini` file. Meta tags `:`, negative tags `-`, operational tags `~`, will potentially break the script, as they are currently not filtered out of the blacklist, so do not use them in this section. Wildcard tags `*` *are* supported in the blacklist, though it is easy for a misspelled wildcard to match an artist's name, for example, and the program will not give any errors.

## [Optional] Modify the defaults in the config file.

The defaults section of the `config.ini` is the primary fallback for any missing lines in a search group. This section uses the same keys as search groups.

There is also a hard-coded secondary fallback if any lines are missing in the defaults section. They are as follows:

```
days = 1
ratings = s
score = -INFINITY
```

## Normal Operation

Once you have added at least one group to the tags file, you should see something similar to this when you run **e621dl**:

```
[i] Running e621dl version 4.5.2.
[i] Checking for partial downloads...
[✓] No partial downloads found

[i] Parsing user config...
[i] Checking user blacklist...
[✓] All blacklist tags have been checked (NUM/NUM)

[i] Checking tags on 'SECTION'...
[✓] All tags for SECTION have been checked (NUM/NUM)

[i] Getting posts...

[i] Beggining search 'SECTION'
[i] Downloads are still in progress... so far X files have been parsed
[✓] For search 'SECTION' a total of X files were parsed with X files downloaded. (X% Downloaded)

[i] Grand Totals of run-time:
+ A Total of X files were parsed
+ X files were downloaded
+ X files were skipped.

[i] Skipped file details:
+ X files were already downloaded
+ X files had an incorrect rating
+ X files were blacklisted
+ X files were missing requested tags
+ X files had a score lower than the threshhold
+ X files had a favorite count lower than the threshhold
```

The runtime of e621dl is very self-explanatory, explaining each step as it continues and it even includes extra verbose logging for longer group checks `days = 2556`,`min_score = 0`,`tags = canine`.

Yeah... this above one should net you [depending on ratings allowed] **literally all of e621** because unsuprisingly almost all furries are canines

It should be recognized that **e621dl**, as a script, can be scheduled to run as often as you like, keeping the your local collections always up-to-date, however, the methods for doing this are dependent on your platform, and are outside the scope of this quick-guide. Good luck though and happy parsing!

## Fixing Broken Python via CMD [Windows Only]
So, sometimes Python installs, but doesn't install its system environment PATH variable.


If that's your problem, this is your fix.

**NOTE: I am unsure but I think this requires Administrator privileges (I'm always Administrator anywhere I go so sorry if you can't do it)**

IF you want to be able to access python anywhere from console, (**and you're on windows 10**), type into the search bar
`system environment variables` OTHERWISE (**Windows 7**) navigate to `System Properties` (I believe you can right click in file explorer while not being in any system drive and on the `This PC` section and select `Properties` to navigate quickly to this section)

A window will open with the title being System Properties. Select `Environment Variables...` at the bottom. If you would like anyone on the computer to be able to access it: Select `Path` -> `Edit...` under `System Variables` section. Click `New` and then add the absolute path to your python installation. (For example, my path is `C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64) This now allows you to type python in console (**PROVIDED It is named python.exe at your directory, check the name of the python executable environment**).

If you would like this to be only on your user account do all of the above under `User variables for <USER ACCOUNT>`

# Feedback and Requests

If you have any ideas on how to make this script run better, or for features you would like to see in the future, [open an issue](https://github.com/friskyfox/e621dl/issues) and I will try to read it as soon as possible.
