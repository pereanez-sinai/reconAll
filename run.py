#!/usr/bin/env python3
import flywheel
import subprocess as sp
import logging
import shutil

logging.basicConfig(level='DEBUG')
log = logging.getLogger(__name__)


def create_command(subject_id, input_volume, directive):
    command = 'recon-all -subject {} -i {} -{}'.format(subject_id, input_volume, directive)
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


def cleanup(subject_id, directive):
    output_freesurf = '/opt/freesurfer/subjects/{}'.format(subject_id)
    output_flywheel = 'flywheel/v0/output/{}_{}'.format(subject_id, directive)

    shutil.make_archive(output_flywheel, 'zip', output_freesurf)

    shutil.rmtree(output_freesurf)


def main():
    context = flywheel.GearContext()
    config = context.config

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
