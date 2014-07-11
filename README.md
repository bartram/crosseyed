CrossEyed
=========

CrossEyed combines duplicate video clips when syncing and exporting XML from PluralEyes to Final Cut Pro X with multiple audio tracks.

Requirements
----------

CrossEyed is a command-line Python script. You must have Python installed. Most versions of Mac OS X include Python by default.

How To Use
----------

Create a project in PluralEyes 3 with more than one Audio Recorder bin. Synchronize your media, and then export the timeline, selecting "Create an Event with audio content replaced in video clips" from the Final Cut Pro X options. Then run the crosseyed.py script, passing the name of the `.fcpxml` file with the suffix "_replaced" as the first argument. For example:

    python crosseyed.py "~/Desktop/Moonshine_FCPX_replaced.fcpxml"

CrossEyed will combine the duplicate video clips into single clips with multiple audio tracks on the timeline. It will also add a custom metadata value to the clip, "Date Created," based on the time the video file was created in camera.

Contact
-------

For bug fixes and feature requests, please [submit an issue at GitHub](https://github.com/bartram/crosseyed/issues). CrossEyed was created by [Bartram Nason](http://www.bartramnason.com/).