.DEFAULT_GOAL := help

help: ## Show available goals and engine options (default)
	@printf '%s\n' 'Usage: make [goal] [ENGINE=rpt|tarql]' '' 'Goals:'
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf '%s\n' '' 'Engines:' \
		'  ENGINE=rpt    Docker aksw/rpt:2.0.0-rc7 (default)' \
		'  ENGINE=tarql  Docker mikulas/tarql with UTF-8 input'

.DELETE_ON_ERROR:
CURL ?= curl
OGR2OGR ?= ogr2ogr
SOURCE_URL := https://unstats.un.org/unsd/classifications/Econ/tables/CPC/CPCv21_ISIC4/cpc21-isic4.txt

ENGINE ?= rpt

RPT_TARQL = docker run --rm -i -v "$(CURDIR):/data" aksw/rpt:2.0.0-rc7 sansa tarql
ORIGINAL_TARQL = docker run --rm -i -v "$(CURDIR):/data" mikulas/tarql -e utf-8

ifeq ($(ENGINE),rpt)
TARQL = $(RPT_TARQL)
TARQL_OUTPUT_ARGS = --out-format turtle/blocks
else ifeq ($(ENGINE),tarql)
TARQL = $(ORIGINAL_TARQL)
TARQL_OUTPUT_ARGS =
else
$(error ENGINE must be either rpt or tarql)
endif

NAME := isic4-cpc21
TARGET_DIR := target
SOURCE := $(TARGET_DIR)/resources/source.csv
CSV := $(TARGET_DIR)/$(NAME).csv
TTL := $(TARGET_DIR)/$(NAME).ttl

.PHONY: all download csv clean distclean help
all: $(TTL) ## Download, extract CSV and generate RDF
download: $(SOURCE) ## Download the official source into target/resources/
csv: $(CSV) ## Download and extract the mapping CSV into target/

$(TARGET_DIR) $(TARGET_DIR)/resources:
	mkdir -p $@

$(SOURCE): | $(TARGET_DIR)/resources
	$(CURL) --fail --location --retry 3 "$(SOURCE_URL)" -o $@.tmp
	mv $@.tmp $@

$(CSV): $(SOURCE) Makefile | $(TARGET_DIR)
	rm -f $@.tmp.csv
	$(OGR2OGR) -f CSV $@.tmp.csv $< -oo AUTODETECT_TYPE=NO -sql 'SELECT ISIC4code AS isic_rev4, CPC21code AS cpc21, ISIC4partial AS isic_partial, CPC21partial AS cpc_partial FROM source WHERE ISIC4code <> '"'"'n/a'"'"'' -lco STRING_QUOTING=ALWAYS
	mv $@.tmp.csv $@

$(TTL): $(CSV) $(NAME).tarql.rq Makefile
	$(TARQL) /data/$(NAME).tarql.rq /data/$(CSV) $(TARQL_OUTPUT_ARGS) > $@.tmp
	mv $@.tmp $@

clean: ## Remove all generated files and downloads under target/
	rm -rf $(TARGET_DIR)

distclean: clean ## Alias for clean; remove all generated files and downloads
