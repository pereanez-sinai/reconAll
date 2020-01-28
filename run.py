import flywheel
import subprocess as sp
import logging
import shutil

logging.basicConfig(level='INFO')
log = logging.getLogger(__name__)


def create_command(subject_id, input_volume, directive):
    command = f'recon-all -subject {subject_id} -i {input_volume} -{directive} '
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
    output_freesurf = f'/opt/freesurfer/subjects/{subject_id}'
    output_flywheel = f'flywheel/v0/output/{subject_id}_{directive}'

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

    command = create_command(subject_id, input_volume, directive)

    call_command(command)

    cleanup(subject_id, directive)
