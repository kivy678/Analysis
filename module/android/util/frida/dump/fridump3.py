from module.android.util.frida.dump import dumper, utils

import textwrap
import frida
import os
import sys
import frida.core
import argparse
import logging

logo = """
        ______    _     _
        |  ___|  (_)   | |
        | |_ _ __ _  __| |_   _ _ __ ___  _ __
        |  _| '__| |/ _` | | | | '_ ` _ \| '_ \\
        | | | |  | | (_| | |_| | | | | | | |_) |
        \_| |_|  |_|\__,_|\__,_|_| |_| |_| .__/
                                         | |
                                         |_|
        """


# Main Menu
def DUMP(output, pkg, strings=True, log=False, usb=True, host=None):
    # Define Configurations
    APP_NAME = utils.normalize_app_name(appName=pkg)
    DIRECTORY = ""
    USB = usb
    NETWORK=False
    DEBUG_LEVEL = logging.INFO
    STRINGS = strings
    MAX_SIZE = 20971520
    PERMS = 'rw-'

    if host is not None:
      NETWORK=True
      IP=host

    #if arguments.read_only:
    #    PERMS = 'r--'

    if log:
        DEBUG_LEVEL = logging.DEBUG
    logging.basicConfig(format='%(levelname)s:%(message)s', level=DEBUG_LEVEL)


    # Start a new Session
    session = None
    try:
        if USB:
            session = frida.get_usb_device().attach(APP_NAME)
        elif NETWORK:
            session = frida.get_device_manager().add_remote_device(IP).attach(APP_NAME)
        else:
            session = frida.attach(APP_NAME)
    except Exception as e:
        print(str(e))
        sys.exit()


    # Selecting Output directory
    if output is not None:
        DIRECTORY = output
        if os.path.isdir(DIRECTORY):
            print("Output directory is set to: " + DIRECTORY)
        else:
            print("The selected output directory does not exist!")
            sys.exit(1)

    else:
        print("Current Directory: " + str(os.getcwd()))
        DIRECTORY = os.path.join(os.getcwd(), "dump")
        print("Output directory is set to: " + DIRECTORY)
        if not os.path.exists(DIRECTORY):
            print("Creating directory...")
            os.makedirs(DIRECTORY)

    mem_access_viol = ""

    print("Starting Memory dump...")

    def on_message(message, data):
        print("[on_message] message:", message, "data:", data)


    script = session.create_script("""'use strict';

    rpc.exports = {
      enumerateRanges: function (prot) {
        return Process.enumerateRangesSync(prot);
      },
      readMemory: function (address, size) {
        return Memory.readByteArray(ptr(address), size);
      }
    };
    """)
    script.on("message", on_message)
    script.load()

    agent = script.exports
    ranges = agent.enumerate_ranges(PERMS)

    #if arguments.max_size is not None:
    #    MAX_SIZE = arguments.max_size

    i = 0
    l = len(ranges)

    # Performing the memory dump
    for range in ranges:
        logging.debug("Base Address: " + str(range["base"]))
        logging.debug("")
        logging.debug("Size: " + str(range["size"]))
        if range["size"] > MAX_SIZE:
            logging.debug("Too big, splitting the dump into chunks")
            mem_access_viol = dumper.splitter(
                agent, range["base"], range["size"], MAX_SIZE, mem_access_viol, DIRECTORY)
            continue
        mem_access_viol = dumper.dump_to_file(
            agent, range["base"], range["size"], mem_access_viol, DIRECTORY)
        i += 1
        utils.printProgress(i, l, prefix='Progress:', suffix='Complete', bar=50)

    # Run Strings if selected

    if STRINGS:
        files = os.listdir(DIRECTORY)
        i = 0
        l = len(files)
        print("Running strings on all files:")
        for f1 in files:
            utils.strings(f1, DIRECTORY)
            i += 1
            utils.printProgress(i, l, prefix='Progress:',
                                suffix='Complete', bar=50)
    print("Finished!")
    #raw_input('Press Enter to exit...')
