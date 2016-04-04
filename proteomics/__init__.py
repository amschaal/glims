import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
GENERATE_TANDEM_QSUB = os.path.join(BASE_DIR,'proteomics','scripts','generate_tandem_inputs.py')
SLEEPER_SCRIPT = os.path.join(BASE_DIR,'proteomics','scripts','sleeper.sh')
CRAP_FILE = os.path.join(BASE_DIR,'proteomics/static/proteomics/crap.fasta')

TANDEM_SCRIPT = os.path.join(BASE_DIR,'proteomics/scripts/tandem.py')
SCAFFOLD_SCRIPT = os.path.join(BASE_DIR,'proteomics/scripts/scaffold.py')

LOCAL_JOB_DIRECTORY = '/tmp'#'/saraswati/home/adam/jobs'
JOB_DIRECTORY = '/home/adam/jobs'
