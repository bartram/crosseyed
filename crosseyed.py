import xml.etree.ElementTree as ElementTree
import sys, getopt, os.path, time, urlparse, urllib, datetime, re

# Check that a file argument was supplied
if len(sys.argv) < 2:
  print 'No input file specified'
  sys.exit(2)

filename = sys.argv[1]

# Check that the file exists
if not os.path.isfile(filename):
  print 'Invalid file name'
  sys.exit(2)

# Check that this is a FCP XML file
if not filename.endswith('.fcpxml'):
  print 'Invalid file extension'
  sys.exit(2)

# Parse the file
try:
  tree = ElementTree.parse(filename)
except ElementTree.ParseError:
  print 'Unable to parse file'
  sys.exit(2)

project = tree.find('project')

# Check that a project exists
if project is None:
  print 'Incorrect XML format'
  sys.exit(2)

# Remove "replaced" from project name
if project.attrib['name']:
  project.attrib['name'] = re.sub(r'\sreplaced$', '', project.attrib['name'])

clips = {}

# Loop through the clips
for clip in project.findall('clip'):

  name = clip.attrib['name']

  if not name in clips:

    # Get the video file
    ref = clip.find('.//video').attrib['ref']
    src = project.find('.//asset[@id="' + ref + '"]').attrib['src']

    path = urlparse.urlparse(src).path
    path = urllib.unquote(path)

    stat = os.stat(path)
    date = datetime.datetime.fromtimestamp(stat.st_birthtime)

    metadata = clip.find('./metadata')
    if metadata is None:
      metadata = ElementTree.SubElement(clip, 'metadata')

    if metadata.find('./md[@key="com.apple.proapps.custom.dateCreated"]') is None:
      # @todo include the timezone offset
      md = ElementTree.SubElement(metadata, 'md', {
        'key': 'com.apple.proapps.custom.dateCreated',
         'value': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'date',
        'editable': '0',
        'displayName': 'Date Created',
        'source': 'CrossEyed'
      })

    # Add this clip to the dictionary
    clips[name] = clip

  else:
    # Move the audio clips to the existing clip, and remove this clip
    existingClip = clips[name]
    videoClip = existingClip.find('.//video/..')
    audioClips = clip.findall('.//audio/..')

    for audioClip in audioClips:
      videoClip.append(audioClip)

    project.remove(clip)

tree.write(filename)