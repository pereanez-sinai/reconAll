import flywheel
import subprocess as sp
import logging
import shutil

logging.basicConfig(level='INFO')
log = logging.getLogger(__name__)


def create_command(subject_id, directive, input):
    command = f'recon-all -subject {subject_id} -i {input} -{directive} '
    log.info(command)

    return command


def call_command(command):
    result = sp.Popen(command.split(' '), stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, shell=True)

    # stdout, stderr = result.communicate()

    while True:
        stdout = result.stdout.readline()
        if stdout == '' and result.poll() is not None:
            break
        if stdout:
            log.info(stdout)

    pass


def cleanup(subject_id):
    output = 'flywheel/v0/output/{}'.subject_id
    input = '/opt/freesurfer/subjects/{}'.subject_id
    shutil.copytree(input, output)

    # zip output/10000 to preserve directory structure
    # remove the unzipped directory
    # id_reconall.zip


def main():
    subject_id = 'test'
    input = 'dir'
    directive = 'directive'

    command = create_command(subject_id, input, directive)
    call_command(command)
    cleanup(subject_id)
