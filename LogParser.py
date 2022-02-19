import Evtx.Evtx as evtx
from collections import OrderedDict
import xml.etree.ElementTree as ET
import re
from os.path import exists
import glob
import argparse

def get_events(input_file, parse_xml=False):
    """Opens a Windows Event Log and returns XML information from
    the event record.

    Arguments:
        input_file (str): Path to evtx file to open
        parse_xml (bool): If True, return an lxml object, otherwise a string

    Yields:
        (generator): XML information in object or string format

    Examples:
        >>> for event_xml in enumerate(get_events("System.evtx")):
        >>>     print(event_xml)

    """
    with evtx.Evtx(input_file) as event_log:
        for record in event_log.records():
            if parse_xml:
                yield record.lxml()
            else:
                yield record.xml()

def main():
    parser = argparse.ArgumentParser(description="Scraping *.evtx files",epilog="Usage: LogParser.py -f <folder>")
    parser.add_argument("folder",help="Path to evtx files")
    parser.add_argument("-f","--folder",help="Folder where are evtx logs")
    args = parser.parse_args()
    folder = args.folder

    if not exists(folder):
        print("Path {} doesn't exist".format(folder))
        return 0
    #"C:\Windows\System32\winevt\Logs\*.evtx
    for eventFile in glob.glob(folder + "\\" "*.evtx"):
        print(eventFile)
        for event_xml in enumerate(get_events(eventFile)):
            root = ET.fromstring(event_xml[1])
            for parent in root:
                for child in parent:
                    tag = re.sub(r'\{[\s\S]+\}','',child.tag)
                    if child.text is None:
                        print("{} {}".format(tag," ".join([child.attrib[key] for key in child.attrib])))
                    else:
                        print(tag,child.text)
            print("\n")

if __name__=="__main__":
    main()