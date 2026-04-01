"""Tests for the HealthDCAT-AP metadata generator."""

import json
import pytest
from rdflib import Graph, Namespace, RDF, URIRef

from ehds_dataholder_mcp.models import DatasetMetadata, Distribution, ContactPoint
from ehds_dataholder_mcp.generator import generate, validate_turtle

DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
HEALTHDCATAP = Namespace("http://healthdataportal.eu/ns/health#")
EU_DATA_THEME = "http://publications.europa.eu/resource/authority/data-theme/"


def _parse_turtle(turtle_str: str) -> Graph:
    g = Graph()
    g.parse(data=turtle_str, format="turtle")
    return g


# ---------------------------------------------------------------------------
# Minimal metadata (only mandatory fields)
# ---------------------------------------------------------------------------

def test_minimal_metadata_generates_valid_turtle():
    meta = DatasetMetadata(
        title="Test Dataset",
        description="A test health dataset",
        publisher_name="Test Hospital",
    )
    rdf = generate(meta)
    assert rdf.strip()
    g = _parse_turtle(rdf)
    assert len(g) > 0


def test_mandatory_properties_present():
    meta = DatasetMetadata(
        title="Cardiac Registry",
        description="Registry of cardiac events",
        publisher_name="National Health Institute",
    )
    rdf = generate(meta)
    g = _parse_turtle(rdf)

    datasets = list(g.subjects(RDF.type, DCAT.Dataset))
    assert len(datasets) == 1
    ds = datasets[0]

    titles = list(g.objects(ds, DCTERMS.title))
    assert any("Cardiac Registry" in str(t) for t in titles)

    descriptions = list(g.objects(ds, DCTERMS.description))
    assert len(descriptions) == 1

    publishers = list(g.objects(ds, DCTERMS.publisher))
    assert len(publishers) == 1


def test_heal_theme_always_added():
    meta = DatasetMetadata(
        title="Any Health Dataset",
        description="Description",
        publisher_name="Publisher",
    )
    rdf = generate(meta)
    g = _parse_turtle(rdf)
    datasets = list(g.subjects(RDF.type, DCAT.Dataset))
    ds = datasets[0]
    themes = [str(t) for t in g.objects(ds, DCAT.theme)]
    assert f"{EU_DATA_THEME}HEAL" in themes


# ---------------------------------------------------------------------------
# URI generation
# ---------------------------------------------------------------------------

def test_custom_identifier_used_as_dataset_uri():
    uri = "https://data.example.org/datasets/my-dataset"
    meta = DatasetMetadata(
        title="My Dataset",
        description="Desc",
        publisher_name="Pub",
        identifier=uri,
    )
    rdf = generate(meta)
    assert uri in rdf


def test_slug_uri_generated_from_title():
    meta = DatasetMetadata(
        title="Dutch Cardiovascular Registry",
        description="Desc",
        publisher_name="Pub",
    )
    rdf = generate(meta)
    assert "dutch-cardiovascular-registry" in rdf


# ---------------------------------------------------------------------------
# Vocabulary resolution
# ---------------------------------------------------------------------------

def test_country_resolved_to_eu_nal_uri():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        spatial_coverage=["Netherlands", "DE"],
    )
    rdf = generate(meta)
    g = _parse_turtle(rdf)
    ds = list(g.subjects(RDF.type, DCAT.Dataset))[0]
    spatials = [str(s) for s in g.objects(ds, DCTERMS.spatial)]
    assert "http://publications.europa.eu/resource/authority/country/NLD" in spatials
    assert "http://publications.europa.eu/resource/authority/country/DEU" in spatials


def test_language_resolved_to_eu_nal_uri():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        language=["en", "dutch"],
    )
    rdf = generate(meta)
    assert "http://publications.europa.eu/resource/authority/language/ENG" in rdf
    assert "http://publications.europa.eu/resource/authority/language/NLD" in rdf


def test_health_category_resolved():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        health_category=["EHR", "claims"],
    )
    rdf = generate(meta)
    assert "healthCategory" in rdf


def test_coding_system_icd10_resolved():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        coding_systems=["ICD-10", "SNOMED CT"],
    )
    rdf = generate(meta)
    assert "id.who.int/icd/release/10" in rdf
    assert "snomed.info/sct" in rdf


def test_frequency_resolved():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        update_frequency="annual",
    )
    rdf = generate(meta)
    assert "ANNUAL" in rdf


def test_access_rights_resolved():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        access_rights="restricted",
    )
    rdf = generate(meta)
    assert "RESTRICTED" in rdf


# ---------------------------------------------------------------------------
# Population statistics
# ---------------------------------------------------------------------------

def test_population_stats():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        min_age=18,
        max_age=65,
        number_of_individuals=1000000,
        number_of_records=5000000,
        population_coverage="Adults aged 18-65",
    )
    rdf = generate(meta)
    assert "minTypicalAge" in rdf
    assert "maxTypicalAge" in rdf
    assert "numberOfUniqueIndividuals" in rdf
    assert "numberOfRecords" in rdf
    assert "1000000" in rdf


def test_invalid_age_range_raises():
    with pytest.raises(ValueError):
        DatasetMetadata(
            title="Dataset",
            description="Desc",
            publisher_name="Pub",
            min_age=80,
            max_age=20,
        )


# ---------------------------------------------------------------------------
# Temporal coverage
# ---------------------------------------------------------------------------

def test_temporal_coverage():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        temporal_start="2010-01-01",
        temporal_end="2022-12-31",
    )
    rdf = generate(meta)
    assert "PeriodOfTime" in rdf
    assert "startDate" in rdf
    assert "endDate" in rdf


# ---------------------------------------------------------------------------
# Distributions
# ---------------------------------------------------------------------------

def test_distribution_added():
    dist = Distribution(
        title="FHIR API",
        format="FHIR",
        access_url="https://fhir.example.org/r4",
    )
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        distributions=[dist],
    )
    rdf = generate(meta)
    g = _parse_turtle(rdf)
    dists = list(g.subjects(RDF.type, DCAT.Distribution))
    assert len(dists) == 1


def test_multiple_distributions():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        distributions=[
            Distribution(title="API", access_url="https://api.example.org"),
            Distribution(title="CSV Export", access_url="https://export.example.org"),
        ],
    )
    rdf = generate(meta)
    g = _parse_turtle(rdf)
    dists = list(g.subjects(RDF.type, DCAT.Distribution))
    assert len(dists) == 2


# ---------------------------------------------------------------------------
# Output formats
# ---------------------------------------------------------------------------

def test_output_format_jsonld():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        output_format="json-ld",
    )
    rdf = generate(meta)
    parsed = json.loads(rdf)
    assert "@context" in parsed or "@graph" in parsed or "@type" in parsed or isinstance(parsed, list)


def test_output_format_rdfxml():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        output_format="rdf/xml",
    )
    rdf = generate(meta)
    assert "<?xml" in rdf or "<rdf:RDF" in rdf


def test_invalid_output_format():
    with pytest.raises(ValueError):
        DatasetMetadata(
            title="Dataset",
            description="Desc",
            publisher_name="Pub",
            output_format="markdown",
        )


# ---------------------------------------------------------------------------
# Contact point
# ---------------------------------------------------------------------------

def test_contact_point():
    meta = DatasetMetadata(
        title="Dataset",
        description="Desc",
        publisher_name="Pub",
        contact_point=ContactPoint(
            name="Dr. Smith",
            email="smith@example.org",
            url="https://example.org/contact",
        ),
    )
    rdf = generate(meta)
    assert "contactPoint" in rdf
    assert "mailto:smith@example.org" in rdf


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def test_validate_valid_turtle():
    meta = DatasetMetadata(
        title="Valid Dataset",
        description="A valid health dataset",
        publisher_name="Health Institute",
    )
    rdf = generate(meta)
    is_valid, issues = validate_turtle(rdf)
    assert is_valid
    assert issues == []


def test_validate_missing_title():
    turtle = """
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .
    <https://example.org/dataset/1> a dcat:Dataset ;
        dct:description "A dataset" ;
        dct:publisher [ a foaf:Agent ; foaf:name "Pub" ] ;
        dcat:theme <http://publications.europa.eu/resource/authority/data-theme/HEAL> .
    """
    is_valid, issues = validate_turtle(turtle)
    assert not is_valid
    assert any("dct:title" in i for i in issues)


def test_validate_missing_heal_theme():
    turtle = """
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .
    <https://example.org/dataset/1> a dcat:Dataset ;
        dct:title "Dataset" ;
        dct:description "A dataset" ;
        dct:publisher [ a foaf:Agent ; foaf:name "Pub" ] .
    """
    is_valid, issues = validate_turtle(turtle)
    assert not is_valid
    assert any("HEAL" in i for i in issues)


def test_validate_invalid_syntax():
    is_valid, issues = validate_turtle("this is not valid turtle @@##")
    assert not is_valid
    assert any("parse error" in i.lower() for i in issues)


# ---------------------------------------------------------------------------
# Full example
# ---------------------------------------------------------------------------

def test_full_example():
    """End-to-end test with a realistic dataset description."""
    meta = DatasetMetadata(
        title="Dutch Cardiovascular Disease Registry 2010-2022",
        description=(
            "Population-based registry of cardiovascular disease diagnoses "
            "in the Netherlands covering 2010-2022."
        ),
        publisher_name="Dutch Institute for Health Records",
        publisher_identifier="https://ror.org/example",
        publisher_url="https://www.dihr.nl",
        contact_point=ContactPoint(
            name="Dr. Jane Smith",
            email="dataaccess@dihr.nl",
        ),
        issued="2023-06-01",
        modified="2024-11-15",
        temporal_start="2010-01-01",
        temporal_end="2022-12-31",
        update_frequency="annual",
        spatial_coverage=["NL"],
        keywords=["cardiovascular", "heart disease", "registry"],
        language=["nl", "en"],
        health_category=["registry", "EHR"],
        health_theme=["cardiovascular"],
        coding_systems=["ICD-10", "SNOMED CT"],
        min_age=18,
        max_age=99,
        number_of_individuals=4200000,
        number_of_records=18500000,
        population_coverage="Adults aged 18+ with CVD in the Netherlands",
        access_rights="restricted",
        license="CC BY 4.0",
        legal_basis="GDPR Article 9(2)(b)",
        personal_data_handling="Pseudonymised",
        conforms_to=["OMOP CDM v5.4"],
        distributions=[
            Distribution(
                title="FHIR R4 API",
                format="FHIR",
                access_url="https://fhir.dihr.nl/r4",
                license="CC BY 4.0",
            )
        ],
    )
    rdf = generate(meta)
    g = _parse_turtle(rdf)

    datasets = list(g.subjects(RDF.type, DCAT.Dataset))
    assert len(datasets) == 1

    is_valid, issues = validate_turtle(rdf)
    assert is_valid, f"Validation issues: {issues}"
