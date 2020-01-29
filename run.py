#!/usr/bin/env python3
import flywheel
import subprocess as sp
import logging
import shutil
import os
import json

logging.basicConfig(level='DEBUG')
log = logging.getLogger(__name__)

environ_json = '/tmp/gear_environ.json'

def set_environment():

    # Let's ensure that we have our environment .json file and load it up
    if os.path.exists(environ_json):

        # If it exists, read the file in as a python dict with json.load
        with open(environ_json, 'r') as f:
            log.info('Loading gear environment')
            environ = json.load(f)

        # Now set the current environment using the keys.  This will automatically be used with any sp.run() calls,
        # without the need to pass in env=...  Passing env= will unset all these variables, so don't use it if you do it
        # this way.
        for key in environ.keys():
            os.environ[key] = environ[key]
    else:
        log.warning('No Environment file found!')
    # Pass back the environ dict in case the run.py program has need of it later on.
    return environ

def create_command(subject_id, input_volume, directive):
    command = 'recon-all -subject {} -i {} -{}'.format(subject_id, input_volume, directive)
    log.info(command)

    return command


def call_command(command):
    #result = sp.Popen(command.split(' '), stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, shell=True)
    result = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, shell=True)

    # stdout, stderr = result.communicate()
    # log.info(stdout)
    # log.info(stderr)

    while True:
        stdout = result.stdout.readline()
        if stdout == '' and result.poll() is not None:
            break
        if stdout:
            log.info(stdout)

    pass


def cleanup(subject_id, directive):
    output_freesurf = '/opt/freesurfer/subjects/{}'.format(subject_id)
    output_flywheel = '/flywheel/v0/output/{}_{}'.format(subject_id, directive)

    shutil.make_archive(output_flywheel, 'zip', output_freesurf)

    shutil.rmtree(output_freesurf)


def main():
    context = flywheel.GearContext()
    config = context.config
    
    set_environment()

    # Load in paths to input files for the gear
    input_volume = context.get_input_path('t1w_anatomy')  # A zip file with NIfTI

    # Load in values from the gear configuration
    subject_id = config['subject_id']  # Name of folder containing subject i.e., 10000
    directive = config['directive']  # Flag indicating subset of processing steps i.e., autorecon1

    # input_volume = '/Users/pereanez/Documents/flywheel/gears/reconAll/data/10000/Sag_T1.nii.gz'
    # subject_id = '10000'
    # directive = 'autorecon1'

    command = create_command(subject_id, input_volume, directive)

    call_command(command)

    cleanup(subject_id, directive)


if __name__ == '__main__':
    log.info('Info Test')
    log.debug('Debug Test')
    main()
