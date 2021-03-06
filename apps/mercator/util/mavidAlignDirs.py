#!/usr/bin/env python

import sys
import os
from optparse import OptionParser

usage = "usage: %prog [options]"
optparser = OptionParser(usage)
optparser.add_option("--init-dir", dest="initDir",
                     help="Initial directory to start in (default: .)",
                     default=".", metavar="DIR")
optparser.add_option("--treefile", dest="treefile",
                     help="Name of tree file in alignment directories " +
                     "(default: treefile)",
                     default="treefile", metavar="NAME")
optparser.add_option("--seqsfile", dest="seqsfile",
                     help="Name of sequence file in alignment directories " +
                     "(default: seqs.fasta)",
                     default="seqs.fasta", metavar="NAME")
optparser.add_option("--mavidpath", dest="mavid",
                     help="Path to MAVID binary (default: mavid)",
                     default="mavid", metavar="PATH")
optparser.add_option("--constraints-file", dest="constraints_file",
                      help="Name of constraints file in alignment directories " +
                      "(default: cons)",
                      default="cons", metavar="NAME")
optparser.add_option("--skip-completed", dest="skip_completed", action="store_true",
                     help="Skip directories that already have valid MAVID output",
                     default=0)
(options, args) = optparser.parse_args()
if len(args) != 0:
    optparser.error("No arguments required")

def alignDir(dir, files):
    # Check if alignment already made
    if options.skip_completed and "mavid.mfa" in files:
	return

    # Check for required files
    for f in (options.treefile, options.seqsfile, options.seqsfile + ".masked"):
        if f not in files:
            print >>sys.stderr, \
                  "Error: Directory '%s' does not have required file %s" % \
                  (dir, f)
            sys.exit(1)

    print >>sys.stderr, dir

    cmd_options = ""

    # Check for optional files
    if options.constraints_file in files:
        cmd_options += " -c " + options.constraints_file
    else:
        print >>sys.stderr, \
            "Warning: Directory '%s' does not have constraints file" % dir

    cmd = ("cd %s; %s %s %s %s > %s 2>&1" % \
               (dir, options.mavid, cmd_options, options.treefile, options.seqsfile,
                "mavid.log"))
    os.system(cmd)

def processDir(dir):
    isLeafDir = 1
    files = os.listdir(dir)
    for f in files:
        fPath = os.path.join(dir, f)
        if os.path.isdir(fPath):
            processDir(fPath)
            isLeafDir = 0
    if isLeafDir:
        alignDir(dir, files)

processDir(options.initDir)
