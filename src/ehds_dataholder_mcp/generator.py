"""HealthDCAT-AP RDF generator.

Converts DatasetMetadata objects into HealthDCAT-AP compliant RDF graphs
and serializes them to Turtle, JSON-LD, RDF/XML, or N-Triples.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, date, timezone

from rdflib import (
    Graph,
    Literal,
    Namespace,
    RDF,
    RDFS,
    OWL,
    URIRef,
    BNode,
)
from rdflib.namespace import (
    DCAT,
    DCTERMS,
    FOAF,
    SKOS,
    XSD,
)

from .models import DatasetMetadata, Distribution, ContactPoint
from .vocabularies import (
    HEALTHDCATAP_NS,
    VCARD_NS,
    ADMS_NS,
    PROV_NS,
    DPV_NS,
    EU_DATA_THEME,
    EU_ACCESS_RIGHT,
    resolve_health_category,
    resolve_coding_system,
    resolve_language,
    resolve_country,
    resolve_access_rights,
    resolve_frequency,
    resolve_license,
    normalize_lookup,
    HEALTH_THEMES,
    EU_DATA_THEMES,
)

# ---------------------------------------------------------------------------
# Namespace objects
# ---------------------------------------------------------------------------

HEALTHDCATAP = Namespace(HEALTHDCATAP_NS)
VCARD = Namespace(VCARD_NS)
ADMS = Namespace(ADMS_NS)
PROV = Namespace(PROV_NS)
DPV = Namespace(DPV_NS)


def _build_graph() -> Graph:
    """Create a new RDF graph with all required namespace bindings."""
    g = Graph()
    g.bind("dcat", DCAT)
    g.bind("dct", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("skos", SKOS)
    g.bind("xsd", XSD)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("owl", OWL)
    g.bind("healthdcatap", HEALTHDCATAP)
    g.bind("vcard", VCARD)
    g.bind("adms", ADMS)
    g.bind("prov", PROV)
    g.bind("dpv", DPV)
    return g


def _uri(uri_str: str) -> URIRef:
    return URIRef(uri_str)


def _lang_literal(value: str, lang: str = "en") -> Literal:
    return Literal(value, lang=lang)


def _date_literal(value: str) -> Literal | None:
    """Parse a date string and return an XSD literal (date or dateTime)."""
    value = value.strip()
    # Try full ISO datetime
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            datetime.strptime(value, fmt)
            return Literal(value, datatype=XSD.dateTime)
        except ValueError:
            pass
    # Try date only
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return Literal(value, datatype=XSD.date)
    except ValueError:
        pass
    # Try year-month
    try:
        datetime.strptime(value, "%Y-%m")
        return Literal(f"{value}-01", datatype=XSD.date)
    except ValueError:
        pass
    # Try year only
    if re.match(r"^\d{4}$", value):
        return Literal(f"{value}-01-01", datatype=XSD.date)
    # Fall back to plain literal
    return Literal(value)


def _add_contact_point(g: Graph, contact: ContactPoint, dataset_uri: URIRef) -> None:
    """Add a vcard contact point to the graph and link it to the dataset."""
    cp = BNode()
    g.add((cp, RDF.type, VCARD.Kind))
    if contact.name:
        g.add((cp, VCARD.fn, Literal(contact.name)))
        g.add((cp, VCARD["organization-name"], Literal(contact.name)))
    if contact.organisation and contact.organisation != contact.name:
        g.add((cp, VCARD["organization-name"], Literal(contact.organisation)))
    if contact.email:
        email = contact.email.strip()
        if not email.startswith("mailto:"):
            email = f"mailto:{email}"
        email_node = BNode()
        g.add((email_node, RDF.type, VCARD.Email))
        g.add((email_node, RDF.value, _uri(email)))
        g.add((cp, VCARD.hasEmail, email_node))
    if contact.url:
        url_node = BNode()
        g.add((url_node, RDF.type, VCARD.URL))
        g.add((url_node, RDF.value, _uri(contact.url)))
        g.add((cp, VCARD.hasURL, url_node))
    if contact.phone:
        phone = contact.phone.strip()
        if not phone.startswith("tel:"):
            phone = f"tel:{phone}"
        tel_node = BNode()
        g.add((tel_node, RDF.type, VCARD.Voice))
        g.add((tel_node, RDF.value, _uri(phone)))
        g.add((cp, VCARD.hasTelephone, tel_node))
    g.add((dataset_uri, DCAT.contactPoint, cp))


def _add_publisher(g: Graph, meta: DatasetMetadata, dataset_uri: URIRef) -> None:
    """Add the publisher as a foaf:Agent (Release 5: includes publisherType and publisherNote)."""
    if meta.publisher_identifier and (
        meta.publisher_identifier.startswith("http://")
        or meta.publisher_identifier.startswith("https://")
    ):
        pub_uri: URIRef | BNode = _uri(meta.publisher_identifier)
    else:
        pub_uri = BNode()

    g.add((pub_uri, RDF.type, FOAF.Agent))
    g.add((pub_uri, FOAF.name, Literal(meta.publisher_name)))
    if meta.publisher_url:
        g.add((pub_uri, FOAF.homepage, _uri(meta.publisher_url)))
    # Release 5: publisherType (controlled vocabulary, use URI or label)
    if meta.publisher_type:
        pt = meta.publisher_type.strip()
        if pt.startswith("http://") or pt.startswith("https://"):
            g.add((pub_uri, HEALTHDCATAP.publisherType, _uri(pt)))
        else:
            g.add((pub_uri, HEALTHDCATAP.publisherType, Literal(pt)))
    # Release 5: publisherNote (free-text description of publisher scope/role)
    if meta.publisher_note:
        g.add((pub_uri, HEALTHDCATAP.publisherNote, Literal(meta.publisher_note)))
    g.add((dataset_uri, DCTERMS.publisher, pub_uri))


def _add_creator(g: Graph, meta: DatasetMetadata, dataset_uri: URIRef) -> None:
    """Add the creator as a foaf:Agent (if different from publisher)."""
    if not meta.creator_name:
        return
    if meta.creator_identifier and (
        meta.creator_identifier.startswith("http://")
        or meta.creator_identifier.startswith("https://")
    ):
        creator_uri: URIRef | BNode = _uri(meta.creator_identifier)
    else:
        creator_uri = BNode()

    g.add((creator_uri, RDF.type, FOAF.Agent))
    g.add((creator_uri, FOAF.name, Literal(meta.creator_name)))
    g.add((dataset_uri, DCTERMS.creator, creator_uri))


def _add_temporal_coverage(g: Graph, meta: DatasetMetadata, dataset_uri: URIRef) -> None:
    """Add temporal coverage as a dct:PeriodOfTime."""
    if not (meta.temporal_start or meta.temporal_end):
        return
    period = BNode()
    g.add((period, RDF.type, DCTERMS.PeriodOfTime))
    if meta.temporal_start:
        lit = _date_literal(meta.temporal_start)
        if lit:
            g.add((period, DCAT.startDate, lit))
    if meta.temporal_end:
        lit = _date_literal(meta.temporal_end)
        if lit:
            g.add((period, DCAT.endDate, lit))
    g.add((dataset_uri, DCTERMS.temporal, period))


def _add_distribution(
    g: Graph, dist: Distribution, dataset_uri: URIRef, index: int
) -> None:
    """Add a single distribution to the graph."""
    # Mint a URI for the distribution based on dataset URI
    dist_uri = URIRef(f"{dataset_uri}/distribution/{index}")
    g.add((dist_uri, RDF.type, DCAT.Distribution))

    if dist.title:
        g.add((dist_uri, DCTERMS.title, _lang_literal(dist.title)))
    if dist.description:
        g.add((dist_uri, DCTERMS.description, _lang_literal(dist.description)))

    # Access URL is mandatory in DCAT; use download_url as fallback
    access_url = dist.access_url or dist.download_url
    if access_url:
        g.add((dist_uri, DCAT.accessURL, _uri(access_url)))
    if dist.download_url:
        g.add((dist_uri, DCAT.downloadURL, _uri(dist.download_url)))

    if dist.format:
        fmt = dist.format.strip().upper()
        # Try EU NAL file type first; otherwise use as plain literal
        eu_fmt_uri = f"http://publications.europa.eu/resource/authority/file-type/{fmt}"
        g.add((dist_uri, DCTERMS["format"], _uri(eu_fmt_uri)))
        # Also add as dcat:mediaType if looks like IANA type
        if dist.media_type:
            g.add((dist_uri, DCAT.mediaType, _uri(
                f"https://www.iana.org/assignments/media-types/{dist.media_type}"
            )))
    elif dist.media_type:
        g.add((dist_uri, DCAT.mediaType, _uri(
            f"https://www.iana.org/assignments/media-types/{dist.media_type}"
        )))

    if dist.license:
        license_uri = resolve_license(dist.license)
        if license_uri:
            g.add((dist_uri, DCTERMS.license, _uri(license_uri)))
        else:
            g.add((dist_uri, DCTERMS.license, Literal(dist.license)))

    if dist.byte_size is not None:
        g.add((dist_uri, DCAT.byteSize, Literal(dist.byte_size, datatype=XSD.nonNegativeInteger)))

    if dist.issued:
        lit = _date_literal(dist.issued)
        if lit:
            g.add((dist_uri, DCTERMS.issued, lit))
    if dist.modified:
        lit = _date_literal(dist.modified)
        if lit:
            g.add((dist_uri, DCTERMS.modified, lit))
    if dist.rights:
        g.add((dist_uri, DCTERMS.rights, Literal(dist.rights)))
    if dist.conforms_to:
        for std in dist.conforms_to:
            if std.startswith("http://") or std.startswith("https://"):
                g.add((dist_uri, DCTERMS.conformsTo, _uri(std)))
            else:
                g.add((dist_uri, DCTERMS.conformsTo, Literal(std)))

    g.add((dataset_uri, DCAT.distribution, dist_uri))


def generate(meta: DatasetMetadata) -> str:
    """
    Generate a HealthDCAT-AP compliant RDF document from the given metadata.

    Returns the serialized RDF as a string in the requested output_format.
    """
    g = _build_graph()
    dataset_uri = _uri(meta.get_dataset_uri())

    # -------------------------------------------------------------------
    # Dataset type
    # -------------------------------------------------------------------
    g.add((dataset_uri, RDF.type, DCAT.Dataset))

    # -------------------------------------------------------------------
    # Mandatory properties
    # -------------------------------------------------------------------
    g.add((dataset_uri, DCTERMS.title, _lang_literal(meta.title)))
    g.add((dataset_uri, DCTERMS.description, _lang_literal(meta.description)))
    _add_publisher(g, meta, dataset_uri)

    # -------------------------------------------------------------------
    # HEAL theme is always required for health datasets
    # -------------------------------------------------------------------
    g.add((dataset_uri, DCAT.theme, _uri(f"{EU_DATA_THEME}HEAL")))

    # -------------------------------------------------------------------
    # Identification
    # -------------------------------------------------------------------
    if meta.identifier:
        g.add((dataset_uri, DCTERMS.identifier, Literal(meta.identifier)))

    if meta.landing_page:
        g.add((dataset_uri, DCAT.landingPage, _uri(meta.landing_page)))

    if meta.version:
        g.add((dataset_uri, OWL.versionInfo, Literal(meta.version)))
        g.add((dataset_uri, DCAT.version, Literal(meta.version)))

    # -------------------------------------------------------------------
    # Contact point (recommended)
    # -------------------------------------------------------------------
    if meta.contact_point:
        _add_contact_point(g, meta.contact_point, dataset_uri)

    # -------------------------------------------------------------------
    # Creator
    # -------------------------------------------------------------------
    _add_creator(g, meta, dataset_uri)

    # -------------------------------------------------------------------
    # Temporal metadata
    # -------------------------------------------------------------------
    if meta.issued:
        lit = _date_literal(meta.issued)
        if lit:
            g.add((dataset_uri, DCTERMS.issued, lit))

    if meta.modified:
        lit = _date_literal(meta.modified)
        if lit:
            g.add((dataset_uri, DCTERMS.modified, lit))

    _add_temporal_coverage(g, meta, dataset_uri)

    if meta.update_frequency:
        freq_uri = resolve_frequency(meta.update_frequency)
        g.add((dataset_uri, DCTERMS.accrualPeriodicity, _uri(freq_uri)))

    # -------------------------------------------------------------------
    # Spatial coverage
    # -------------------------------------------------------------------
    if meta.spatial_coverage:
        for location in meta.spatial_coverage:
            resolved = resolve_country(location)
            if resolved:
                g.add((dataset_uri, DCTERMS.spatial, _uri(resolved)))
            elif location.startswith("http://") or location.startswith("https://"):
                g.add((dataset_uri, DCTERMS.spatial, _uri(location)))
            else:
                # Unknown country: add as a labelled location node
                loc_node = BNode()
                g.add((loc_node, RDF.type, DCTERMS.Location))
                g.add((loc_node, RDFS.label, Literal(location)))
                g.add((dataset_uri, DCTERMS.spatial, loc_node))

    if meta.spatial_resolution:
        # Try to parse as numeric meters; otherwise use label
        try:
            meters = float(meta.spatial_resolution)
            g.add((
                dataset_uri,
                DCAT.spatialResolutionInMeters,
                Literal(meters, datatype=XSD.decimal),
            ))
        except ValueError:
            g.add((dataset_uri, DCAT.spatialResolutionInMeters, Literal(meta.spatial_resolution)))

    # -------------------------------------------------------------------
    # Keywords
    # -------------------------------------------------------------------
    if meta.keywords:
        for kw in meta.keywords:
            g.add((dataset_uri, DCAT.keyword, Literal(kw.strip())))

    # -------------------------------------------------------------------
    # Languages
    # -------------------------------------------------------------------
    if meta.language:
        for lang in meta.language:
            resolved = resolve_language(lang)
            if resolved:
                g.add((dataset_uri, DCTERMS.language, _uri(resolved)))
            elif lang.startswith("http://") or lang.startswith("https://"):
                g.add((dataset_uri, DCTERMS.language, _uri(lang)))
            else:
                g.add((dataset_uri, DCTERMS.language, Literal(lang)))

    # -------------------------------------------------------------------
    # Additional EU data themes
    # -------------------------------------------------------------------
    if meta.additional_themes:
        for theme in meta.additional_themes:
            resolved_uri = normalize_lookup(theme, EU_DATA_THEMES)
            if resolved_uri:
                g.add((dataset_uri, DCAT.theme, _uri(resolved_uri)))
            elif theme.startswith("http://") or theme.startswith("https://"):
                g.add((dataset_uri, DCAT.theme, _uri(theme)))

    # -------------------------------------------------------------------
    # Health categories
    # -------------------------------------------------------------------
    if meta.health_category:
        for cat in meta.health_category:
            cat_uri = resolve_health_category(cat)
            g.add((dataset_uri, HEALTHDCATAP.healthCategory, _uri(cat_uri)))

    # -------------------------------------------------------------------
    # Health themes
    # -------------------------------------------------------------------
    if meta.health_theme:
        for theme in meta.health_theme:
            resolved_ht = normalize_lookup(theme, HEALTH_THEMES)
            if resolved_ht:
                g.add((dataset_uri, HEALTHDCATAP.healthTheme, _uri(resolved_ht)))
            elif theme.startswith("http://") or theme.startswith("https://"):
                g.add((dataset_uri, HEALTHDCATAP.healthTheme, _uri(theme)))
            else:
                # Unknown theme: create a SKOS concept
                theme_node = BNode()
                g.add((theme_node, RDF.type, SKOS.Concept))
                g.add((theme_node, SKOS.prefLabel, Literal(theme)))
                g.add((dataset_uri, HEALTHDCATAP.healthTheme, theme_node))

    # -------------------------------------------------------------------
    # Coding systems
    # -------------------------------------------------------------------
    if meta.coding_systems:
        for cs in meta.coding_systems:
            cs_uri = resolve_coding_system(cs)
            if cs_uri.startswith("http://") or cs_uri.startswith("https://"):
                g.add((dataset_uri, HEALTHDCATAP.hasCodingSystem, _uri(cs_uri)))
            else:
                # Unknown system: add as a labelled node
                cs_node = BNode()
                g.add((cs_node, RDF.type, SKOS.ConceptScheme))
                g.add((cs_node, DCTERMS.title, Literal(cs)))
                g.add((dataset_uri, HEALTHDCATAP.hasCodingSystem, cs_node))

    # -------------------------------------------------------------------
    # Population statistics
    # -------------------------------------------------------------------
    if meta.min_age is not None:
        g.add((
            dataset_uri,
            HEALTHDCATAP.minTypicalAge,
            Literal(meta.min_age, datatype=XSD.nonNegativeInteger),
        ))
    if meta.max_age is not None:
        g.add((
            dataset_uri,
            HEALTHDCATAP.maxTypicalAge,
            Literal(meta.max_age, datatype=XSD.nonNegativeInteger),
        ))
    if meta.number_of_individuals is not None:
        g.add((
            dataset_uri,
            HEALTHDCATAP.numberOfUniqueIndividuals,
            Literal(meta.number_of_individuals, datatype=XSD.nonNegativeInteger),
        ))
    if meta.number_of_records is not None:
        g.add((
            dataset_uri,
            HEALTHDCATAP.numberOfRecords,
            Literal(meta.number_of_records, datatype=XSD.nonNegativeInteger),
        ))
    if meta.population_coverage:
        g.add((
            dataset_uri,
            HEALTHDCATAP.populationCoverage,
            Literal(meta.population_coverage),
        ))

    # -------------------------------------------------------------------
    # Legal & governance
    # -------------------------------------------------------------------
    if meta.access_rights:
        ar_uri = resolve_access_rights(meta.access_rights)
        g.add((dataset_uri, DCTERMS.accessRights, _uri(ar_uri)))

    if meta.license:
        license_uri = resolve_license(meta.license)
        if license_uri:
            g.add((dataset_uri, DCTERMS.license, _uri(license_uri)))
        else:
            g.add((dataset_uri, DCTERMS.license, Literal(meta.license)))

    # Release 5: legal basis uses dpv:hasLegalBasis (DPV namespace)
    if meta.legal_basis:
        lb = meta.legal_basis.strip()
        if lb.startswith("http://") or lb.startswith("https://"):
            g.add((dataset_uri, DPV.hasLegalBasis, _uri(lb)))
        else:
            g.add((dataset_uri, DPV.hasLegalBasis, Literal(lb)))

    # Release 5: personal data uses dpv:hasPersonalData (DPV namespace)
    if meta.personal_data_handling:
        g.add((dataset_uri, DPV.hasPersonalData, Literal(meta.personal_data_handling)))

    # Release 5: purpose uses dpv:hasPurpose (DPV namespace)
    if meta.purpose_of_collection:
        g.add((dataset_uri, DPV.hasPurpose, Literal(meta.purpose_of_collection)))

    if meta.retention_period:
        g.add((dataset_uri, HEALTHDCATAP.retentionPeriod, Literal(meta.retention_period)))

    # Release 5: Health Data Access Body (hdab) – the legally competent body for data access
    if meta.hdab_name:
        if meta.hdab_identifier and (
            meta.hdab_identifier.startswith("http://")
            or meta.hdab_identifier.startswith("https://")
        ):
            hdab_node: URIRef | BNode = _uri(meta.hdab_identifier)
        else:
            hdab_node = BNode()
        g.add((hdab_node, RDF.type, FOAF.Agent))
        g.add((hdab_node, FOAF.name, Literal(meta.hdab_name)))
        if meta.hdab_url:
            g.add((hdab_node, FOAF.homepage, _uri(meta.hdab_url)))
        g.add((dataset_uri, HEALTHDCATAP.hdab, hdab_node))

    # Release 5: publisher type and note (on the publisher agent node)
    # These are added in _add_publisher if provided; exposed here via dataset for simplicity

    # -------------------------------------------------------------------
    # Standards conformance
    # -------------------------------------------------------------------
    if meta.conforms_to:
        for std in meta.conforms_to:
            if std.startswith("http://") or std.startswith("https://"):
                g.add((dataset_uri, DCTERMS.conformsTo, _uri(std)))
            else:
                g.add((dataset_uri, DCTERMS.conformsTo, Literal(std)))

    # -------------------------------------------------------------------
    # Provenance
    # -------------------------------------------------------------------
    if meta.provenance:
        prov_node = BNode()
        g.add((prov_node, RDF.type, DCTERMS.ProvenanceStatement))
        g.add((prov_node, RDFS.label, Literal(meta.provenance)))
        g.add((dataset_uri, DCTERMS.provenance, prov_node))

    # -------------------------------------------------------------------
    # Related resources
    # -------------------------------------------------------------------
    if meta.related_resources:
        for rel in meta.related_resources:
            if rel.startswith("http://") or rel.startswith("https://"):
                g.add((dataset_uri, DCTERMS.relation, _uri(rel)))
            else:
                g.add((dataset_uri, DCTERMS.relation, Literal(rel)))

    if meta.is_part_of:
        if meta.is_part_of.startswith("http://") or meta.is_part_of.startswith("https://"):
            g.add((dataset_uri, DCTERMS.isPartOf, _uri(meta.is_part_of)))

    # -------------------------------------------------------------------
    # Distributions
    # -------------------------------------------------------------------
    if meta.distributions:
        for i, dist in enumerate(meta.distributions, start=1):
            _add_distribution(g, dist, dataset_uri, i)

    # -------------------------------------------------------------------
    # Additional properties (pass-through)
    # -------------------------------------------------------------------
    if meta.additional_properties:
        _add_additional_properties(g, meta.additional_properties, dataset_uri)

    # -------------------------------------------------------------------
    # Serialize
    # -------------------------------------------------------------------
    fmt_map = {
        "turtle": "turtle",
        "json-ld": "json-ld",
        "rdf/xml": "xml",
        "n-triples": "nt",
    }
    rdf_format = fmt_map.get(meta.output_format, "turtle")
    return g.serialize(format=rdf_format)


def _add_additional_properties(
    g: Graph, props: dict, subject: URIRef
) -> None:
    """Attempt to add additional key-value properties to the graph."""
    # Simple namespace prefix resolution
    known_ns = {
        "dct": str(DCTERMS),
        "dcterms": str(DCTERMS),
        "dcat": str(DCAT),
        "foaf": str(FOAF),
        "skos": str(SKOS),
        "healthdcatap": HEALTHDCATAP_NS,
        "schema": "http://schema.org/",
        "rdfs": str(RDFS),
        "owl": str(OWL),
    }
    for key, value in props.items():
        # Resolve predicate
        if key.startswith("http://") or key.startswith("https://"):
            pred = _uri(key)
        elif ":" in key:
            prefix, local = key.split(":", 1)
            ns_uri = known_ns.get(prefix.lower())
            if ns_uri:
                pred = _uri(f"{ns_uri}{local}")
            else:
                continue  # Skip unknown prefixes
        else:
            continue  # Skip bare names without prefix

        # Add value(s)
        if isinstance(value, list):
            values = value
        else:
            values = [value]

        for v in values:
            if isinstance(v, str):
                if v.startswith("http://") or v.startswith("https://"):
                    g.add((subject, pred, _uri(v)))
                else:
                    g.add((subject, pred, Literal(v)))
            elif isinstance(v, bool):
                g.add((subject, pred, Literal(v, datatype=XSD.boolean)))
            elif isinstance(v, int):
                g.add((subject, pred, Literal(v, datatype=XSD.integer)))
            elif isinstance(v, float):
                g.add((subject, pred, Literal(v, datatype=XSD.decimal)))
            elif isinstance(v, (datetime, date)):
                g.add((subject, pred, Literal(v.isoformat(), datatype=XSD.dateTime)))


def validate_turtle(turtle_str: str) -> tuple[bool, list[str]]:
    """
    Parse a Turtle RDF string and return basic validation results.

    Returns:
        (is_valid, list_of_issues)
    """
    issues: list[str] = []
    try:
        g = Graph()
        g.parse(data=turtle_str, format="turtle")
    except Exception as e:
        return False, [f"RDF parse error: {e}"]

    triple_count = len(g)
    if triple_count == 0:
        issues.append("Warning: Graph is empty (no triples found)")

    # Check for dcat:Dataset
    datasets = list(g.subjects(RDF.type, DCAT.Dataset))
    if not datasets:
        issues.append("Warning: No dcat:Dataset found in the graph")
    else:
        for ds in datasets:
            ds_uri = str(ds)
            # Check mandatory properties
            titles = list(g.objects(ds, DCTERMS.title))
            if not titles:
                issues.append(f"Missing dct:title on dataset <{ds_uri}>")

            descriptions = list(g.objects(ds, DCTERMS.description))
            if not descriptions:
                issues.append(f"Missing dct:description on dataset <{ds_uri}>")

            publishers = list(g.objects(ds, DCTERMS.publisher))
            if not publishers:
                issues.append(f"Missing dct:publisher on dataset <{ds_uri}>")

            # Check HEAL theme
            themes = [str(t) for t in g.objects(ds, DCAT.theme)]
            heal_theme = f"{EU_DATA_THEME}HEAL"
            if heal_theme not in themes:
                issues.append(
                    f"Missing mandatory dcat:theme <{heal_theme}> (HEAL) on dataset <{ds_uri}>"
                )

    return len(issues) == 0, issues
