"""Pydantic models for HealthDCAT-AP dataset metadata input."""

from __future__ import annotations

from typing import Annotated, Any
from pydantic import BaseModel, Field, field_validator, model_validator
import re


class ContactPoint(BaseModel):
    """Contact information for the dataset (vcard:Kind)."""

    name: str | None = Field(None, description="Name of the contact person or department")
    email: str | None = Field(None, description="Contact email address")
    url: str | None = Field(None, description="URL of a contact form or page")
    phone: str | None = Field(None, description="Contact phone number")
    organisation: str | None = Field(None, description="Organisation name of the contact point")


class Distribution(BaseModel):
    """A specific representation or access point for the dataset (dcat:Distribution)."""

    title: str | None = Field(None, description="Title of this distribution")
    description: str | None = Field(None, description="Description of this distribution")
    format: str | None = Field(
        None,
        description="File format (e.g. 'CSV', 'JSON', 'FHIR', 'HL7 CDA', 'Parquet', 'RDF/Turtle')",
    )
    media_type: str | None = Field(
        None,
        description="IANA media type (e.g. 'text/csv', 'application/json', 'application/fhir+json')",
    )
    access_url: str | None = Field(
        None,
        description="URL of the page giving access to the distribution (required if no download_url)",
    )
    download_url: str | None = Field(None, description="Direct download URL for the distribution")
    license: str | None = Field(
        None, description="License for this distribution (URL or common name like 'CC BY 4.0')"
    )
    byte_size: int | None = Field(None, description="Size of the distribution in bytes", ge=0)
    issued: str | None = Field(None, description="Publication date (ISO 8601, e.g. '2023-01-01')")
    modified: str | None = Field(
        None, description="Last modification date (ISO 8601, e.g. '2024-06-30')"
    )
    rights: str | None = Field(None, description="Access rights statement for this distribution")
    conforms_to: list[str] | None = Field(
        None,
        description="Standards or specifications the distribution conforms to",
    )


class DatasetMetadata(BaseModel):
    """
    Semi-structured metadata descriptor for an EHDS health dataset.

    Mandatory fields are `title`, `description`, and `publisher_name`.
    All other fields are optional but recommended for HealthDCAT-AP compliance.
    The generator will automatically:
    - Add the mandatory HEAL (Health) EU data theme
    - Resolve language/country codes to EU Named Authority List URIs
    - Resolve health category names to HealthDCAT-AP vocabulary URIs
    - Resolve coding system names to canonical terminology URIs
    """

    # -----------------------------------------------------------------------
    # Mandatory (HealthDCAT-AP M)
    # -----------------------------------------------------------------------
    title: Annotated[str, Field(description="Title of the dataset (dct:title)", min_length=1)]
    description: Annotated[
        str,
        Field(
            description="Free-text description of the dataset (dct:description)", min_length=1
        ),
    ]
    publisher_name: Annotated[
        str,
        Field(
            description="Name of the organisation publishing this dataset (dct:publisher)",
            min_length=1,
        ),
    ]

    # -----------------------------------------------------------------------
    # Identification
    # -----------------------------------------------------------------------
    identifier: str | None = Field(
        None,
        description=(
            "Unique identifier / URI for this dataset. "
            "If omitted, one is generated from the title. "
            "Example: 'https://data.example.org/datasets/cardiac-registry-2020'"
        ),
    )
    publisher_identifier: str | None = Field(
        None,
        description=(
            "URI or identifier for the publisher organisation. "
            "Example: 'https://ror.org/...' or 'https://www.example-hospital.org'"
        ),
    )
    publisher_url: str | None = Field(
        None, description="Homepage URL of the publisher organisation"
    )
    publisher_type: str | None = Field(
        None,
        description=(
            "Type of the publishing organisation (healthdcatap:publisherType). "
            "Controlled vocabulary under development by TEHDAS2. "
            "Accepts a URI or a label e.g. 'hospital', 'research institute', 'national agency'."
        ),
    )
    publisher_note: str | None = Field(
        None,
        description=(
            "Free-text description of the publisher's activities, scope, and role "
            "(healthdcatap:publisherNote)."
        ),
    )
    creator_name: str | None = Field(
        None,
        description=(
            "Name of the organisation or person that created the dataset (dct:creator), "
            "if different from publisher"
        ),
    )
    creator_identifier: str | None = Field(None, description="URI/identifier for the creator")

    # -----------------------------------------------------------------------
    # Contact
    # -----------------------------------------------------------------------
    contact_point: ContactPoint | None = Field(
        None,
        description="Contact information for enquiries about the dataset (dcat:contactPoint)",
    )

    # -----------------------------------------------------------------------
    # Temporal
    # -----------------------------------------------------------------------
    issued: str | None = Field(
        None,
        description="Publication/release date in ISO 8601 format (dct:issued). E.g. '2022-03-15'",
    )
    modified: str | None = Field(
        None,
        description="Date last modified in ISO 8601 format (dct:modified). E.g. '2024-11-01'",
    )
    temporal_start: str | None = Field(
        None,
        description=(
            "Start of the temporal coverage of the data (dct:temporal). "
            "ISO 8601 format, e.g. '2010-01-01'"
        ),
    )
    temporal_end: str | None = Field(
        None,
        description=(
            "End of the temporal coverage of the data. ISO 8601 format, e.g. '2022-12-31'. "
            "Omit if data collection is ongoing."
        ),
    )
    update_frequency: str | None = Field(
        None,
        description=(
            "How often the dataset is updated (dct:accrualPeriodicity). "
            "Accepts: 'annual', 'monthly', 'quarterly', 'daily', 'weekly', 'irregular', "
            "'continuous', 'never', etc."
        ),
    )

    # -----------------------------------------------------------------------
    # Geographic coverage
    # -----------------------------------------------------------------------
    spatial_coverage: list[str] | None = Field(
        None,
        description=(
            "Geographic coverage of the dataset (dct:spatial). "
            "Accepts ISO 3166-1 alpha-2 codes (e.g. 'NL', 'DE'), country names "
            "(e.g. 'Netherlands'), or full URIs. Multiple countries allowed."
        ),
    )
    spatial_resolution: str | None = Field(
        None,
        description=(
            "Minimum spatial separation of observations, e.g. 'national', 'regional', "
            "'municipality', '1km' (dcat:spatialResolutionInMeters accepts numeric values too)"
        ),
    )

    # -----------------------------------------------------------------------
    # Classification & discovery
    # -----------------------------------------------------------------------
    keywords: list[str] | None = Field(
        None,
        description="List of keywords/tags for discovery (dcat:keyword)",
    )
    language: list[str] | None = Field(
        None,
        description=(
            "Language(s) of the dataset content (dct:language). "
            "Accepts ISO 639-1 codes ('en', 'nl', 'de') or language names."
        ),
    )
    additional_themes: list[str] | None = Field(
        None,
        description=(
            "Additional EU data themes beyond the mandatory HEAL theme (dcat:theme). "
            "E.g. ['science', 'society', 'environment']"
        ),
    )

    # -----------------------------------------------------------------------
    # Health-specific classification
    # -----------------------------------------------------------------------
    health_category: list[str] | None = Field(
        None,
        description=(
            "Type(s) of health data (healthdcatap:healthCategory). "
            "E.g. ['EHR', 'claims', 'registry', 'genomic', 'biobank', 'survey', "
            "'imaging', 'clinical trial']"
        ),
    )
    health_theme: list[str] | None = Field(
        None,
        description=(
            "Health topic(s) covered by the dataset (healthdcatap:healthTheme). "
            "HealthDCAT-AP Release 5 requires Wikidata URIs. "
            "Accepts common names (resolved to Wikidata URIs automatically) or full Wikidata URIs. "
            "E.g. ['cancer', 'cardiovascular', 'diabetes', 'mental health', 'rare disease', "
            "'COVID-19'] or ['http://www.wikidata.org/entity/Q12078']"
        ),
    )
    coding_systems: list[str] | None = Field(
        None,
        description=(
            "Terminology/coding systems used in the dataset (healthdcatap:hasCodingSystem). "
            "E.g. ['ICD-10', 'SNOMED CT', 'LOINC', 'ATC', 'OMOP CDM', 'FHIR']"
        ),
    )

    # -----------------------------------------------------------------------
    # Population / statistics
    # -----------------------------------------------------------------------
    min_age: int | None = Field(
        None,
        description="Minimum typical age of subjects in years (healthdcatap:minTypicalAge)",
        ge=0,
        le=150,
    )
    max_age: int | None = Field(
        None,
        description="Maximum typical age of subjects in years (healthdcatap:maxTypicalAge)",
        ge=0,
        le=150,
    )
    number_of_individuals: int | None = Field(
        None,
        description=(
            "Number of unique individuals in the dataset "
            "(healthdcatap:numberOfUniqueIndividuals)"
        ),
        ge=0,
    )
    number_of_records: int | None = Field(
        None,
        description="Total number of records/observations (healthdcatap:numberOfRecords)",
        ge=0,
    )
    population_coverage: str | None = Field(
        None,
        description=(
            "Free-text description of the population covered (healthdcatap:populationCoverage). "
            "E.g. 'Adults aged 18+ with type 2 diabetes in the Netherlands, 2010-2022'"
        ),
    )

    # -----------------------------------------------------------------------
    # Legal & governance
    # -----------------------------------------------------------------------
    access_rights: str | None = Field(
        None,
        description=(
            "Access level for the dataset (dct:accessRights). "
            "Accepts: 'public', 'restricted', 'non-public' / 'private'"
        ),
    )
    license: str | None = Field(
        None,
        description=(
            "License for the dataset (dct:license). "
            "Accepts common names ('CC BY 4.0', 'CC0') or a license URI."
        ),
    )
    # Release 5: Health Data Access Body – the legally competent body responsible for
    # granting access to the dataset under EHDS (healthdcatap:hdab)
    hdab_name: str | None = Field(
        None,
        description=(
            "Name of the Health Data Access Body (HDAB) responsible for granting access "
            "to this dataset under EHDS (healthdcatap:hdab). "
            "E.g. 'Finnish Institute for Health and Welfare (THL)'"
        ),
    )
    hdab_identifier: str | None = Field(
        None,
        description="URI or identifier for the HDAB organisation",
    )
    hdab_url: str | None = Field(
        None,
        description="Homepage URL of the HDAB organisation",
    )

    legal_basis: str | None = Field(
        None,
        description=(
            "Legal basis for processing the data (dpv:hasLegalBasis – DPV namespace). "
            "E.g. 'GDPR Article 9(2)(b)', 'EHDS Regulation Article 50', "
            "or a URI to the legal act."
        ),
    )
    personal_data_handling: str | None = Field(
        None,
        description=(
            "Personal data categories present in the dataset (dpv:hasPersonalData). "
            "E.g. 'Pseudonymised health data', 'Anonymised', 'Genetic data', "
            "'Biometric data'"
        ),
    )
    purpose_of_collection: str | None = Field(
        None,
        description=(
            "Purpose(s) for which the data was collected or can be used "
            "(dpv:hasPurpose). "
            "E.g. 'Clinical care', 'Scientific research', "
            "'Public health monitoring', 'Quality assessment'"
        ),
    )
    retention_period: str | None = Field(
        None,
        description=(
            "How long the data is or will be retained "
            "(healthdcatap:retentionPeriod). E.g. '10 years', '2030-12-31'"
        ),
    )

    # -----------------------------------------------------------------------
    # Standards compliance
    # -----------------------------------------------------------------------
    conforms_to: list[str] | None = Field(
        None,
        description=(
            "Standards or specifications this dataset conforms to (dct:conformsTo). "
            "E.g. ['OMOP CDM v5.4', 'HL7 FHIR R4', 'ISO 27001']"
        ),
    )

    # -----------------------------------------------------------------------
    # Distributions
    # -----------------------------------------------------------------------
    distributions: list[Distribution] | None = Field(
        None,
        description=(
            "List of distributions / access points for the dataset (dcat:distribution). "
            "Each describes how the data can be accessed or downloaded."
        ),
    )

    # -----------------------------------------------------------------------
    # Other
    # -----------------------------------------------------------------------
    is_part_of: str | None = Field(
        None,
        description=(
            "URI of a catalog or dataset series this dataset belongs to "
            "(dct:isPartOf / dcat:inSeries)"
        ),
    )
    related_resources: list[str] | None = Field(
        None,
        description="URIs of related datasets or resources (dct:relation)",
    )
    provenance: str | None = Field(
        None,
        description=(
            "Description of the provenance / data lineage (dct:provenance). "
            "E.g. 'Derived from hospital EHR system XYZ, extracted annually'"
        ),
    )
    landing_page: str | None = Field(
        None,
        description="URL of a web page about the dataset (dcat:landingPage)",
    )
    version: str | None = Field(
        None,
        description="Version of the dataset (dcat:version / owl:versionInfo). E.g. '2.1'",
    )
    additional_properties: dict[str, Any] | None = Field(
        None,
        description=(
            "Any additional key-value properties not covered above. "
            "Keys should use prefixed notation where possible (e.g. 'dct:source', "
            "'schema:variableMeasured')."
        ),
    )

    # -----------------------------------------------------------------------
    # Output control
    # -----------------------------------------------------------------------
    output_format: str = Field(
        default="turtle",
        description=(
            "Serialization format for the RDF output. "
            "One of: 'turtle' (default), 'json-ld', 'rdf/xml', 'n-triples'"
        ),
    )
    base_uri: str = Field(
        default="https://data.healthdata.eu/datasets/",
        description="Base URI used to mint dataset and publisher URIs when none are provided",
    )

    @field_validator("output_format")
    @classmethod
    def validate_output_format(cls, v: str) -> str:
        valid = {"turtle", "json-ld", "rdf/xml", "n-triples"}
        normalized = v.strip().lower()
        if normalized not in valid:
            raise ValueError(f"output_format must be one of {valid}. Got: '{v}'")
        return normalized

    @model_validator(mode="after")
    def validate_age_range(self) -> "DatasetMetadata":
        if (
            self.min_age is not None
            and self.max_age is not None
            and self.min_age > self.max_age
        ):
            raise ValueError(
                f"min_age ({self.min_age}) must not be greater than max_age ({self.max_age})"
            )
        return self

    def _slug(self) -> str:
        """Generate a URL-safe slug from the title."""
        slug = re.sub(r"[^\w\s-]", "", self.title.lower())
        slug = re.sub(r"[\s_]+", "-", slug).strip("-")
        return slug[:80]

    def get_dataset_uri(self) -> str:
        """Return the dataset URI, generating one from title if not set."""
        if self.identifier and (
            self.identifier.startswith("http://") or self.identifier.startswith("https://")
        ):
            return self.identifier
        base = self.base_uri.rstrip("/")
        return f"{base}/{self._slug()}"
