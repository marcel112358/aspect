# Helper Makefile to generate the plots for the doc
ASPECT_BIN?=../../../build/aspect
MPI_NP?=6
EXPERIMENTS?=gerya_2019_vep gerya_2019_vp gerya_2019_vp_damper
OUTPUT_DIR_PREFIX?=output_

PYTHON?=python3

.PHONY: all
all: $(addprefix doc/,$(addsuffix .svg,$(EXPERIMENTS)))

doc/%.svg: gerya_2019_analysis.py $(OUTPUT_DIR_PREFIX)%/log.txt
	python3 gerya_2019_analysis.py -o $(OUTPUT_DIR_PREFIX)$* -p $@

%/log.txt:
	mpirun -n $(MPI_NP) $(ASPECT_BIN) $(subst $(OUTPUT_DIR_PREFIX),,$(*F)).prm

.PHONY: clean
clean:
	$(RM) $(addprefix doc/,$(addsuffix .svg,$(EXPERIMENTS)))
