
P4_SOURCE = program.p4
P4_OBJECT = $(P4_SOURCE:.p4=.json)

# JSON object file as seen from $(P4BM_DIR)
P4_OBJECT_TEST = ../$(P4_OBJECT)

# Default testcase directory.  Assumes each test case is a subdir below the sim dir.
P4BM_DIR = test-case1

# Testcase directory list to use for p4bm simulation
# P4BM_DIRS = test-case1 test-case2 test-case3
P4BM_DIRS = test-case1 test-case2 test-case3 test-case4

# Files within each testcase directory, as seen from within $(P4BM_DIR)
# Note that $(P4BM_OUTPUT_PCAP) and $(P4BM_OUTPUT_META) are
# implicitly named in $(P4BM_SCRIPT).
P4BM_SCRIPT         = cli_commands.txt
P4BM_LOGFILE_PREFIX = $(P4BM_SCRIPT)
P4BM_OUTPUT_PCAP    = packets_out.pcap
P4BM_OUTPUT_USER    = packets_out.user
P4BM_OUTPUT_META    = packets_out.meta
P4BM_OUTPUTS        = $(P4BM_LOGFILE_PREFIX)_cli.txt $(P4BM_LOGFILE_PREFIX)_model.txt \
                      $(P4BM_OUTPUT_META) $(P4BM_OUTPUT_PCAP) $(P4BM_OUTPUT_USER)

# Executable pathnames (particularly if they're not in $PATH)
P4C_VITISNET      = p4c-vitisnet
RUN_P4BM_VITISNET = run-p4bm-vitisnet

# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------
sim-all:
	for d in $(P4BM_DIRS); do $(MAKE) P4BM_DIR=$$d sim || exit 1; done

sim: build
# Make sure that $(P4BM_DIR)/$(P4BM_SCRIPT) exists (avoids issues if script is missing).
	(cd $(P4BM_DIR) && wc $(P4BM_SCRIPT) > /dev/null)
	(cd $(P4BM_DIR) && $(RUN_P4BM_VITISNET) -l $(P4BM_LOGFILE_PREFIX) \
                                             -j $(P4_OBJECT_TEST) -s $(P4BM_SCRIPT) )
build: $(P4_OBJECT)


cleansim-all:
	for d in $(P4BM_DIRS); do $(MAKE) P4BM_DIR=$$d cleansim; done

cleansim:
	cd $(P4BM_DIR) && rm -f $(P4BM_OUTPUTS) && rm -f *.log

clean: cleansim-all
	rm -f $(P4_OBJECT)

%.json: %.p4
	$(P4C_VITISNET) $< -o $@

