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

CSV_NAMES = \
	sectors \
	code-to-isicrev4 \
	industry-aggregate-labels \
	industry-aggregate-code-to-isicrev4divisions

TARGET_DIR = target
TTL_FILES = $(addprefix $(TARGET_DIR)/,$(addsuffix .ttl,$(CSV_NAMES)))

.PHONY: all clean help

all: $(TTL_FILES) ## Generate all RDF files

$(TARGET_DIR):
	mkdir -p $@

$(TARGET_DIR)/%.ttl: %.csv %.tarql.rq | $(TARGET_DIR)
	$(TARQL) /data/$*.tarql.rq /data/$*.csv $(TARQL_OUTPUT_ARGS) > $@.tmp
	mv $@.tmp $@

clean: ## Remove generated RDF files
	rm -f $(TTL_FILES) $(addsuffix .tmp,$(TTL_FILES))
	rmdir $(TARGET_DIR) 2>/dev/null || true

help: ## Show available targets and engines
	@printf '%s\n' \
		'make              # Generate all RDF with rpt (default)' \
		'make ENGINE=rpt   # Use aksw/rpt:2.0.0-rc7 sansa tarql' \
		'make ENGINE=tarql # Use mikulas/tarql with UTF-8 input' \
		'make clean        # Remove generated RDF files'
