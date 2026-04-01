"""EHDS DataHolder MCP Server.

Exposes tools for generating and validating HealthDCAT-AP metadata,
enabling EHDS data holders to publish to the European Health Data Space
central catalog.
"""

from __future__ import annotations

import json
import textwrap
from typing import Any

from mcp.server.fastmcp import FastMCP

from .generator import generate, validate_turtle
from .models import DatasetMetadata, Distribution, ContactPoint
from .vocabularies import (
    HEALTH_CATEGORIES,
    CODING_SYSTEMS,
    UPDATE_FREQUENCIES,
    LANGUAGES,
    COUNTRIES,
    HEALTH_THEMES,
    EU_DATA_THEMES,
)

mcp = FastMCP(
    "EHDS DataHolder MCP",
    instructions=textwrap.dedent("""
        This server helps EHDS (European Health Data Space) data holders publish
        their health dataset metadata to the central EHDS catalog using the
        HealthDCAT-AP metadata standard.

        Available tools:
        1. generate_healthdcat_metadata  – Generate HealthDCAT-AP compliant RDF from
           a flexible dataset description (Turtle / JSON-LD / RDF/XML output).
        2. get_metadata_template         – Get a fully-commented example showing all
           supported metadata fields.
        3. validate_healthdcat_turtle    – Validate a Turtle RDF document against
           basic HealthDCAT-AP requirements.
        4. list_supported_values         – List supported values for a vocabulary
           field (health_category, coding_system, language, country, frequency).

        Typical workflow:
        1. Call get_metadata_template to understand available fields.
        2. Collect dataset description from the data holder (free text, forms, etc.).
        3. Call generate_healthdcat_metadata with the extracted fields.
        4. Optionally call validate_healthdcat_turtle on the output.
        5. Submit the RDF to the EHDS metadata catalog.
    """),
)


# ---------------------------------------------------------------------------
# Tool: generate_healthdcat_metadata
# ---------------------------------------------------------------------------

@mcp.tool()
def generate_healthdcat_metadata(
    # --- Mandatory ---
    title: str,
    description: str,
    publisher_name: str,
    # --- Identification ---
    identifier: str | None = None,
    publisher_identifier: str | None = None,
    publisher_url: str | None = None,
    creator_name: str | None = None,
    creator_identifier: str | None = None,
    # --- Contact ---
    contact_name: str | None = None,
    contact_email: str | None = None,
    contact_url: str | None = None,
    contact_phone: str | None = None,
    contact_organisation: str | None = None,
    # --- Temporal ---
    issued: str | None = None,
    modified: str | None = None,
    temporal_start: str | None = None,
    temporal_end: str | None = None,
    update_frequency: str | None = None,
    # --- Geographic ---
    spatial_coverage: list[str] | None = None,
    spatial_resolution: str | None = None,
    # --- Discovery ---
    keywords: list[str] | None = None,
    language: list[str] | None = None,
    additional_themes: list[str] | None = None,
    # --- Health classification ---
    health_category: list[str] | None = None,
    health_theme: list[str] | None = None,
    coding_systems: list[str] | None = None,
    # --- Population ---
    min_age: int | None = None,
    max_age: int | None = None,
    number_of_individuals: int | None = None,
    number_of_records: int | None = None,
    population_coverage: str | None = None,
    # --- Legal & governance ---
    access_rights: str | None = None,
    license: str | None = None,
    legal_basis: str | None = None,
    personal_data_handling: str | None = None,
    purpose_of_collection: str | None = None,
    retention_period: str | None = None,
    # --- Standards ---
    conforms_to: list[str] | None = None,
    # --- Distributions (JSON-encoded list of objects) ---
    distributions_json: str | None = None,
    # --- Other ---
    is_part_of: str | None = None,
    related_resources: list[str] | None = None,
    provenance: str | None = None,
    landing_page: str | None = None,
    version: str | None = None,
    additional_properties_json: str | None = None,
    # --- Output control ---
    output_format: str = "turtle",
    base_uri: str = "https://data.healthdata.eu/datasets/",
) -> str:
    """
    Generate HealthDCAT-AP compliant RDF metadata for an EHDS health dataset.

    This tool converts a semi-structured dataset description into a valid
    HealthDCAT-AP RDF document that can be submitted to the EHDS central catalog.

    **Mandatory fields:** title, description, publisher_name.
    All other fields are optional but improve catalog discoverability and compliance.

    The generator automatically:
    - Adds the mandatory HEAL (health) EU data theme
    - Resolves country names/codes to EU Named Authority List URIs
    - Resolves language codes/names to EU NAL URIs
    - Resolves health category names to HealthDCAT-AP vocabulary URIs
    - Resolves terminology system names to canonical ontology URIs
    - Mints a dataset URI from the title if no identifier is provided

    **Distributions:** Pass as a JSON array string, e.g.:
    ```json
    [{"title": "FHIR API", "format": "FHIR", "access_url": "https://..."}]
    ```

    **Output formats:** "turtle" (default), "json-ld", "rdf/xml", "n-triples"
    """
    # Parse optional JSON args
    distributions = None
    if distributions_json:
        try:
            raw_dists = json.loads(distributions_json)
            if isinstance(raw_dists, list):
                distributions = [Distribution(**d) for d in raw_dists]
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            return f"Error: Invalid distributions_json – {e}"

    additional_properties = None
    if additional_properties_json:
        try:
            additional_properties = json.loads(additional_properties_json)
        except json.JSONDecodeError as e:
            return f"Error: Invalid additional_properties_json – {e}"

    # Build contact point if any contact details provided
    contact_point = None
    if any([contact_name, contact_email, contact_url, contact_phone, contact_organisation]):
        contact_point = ContactPoint(
            name=contact_name,
            email=contact_email,
            url=contact_url,
            phone=contact_phone,
            organisation=contact_organisation,
        )

    try:
        meta = DatasetMetadata(
            title=title,
            description=description,
            publisher_name=publisher_name,
            identifier=identifier,
            publisher_identifier=publisher_identifier,
            publisher_url=publisher_url,
            creator_name=creator_name,
            creator_identifier=creator_identifier,
            contact_point=contact_point,
            issued=issued,
            modified=modified,
            temporal_start=temporal_start,
            temporal_end=temporal_end,
            update_frequency=update_frequency,
            spatial_coverage=spatial_coverage,
            spatial_resolution=spatial_resolution,
            keywords=keywords,
            language=language,
            additional_themes=additional_themes,
            health_category=health_category,
            health_theme=health_theme,
            coding_systems=coding_systems,
            min_age=min_age,
            max_age=max_age,
            number_of_individuals=number_of_individuals,
            number_of_records=number_of_records,
            population_coverage=population_coverage,
            access_rights=access_rights,
            license=license,
            legal_basis=legal_basis,
            personal_data_handling=personal_data_handling,
            purpose_of_collection=purpose_of_collection,
            retention_period=retention_period,
            conforms_to=conforms_to,
            distributions=distributions,
            is_part_of=is_part_of,
            related_resources=related_resources,
            provenance=provenance,
            landing_page=landing_page,
            version=version,
            additional_properties=additional_properties,
            output_format=output_format,
            base_uri=base_uri,
        )
    except ValueError as e:
        return f"Validation error: {e}"

    try:
        rdf_output = generate(meta)
    except Exception as e:
        return f"Generation error: {e}"

    return rdf_output


# ---------------------------------------------------------------------------
# Tool: get_metadata_template
# ---------------------------------------------------------------------------

@mcp.tool()
def get_metadata_template(include_distributions: bool = True) -> str:
    """
    Return a comprehensive metadata template showing all supported fields with
    example values and descriptions.

    Use this to understand what information can be collected from a data holder
    before calling generate_healthdcat_metadata.

    Set include_distributions=True to include distribution examples (default).
    """
    template = {
        "_comment": (
            "HealthDCAT-AP Metadata Template – provide as many fields as available. "
            "Only title, description, and publisher_name are strictly required."
        ),

        # Mandatory
        "title": "Dutch Cardiovascular Disease Registry 2010-2022",
        "description": (
            "Population-based registry of cardiovascular disease diagnoses "
            "in the Netherlands covering 2010-2022. Contains ICD-10 coded "
            "diagnoses, treatment records, and outcomes for ~4.2 million patients."
        ),
        "publisher_name": "Dutch Institute for Health Records (DIHR)",

        # Identification
        "identifier": "https://data.dihr.nl/datasets/cvd-registry-2010-2022",
        "publisher_identifier": "https://ror.org/example-dihr",
        "publisher_url": "https://www.dihr.nl",
        "creator_name": "DIHR Data Science Department",
        "creator_identifier": "https://www.dihr.nl/departments/data-science",

        # Contact
        "contact_name": "Dr. Jane Smith",
        "contact_email": "dataaccess@dihr.nl",
        "contact_url": "https://www.dihr.nl/contact",
        "contact_phone": "+31-20-123-4567",
        "contact_organisation": "Dutch Institute for Health Records",

        # Temporal
        "issued": "2023-06-01",
        "modified": "2024-11-15",
        "temporal_start": "2010-01-01",
        "temporal_end": "2022-12-31",
        "update_frequency": "annual",

        # Geographic
        "spatial_coverage": ["NL"],
        "spatial_resolution": "national",

        # Discovery
        "keywords": ["cardiovascular", "heart disease", "registry", "Netherlands", "ICD-10"],
        "language": ["nl", "en"],
        "additional_themes": ["science"],

        # Health classification
        "health_category": ["registry", "EHR"],
        "health_theme": ["cardiovascular", "heart disease"],
        "coding_systems": ["ICD-10", "SNOMED CT", "ATC"],

        # Population
        "min_age": 18,
        "max_age": 99,
        "number_of_individuals": 4200000,
        "number_of_records": 18500000,
        "population_coverage": (
            "Adults aged 18+ with cardiovascular disease diagnoses in the Netherlands. "
            "Covers approximately 87% of the Dutch adult population."
        ),

        # Legal & governance
        "access_rights": "restricted",
        "license": "CC BY 4.0",
        "legal_basis": "GDPR Article 9(2)(b) – medical research with safeguards",
        "personal_data_handling": "Pseudonymised",
        "purpose_of_collection": "Clinical care, quality assessment, public health research",
        "retention_period": "30 years from last patient contact",

        # Standards
        "conforms_to": ["OMOP CDM v5.4", "HL7 FHIR R4"],

        # Other
        "landing_page": "https://www.dihr.nl/data/cvd-registry",
        "version": "3.2",
        "provenance": "Derived from hospital EHR systems via standardized ETL pipeline v2.1",
        "is_part_of": "https://www.dihr.nl/datasets/national-health-catalog",

        # Output control
        "output_format": "turtle",
        "base_uri": "https://data.healthdata.eu/datasets/",

        # Supported values reference
        "_health_category_values": list(set(HEALTH_CATEGORIES.keys()))[:15],
        "_health_theme_values": list(set(HEALTH_THEMES.keys()))[:15],
        "_coding_system_values": list(set(CODING_SYSTEMS.keys()))[:15],
        "_language_values_example": ["en", "nl", "de", "fr", "es", "it", "sv", "da"],
        "_country_values_example": [
            "NL", "DE", "FR", "BE", "SE", "DK", "FI", "NO", "ES", "IT", "PL"
        ],
        "_access_rights_values": ["public", "restricted", "non-public"],
        "_update_frequency_values": [
            "annual", "monthly", "quarterly", "daily", "weekly", "irregular",
            "continuous", "never",
        ],
        "_output_format_values": ["turtle", "json-ld", "rdf/xml", "n-triples"],
    }

    if include_distributions:
        template["distributions_json"] = json.dumps([
            {
                "title": "FHIR R4 REST API",
                "description": "Access via HL7 FHIR R4 REST API (requires data access agreement)",
                "format": "FHIR",
                "media_type": "application/fhir+json",
                "access_url": "https://fhir.dihr.nl/r4/cardiovascular",
                "license": "CC BY 4.0",
            },
            {
                "title": "Bulk CSV Export",
                "description": "Annual bulk export in OMOP CDM CSV format",
                "format": "CSV",
                "media_type": "text/csv",
                "access_url": "https://data.dihr.nl/request/cvd-registry",
                "download_url": "https://data.dihr.nl/download/cvd-registry-2022.zip",
                "byte_size": 2500000000,
                "issued": "2023-06-01",
                "license": "CC BY 4.0",
                "conforms_to": ["OMOP CDM v5.4"],
            },
        ], indent=2)

    return json.dumps(template, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Tool: validate_healthdcat_turtle
# ---------------------------------------------------------------------------

@mcp.tool()
def validate_healthdcat_turtle(turtle_rdf: str) -> str:
    """
    Validate a HealthDCAT-AP Turtle RDF document for basic structural compliance.

    Checks:
    - RDF can be parsed (syntax validity)
    - Presence of dcat:Dataset type
    - Mandatory properties: dct:title, dct:description, dct:publisher
    - Presence of the mandatory HEAL data theme (dcat:theme)

    Returns a JSON report with 'valid' (bool) and 'issues' (list of strings).
    """
    is_valid, issues = validate_turtle(turtle_rdf)
    result = {
        "valid": is_valid,
        "issues": issues,
        "issue_count": len(issues),
        "summary": (
            "No HealthDCAT-AP issues found." if is_valid
            else f"{len(issues)} issue(s) found. See 'issues' for details."
        ),
    }
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Tool: list_supported_values
# ---------------------------------------------------------------------------

@mcp.tool()
def list_supported_values(
    vocabulary: str,
    filter_prefix: str | None = None,
) -> str:
    """
    List the supported values for a specific vocabulary field.

    Available vocabularies:
    - "health_category"  – Types of health data (EHR, claims, registry, etc.)
    - "health_theme"     – Health topics (cancer, cardiovascular, diabetes, etc.)
    - "coding_system"    – Terminology systems (ICD-10, SNOMED CT, LOINC, etc.)
    - "language"         – Language codes and names
    - "country"          – Country codes and names (EU/EEA focus)
    - "frequency"        – Update frequency values
    - "access_rights"    – Access rights levels
    - "output_format"    – Supported RDF output formats

    Use filter_prefix to filter results (e.g., filter_prefix="icd" shows ICD variants).

    Returns a JSON object mapping input values to their resolved URIs.
    """
    vocab_map: dict[str, dict[str, str]] = {
        "health_category": HEALTH_CATEGORIES,
        "health_theme": HEALTH_THEMES,
        "coding_system": CODING_SYSTEMS,
        "language": LANGUAGES,
        "country": COUNTRIES,
        "frequency": UPDATE_FREQUENCIES,
        "access_rights": {
            "public": "http://publications.europa.eu/resource/authority/access-right/PUBLIC",
            "restricted": "http://publications.europa.eu/resource/authority/access-right/RESTRICTED",
            "non-public": "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC",
            "non public": "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC",
            "private": "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC",
        },
        "output_format": {
            "turtle": "Turtle (text/turtle) – default, human-readable",
            "json-ld": "JSON-LD (application/ld+json) – JSON-based linked data",
            "rdf/xml": "RDF/XML (application/rdf+xml) – XML serialization",
            "n-triples": "N-Triples (application/n-triples) – line-based, machine-friendly",
        },
    }

    vocab_lower = vocabulary.strip().lower().replace("-", "_")
    mapping = vocab_map.get(vocab_lower)

    if mapping is None:
        available = list(vocab_map.keys())
        return json.dumps({
            "error": f"Unknown vocabulary '{vocabulary}'",
            "available_vocabularies": available,
        }, indent=2)

    if filter_prefix:
        fp = filter_prefix.strip().lower()
        filtered = {k: v for k, v in mapping.items() if k.startswith(fp)}
    else:
        filtered = dict(mapping)

    # Deduplicate values (multiple keys often map to same URI)
    unique: dict[str, str] = {}
    seen_uris: set[str] = set()
    for k, v in filtered.items():
        if v not in seen_uris:
            unique[k] = v
            seen_uris.add(v)

    return json.dumps({
        "vocabulary": vocabulary,
        "count": len(unique),
        "values": unique,
        "_note": (
            "Pass any key (or its synonym) to the corresponding field in "
            "generate_healthdcat_metadata. The generator resolves it to the correct URI."
        ),
    }, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server using stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
