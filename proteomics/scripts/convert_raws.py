import argparse, glob
import json
import urllib2, urllib
RAW_DIRECTORY = '/data/raws'
PROCESSED_DIRECTORY = '/data/raws/processed'
SAMPLES_API_URL = 'http://localhost:8001/api/samples/'
SAMPLE_API_URL = SAMPLES_API_URL+'%s/'
UPLOAD_SAMPLE_FILE_URL = SAMPLE_API_URL + 'upload_file/'
RAW_FILE_REGEX = r''
AUTHENTICATION_TOKEN = '1753e52b5b4a6835e8fdfe9f42cf74252a4d1f25' #test token, replace with real token

def parse_sample_id(filename):
    # @todo: Make this more robust
    return filename.split('_')[0]

def get_sample(sample_id):
#     params = urllib.urlencode({'sample_id': sample_id})
    response = urllib2.urlopen(urllib2.Request(SAMPLE_API_URL%sample_id,headers={'Authorization': 'Token %s'%AUTHENTICATION_TOKEN}))
    data = json.loads(response.read())
#     except urllib2.HTTPError as e:
#         error_message = e.read()
#         print error_message
    return data

def convert_files(options):
    raws = glob.glob1(options.directory, '*.raw')
    for raw in raws:
        sample_id = parse_sample_id(raw)
        print get_sample(sample_id)
        
def main():
    parser = argparse.ArgumentParser(description='Convert raw files to MZML format and upload to GLIMS')
#     parser.add_argument('--mzml', required=True, nargs='+', help='An mzML file path.  May use wildcards to use multiple files, such as *.mzml')
    parser.add_argument('--directory', required=False, default=RAW_DIRECTORY, help='The directory containing the raw files.')
    parser.add_argument('--processed_directory', required=False, default=PROCESSED_DIRECTORY, help='Where to put the raw files after conversion.')
    options = parser.parse_args()
    convert_files(options)
    


if __name__ == '__main__':
    main()
