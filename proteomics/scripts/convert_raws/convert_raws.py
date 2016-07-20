#REQUIRES Poster library for posting files: https://atlee.ca/software/poster/
from poster import encode, streaminghttp

import argparse, glob, os
import json
import urllib2, urllib
import shutil
import subprocess
RAW_DIRECTORY = '/data/raws'
PROCESSED_DIRECTORY = '/data/raws/processed'
BASE_URL = 'http://localhost:8001'
SAMPLES_API_URL = BASE_URL+'/api/samples/'
SAMPLE_API_URL = SAMPLES_API_URL+'%s/'
UPLOAD_SAMPLE_FILE_URL = SAMPLE_API_URL + 'upload_file/'
RAW_FILE_REGEX = r''
AUTHENTICATION_TOKEN = '1753e52b5b4a6835e8fdfe9f42cf74252a4d1f25' #test token, replace with real token

def parse_sample_id(filename):
    # @todo: Make this more robust
    return filename.split('_')[0]

def get_sample(sample_id,options):
    response = urllib2.urlopen(urllib2.Request(SAMPLE_API_URL%sample_id,headers={'Authorization': 'Token %s'%options.auth_token}))
    data = json.loads(response.read())
#     except urllib2.HTTPError as e:
#         error_message = e.read()
#         print error_message
    return data

def post_sample_file(sample_id,file_path,subdir,options):
    try:
        opener = streaminghttp.register_openers()
        params = {'file': open(file_path,'rb'), 'subdir': subdir,'overwrite':True}
        datagen, headers = encode.multipart_encode(params)
        headers['Authorization'] = 'Token %s'%options.auth_token
        response = opener.open(urllib2.Request(UPLOAD_SAMPLE_FILE_URL%sample_id, datagen, headers))
        data = json.loads(response.read())
        return data
    except Exception as e:
        print e.read()

def raw_to_mzml(raw_path,test=False):
#     @todo: Run msconvert to actually convert raw->mzml.  This is for testing.
    mzml_path = os.path.splitext(raw_path)[0] + '.mzML'
    if os.path.exists(mzml_path):
        return mzml_path
    if test:
        shutil.copyfile(raw_path, mzml_path)
    else:
        subprocess.check_output(['msconvert',raw_path])
    return mzml_path

def move_files(files,directory):
    for file in files:
        shutil.move(file, file + '.moving') #in case move fails, change extension so we don't attempt to 
        shutil.move(file + '.moving',os.path.join(directory,os.path.basename(file)))
        

def convert_files(options):
    raws = glob.glob1(options.directory, '*.raw')
    for raw in raws:
        sample_id = parse_sample_id(raw)
        print get_sample(sample_id,options)
        raw_path = os.path.join(options.directory,raw)
        mzml_path = raw_to_mzml(raw_path,test=options.test)
        print post_sample_file(sample_id, mzml_path, 'mzmls', options)
        move_files([raw_path,mzml_path],options.processed_directory)

def main():
    parser = argparse.ArgumentParser(description='Convert raw files to MZML format and upload to GLIMS')
#     parser.add_argument('--mzml', required=True, nargs='+', help='An mzML file path.  May use wildcards to use multiple files, such as *.mzml')
    parser.add_argument('--directory', required=False, default=RAW_DIRECTORY, help='The directory containing the raw files.')
    parser.add_argument('--processed_directory', required=False, default=PROCESSED_DIRECTORY, help='Where to put the raw files after conversion.')
    parser.add_argument('--auth_token', required=False, default=AUTHENTICATION_TOKEN, help='Authentication token for connecting to REST services.')
    parser.add_argument('--test', required=False, default=False, help='Authentication token for connecting to REST services.')
    options = parser.parse_args()
    convert_files(options)


if __name__ == '__main__':
    main()
