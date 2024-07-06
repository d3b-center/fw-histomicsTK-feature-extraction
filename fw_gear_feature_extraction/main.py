"""Main module."""
import logging
import os
import json
import shutil
from zipfile import ZipFile

from fw_core_client import CoreClient
from flywheel_gear_toolkit import GearToolkitContext
import flywheel

from .colorDeconvolve import HandE_deconvolve
from .feature_extraction import get_path_features

from .run_level import get_analysis_run_level_and_hierarchy
# from .get_analysis import get_matching_analysis

log = logging.getLogger(__name__)

fw_context = flywheel.GearContext()
fw = fw_context.client

def run(client: CoreClient, gtk_context: GearToolkitContext):
    """Main entrypoint

    Args:
        client (CoreClient): Client to connect to API
        gtk_context (GearToolkitContext)
    """
    # get the Flywheel hierarchy for the run
    destination_id = gtk_context.destination["id"]
    hierarchy = get_analysis_run_level_and_hierarchy(gtk_context.client, destination_id)
    acq_label = hierarchy['acquisition_label']
    sub_label = hierarchy['subject_label']
    ses_label = hierarchy['session_label']
    project_label = hierarchy['project_label']
    group_name = hierarchy['group']

    # get the output acqusition container
    acq = fw.lookup(f'{group_name}/{project_label}/{sub_label}/{ses_label}/{acq_label}')
    acq = acq.reload()

    # get the input file
    CONFIG_FILE_PATH = '/flywheel/v0/config.json'
    with open(CONFIG_FILE_PATH) as config_file:
        config = json.load(config_file)

    input_file_name = config['inputs']['input_image']['location']['path']
    input_label_file = config['inputs']['label_image']['location']['path']

    output_dir = 'output/'

    # run the main processes & upload output file back to acquisition
    print(f'Deconvolving: {input_file_name}')
    HandE_deconvolve(input_file_name, output_dir)

    print(f'Generating features')
    get_path_features(input_label_file, output_dir)

    # print(f'Uploading to acquisition: {acq.label}/{output_dir}.zip')
    # acq.upload_file(f'{output_dir}.zip')
    # os.remove(f'{output_dir}.zip') # remove from instance to save space
