VERSION = '4.5.2'
VERSION_NOTE = 'Forked from 2.4.6'

LOGGER_FORMAT = '%(name)-11s %(levelname)-8s %(message)s'
DATE_FORMAT = '%Y-%m-%d'

USER_AGENT = 'e621dl (Wulfre) -- Version ' + VERSION
MAX_RESULTS = 320
PARTIAL_DOWNLOAD_EXT = 'request'

DEFAULT_CONFIG_TEXT = f''';;;;;;;;;;;;;;
;; GENERAL  ;;
;;;;;;;;;;;;;;

[Defaults]
days = 1
ratings = s
min_score = 0
min_favs = 0

[Blacklist]
tags =

[Other]
;Includes md5 checksum in the filename for files that are downloaded
include_md5 = false

;Organizes files by their extension type (images/videos/swfs/gifs)
organize_by_type = false

;Do Not Edit Version Number Unless You Know What You Are Doing
version = {VERSION}

;;;;;;;;;;;;;;;;;;;
;; SEARCH GROUPS ;;
;;;;;;;;;;;;;;;;;;;

; New search groups can be created by writing the following. (Do not include semicolons.):
; [Directory Name]
; days = 1
; ratings = s, q, e
; min_score = -100
; min_favs = 0
; tags = tag1, tag2, tag3, ...

; Example:
; [Cute Cats]
; days = 30
; ratings = s
; min_score = 5
; min_favs = 20
; tags = cat, cute'''
