# EHDS DataHolder MCP

A tool server for EHDS (European Health Data Space) data holders to publish their dataset metadata to the central EHDS catalog using the [HealthDCAT-AP](https://healthdcat-ap.github.io/) metadata standard.

## Overview

This server exposes tools that convert semi-structured dataset descriptions into HealthDCAT-AP compliant RDF metadata (Turtle, JSON-LD, RDF/XML). Data holders provide whatever information they have about their datasets; the server handles vocabulary resolution, URI minting, and RDF serialization.

## Tools

| Tool | Description |
|------|-------------|
| `generate_healthdcat_metadata` | Generate HealthDCAT-AP RDF from a dataset description |
| `get_metadata_template` | Get a fully-annotated example showing all supported fields |
| `validate_healthdcat_turtle` | Validate a Turtle RDF document for HealthDCAT-AP compliance |
| `list_supported_values` | List accepted values for vocabulary fields |

## HealthDCAT-AP Support

The generator supports the full HealthDCAT-AP property set including:

- All DCAT-AP 3.0 mandatory and recommended properties
- Health-specific extensions: `healthdcatap:healthCategory`, `healthdcatap:healthTheme`, `healthdcatap:hasCodingSystem`, `healthdcatap:minTypicalAge`, `healthdcatap:maxTypicalAge`, `healthdcatap:numberOfUniqueIndividuals`, `healthdcatap:numberOfRecords`, `healthdcatap:populationCoverage`, `healthdcatap:hasLegalBasis`, `healthdcatap:hasPersonalDataHandling`, `healthdcatap:purposeOfCollection`
- Automatic vocabulary resolution: country names/codes → EU Named Authority List URIs, language codes → EU NAL, health categories → HealthDCAT-AP vocabulary, terminology systems → canonical ontology URIs
- Mandatory HEAL EU data theme automatically added to all datasets

## Installation

```bash
pip install -e .
```

## Usage

Run as a stdio MCP server:

```bash
ehds-dataholder-mcp
```

## Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

## License

MIT
