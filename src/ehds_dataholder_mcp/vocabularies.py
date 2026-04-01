"""Controlled vocabularies and namespace mappings for HealthDCAT-AP."""

# ---------------------------------------------------------------------------
# Namespace URIs
# ---------------------------------------------------------------------------

HEALTHDCATAP_NS = "http://healthdataportal.eu/ns/health#"
DCAT_NS = "http://www.w3.org/ns/dcat#"
DCT_NS = "http://purl.org/dc/terms/"
FOAF_NS = "http://xmlns.com/foaf/0.1/"
VCARD_NS = "http://www.w3.org/2006/vcard/ns#"
SKOS_NS = "http://www.w3.org/2004/02/skos/core#"
XSD_NS = "http://www.w3.org/2001/XMLSchema#"
RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NS = "http://www.w3.org/2000/01/rdf-schema#"
OWL_NS = "http://www.w3.org/2002/07/owl#"
ADMS_NS = "http://www.w3.org/ns/adms#"
SPDX_NS = "http://spdx.org/rdf/terms#"
SCHEMA_NS = "http://schema.org/"
PROV_NS = "http://www.w3.org/ns/prov#"

# EU Named Authority List base URIs
EU_NAL_BASE = "http://publications.europa.eu/resource/authority/"
EU_ACCESS_RIGHT = f"{EU_NAL_BASE}access-right/"
EU_DATA_THEME = f"{EU_NAL_BASE}data-theme/"
EU_LANGUAGE = f"{EU_NAL_BASE}language/"
EU_COUNTRY = f"{EU_NAL_BASE}country/"
EU_FILE_TYPE = f"{EU_NAL_BASE}file-type/"
EU_FREQUENCY = f"{EU_NAL_BASE}frequency/"

# ---------------------------------------------------------------------------
# HealthDCAT-AP Health Categories
# Source: http://healthdataportal.eu/ns/health#
# ---------------------------------------------------------------------------

HEALTH_CATEGORIES: dict[str, str] = {
    "ehr": f"{HEALTHDCATAP_NS}ElectronicHealthRecord",
    "electronic health record": f"{HEALTHDCATAP_NS}ElectronicHealthRecord",
    "electronic health records": f"{HEALTHDCATAP_NS}ElectronicHealthRecord",
    "claims": f"{HEALTHDCATAP_NS}AdministrativeClaims",
    "claims data": f"{HEALTHDCATAP_NS}AdministrativeClaims",
    "administrative": f"{HEALTHDCATAP_NS}AdministrativeClaims",
    "administrative data": f"{HEALTHDCATAP_NS}AdministrativeClaims",
    "registry": f"{HEALTHDCATAP_NS}Registry",
    "patient registry": f"{HEALTHDCATAP_NS}PatientRegistry",
    "disease registry": f"{HEALTHDCATAP_NS}DiseaseRegistry",
    "population registry": f"{HEALTHDCATAP_NS}PopulationRegistry",
    "genomic": f"{HEALTHDCATAP_NS}GenomicData",
    "genomics": f"{HEALTHDCATAP_NS}GenomicData",
    "genomic data": f"{HEALTHDCATAP_NS}GenomicData",
    "biobank": f"{HEALTHDCATAP_NS}BiobankData",
    "biobank data": f"{HEALTHDCATAP_NS}BiobankData",
    "survey": f"{HEALTHDCATAP_NS}SurveyData",
    "questionnaire": f"{HEALTHDCATAP_NS}SurveyData",
    "survey data": f"{HEALTHDCATAP_NS}SurveyData",
    "imaging": f"{HEALTHDCATAP_NS}MedicalImaging",
    "medical imaging": f"{HEALTHDCATAP_NS}MedicalImaging",
    "wearable": f"{HEALTHDCATAP_NS}WearableData",
    "wearable data": f"{HEALTHDCATAP_NS}WearableData",
    "device data": f"{HEALTHDCATAP_NS}WearableData",
    "clinical trial": f"{HEALTHDCATAP_NS}ClinicalTrialData",
    "clinical trials": f"{HEALTHDCATAP_NS}ClinicalTrialData",
    "research cohort": f"{HEALTHDCATAP_NS}ResearchCohort",
    "cohort": f"{HEALTHDCATAP_NS}ResearchCohort",
    "environmental": f"{HEALTHDCATAP_NS}EnvironmentalHealth",
    "environmental health": f"{HEALTHDCATAP_NS}EnvironmentalHealth",
    "social care": f"{HEALTHDCATAP_NS}SocialCareData",
    "social care data": f"{HEALTHDCATAP_NS}SocialCareData",
    "public health": f"{HEALTHDCATAP_NS}PublicHealthData",
    "real world data": f"{HEALTHDCATAP_NS}RealWorldData",
    "rwd": f"{HEALTHDCATAP_NS}RealWorldData",
    "laboratory": f"{HEALTHDCATAP_NS}LaboratoryData",
    "lab data": f"{HEALTHDCATAP_NS}LaboratoryData",
    "prescription": f"{HEALTHDCATAP_NS}PrescriptionData",
    "medication": f"{HEALTHDCATAP_NS}PrescriptionData",
    "pharmacy": f"{HEALTHDCATAP_NS}PrescriptionData",
}

# ---------------------------------------------------------------------------
# Coding / Terminology Systems
# ---------------------------------------------------------------------------

CODING_SYSTEMS: dict[str, str] = {
    "icd-10": "http://id.who.int/icd/release/10",
    "icd10": "http://id.who.int/icd/release/10",
    "icd 10": "http://id.who.int/icd/release/10",
    "icd-11": "http://id.who.int/icd/release/11",
    "icd11": "http://id.who.int/icd/release/11",
    "icd 11": "http://id.who.int/icd/release/11",
    "snomed": "http://snomed.info/sct",
    "snomed ct": "http://snomed.info/sct",
    "snomed-ct": "http://snomed.info/sct",
    "snomedct": "http://snomed.info/sct",
    "loinc": "http://loinc.org",
    "atc": "http://www.whocc.no/atc",
    "atc classification": "http://www.whocc.no/atc",
    "rxnorm": "http://www.nlm.nih.gov/research/umls/rxnorm",
    "hpo": "http://purl.obolibrary.org/obo/hp.owl",
    "human phenotype ontology": "http://purl.obolibrary.org/obo/hp.owl",
    "omop": "https://www.ohdsi.org/data-standardization/",
    "omop cdm": "https://www.ohdsi.org/data-standardization/",
    "fhir": "http://hl7.org/fhir",
    "hl7 fhir": "http://hl7.org/fhir",
    "hl7": "http://www.hl7.org",
    "orphanet": "http://www.orpha.net/ontology/orphanet.owl",
    "orpha": "http://www.orpha.net/ontology/orphanet.owl",
    "mesh": "http://id.nlm.nih.gov/mesh",
    "meddra": "http://www.meddra.org",
    "ndc": "http://hl7.org/fhir/sid/ndc",
    "dkbog": "http://www.dk-bog.dk",
    "icd-o": "http://id.who.int/icd/release/o3",
    "read codes": "http://read.info",
    "read": "http://read.info",
    "cpt": "http://www.ama-assn.org/go/cpt",
    "drg": "http://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/MS-DRG-Classifications-and-Software.html",
    "nomen": "http://www.nomenclator.nl",
}

# ---------------------------------------------------------------------------
# Update Frequency (EU NAL Frequency)
# ---------------------------------------------------------------------------

UPDATE_FREQUENCIES: dict[str, str] = {
    "annual": f"{EU_FREQUENCY}ANNUAL",
    "annually": f"{EU_FREQUENCY}ANNUAL",
    "yearly": f"{EU_FREQUENCY}ANNUAL",
    "biennial": f"{EU_FREQUENCY}BIENNIAL",
    "every two years": f"{EU_FREQUENCY}BIENNIAL",
    "triennial": f"{EU_FREQUENCY}TRIENNIAL",
    "every three years": f"{EU_FREQUENCY}TRIENNIAL",
    "monthly": f"{EU_FREQUENCY}MONTHLY",
    "bimonthly": f"{EU_FREQUENCY}BIMONTHLY",
    "every two months": f"{EU_FREQUENCY}BIMONTHLY",
    "quarterly": f"{EU_FREQUENCY}QUARTERLY",
    "four times a year": f"{EU_FREQUENCY}QUARTERLY",
    "weekly": f"{EU_FREQUENCY}WEEKLY",
    "biweekly": f"{EU_FREQUENCY}BIWEEKLY",
    "every two weeks": f"{EU_FREQUENCY}BIWEEKLY",
    "semiweekly": f"{EU_FREQUENCY}SEMIWEEKLY",
    "twice a week": f"{EU_FREQUENCY}SEMIWEEKLY",
    "daily": f"{EU_FREQUENCY}DAILY",
    "semiannual": f"{EU_FREQUENCY}ANNUAL_2",
    "twice a year": f"{EU_FREQUENCY}ANNUAL_2",
    "semimonthly": f"{EU_FREQUENCY}SEMIMONTHLY",
    "twice a month": f"{EU_FREQUENCY}SEMIMONTHLY",
    "irregular": f"{EU_FREQUENCY}IRREGULAR",
    "continuous": f"{EU_FREQUENCY}CONT",
    "real-time": f"{EU_FREQUENCY}CONT",
    "realtime": f"{EU_FREQUENCY}CONT",
    "never": f"{EU_FREQUENCY}NEVER",
    "static": f"{EU_FREQUENCY}NEVER",
    "as needed": f"{EU_FREQUENCY}IRREG",
    "on demand": f"{EU_FREQUENCY}IRREG",
}

# ---------------------------------------------------------------------------
# Languages (ISO 639-1 / name -> EU NAL URI)
# ---------------------------------------------------------------------------

LANGUAGES: dict[str, str] = {
    "en": f"{EU_LANGUAGE}ENG",
    "eng": f"{EU_LANGUAGE}ENG",
    "english": f"{EU_LANGUAGE}ENG",
    "de": f"{EU_LANGUAGE}DEU",
    "deu": f"{EU_LANGUAGE}DEU",
    "ger": f"{EU_LANGUAGE}DEU",
    "german": f"{EU_LANGUAGE}DEU",
    "deutsch": f"{EU_LANGUAGE}DEU",
    "fr": f"{EU_LANGUAGE}FRA",
    "fra": f"{EU_LANGUAGE}FRA",
    "fre": f"{EU_LANGUAGE}FRA",
    "french": f"{EU_LANGUAGE}FRA",
    "nl": f"{EU_LANGUAGE}NLD",
    "nld": f"{EU_LANGUAGE}NLD",
    "dut": f"{EU_LANGUAGE}NLD",
    "dutch": f"{EU_LANGUAGE}NLD",
    "nederlands": f"{EU_LANGUAGE}NLD",
    "es": f"{EU_LANGUAGE}SPA",
    "spa": f"{EU_LANGUAGE}SPA",
    "spanish": f"{EU_LANGUAGE}SPA",
    "it": f"{EU_LANGUAGE}ITA",
    "ita": f"{EU_LANGUAGE}ITA",
    "italian": f"{EU_LANGUAGE}ITA",
    "pt": f"{EU_LANGUAGE}POR",
    "por": f"{EU_LANGUAGE}POR",
    "portuguese": f"{EU_LANGUAGE}POR",
    "sv": f"{EU_LANGUAGE}SWE",
    "swe": f"{EU_LANGUAGE}SWE",
    "swedish": f"{EU_LANGUAGE}SWE",
    "da": f"{EU_LANGUAGE}DAN",
    "dan": f"{EU_LANGUAGE}DAN",
    "danish": f"{EU_LANGUAGE}DAN",
    "fi": f"{EU_LANGUAGE}FIN",
    "fin": f"{EU_LANGUAGE}FIN",
    "finnish": f"{EU_LANGUAGE}FIN",
    "no": f"{EU_LANGUAGE}NOR",
    "nor": f"{EU_LANGUAGE}NOR",
    "norwegian": f"{EU_LANGUAGE}NOR",
    "pl": f"{EU_LANGUAGE}POL",
    "pol": f"{EU_LANGUAGE}POL",
    "polish": f"{EU_LANGUAGE}POL",
    "cs": f"{EU_LANGUAGE}CES",
    "ces": f"{EU_LANGUAGE}CES",
    "cze": f"{EU_LANGUAGE}CES",
    "czech": f"{EU_LANGUAGE}CES",
    "hu": f"{EU_LANGUAGE}HUN",
    "hun": f"{EU_LANGUAGE}HUN",
    "hungarian": f"{EU_LANGUAGE}HUN",
    "ro": f"{EU_LANGUAGE}RON",
    "ron": f"{EU_LANGUAGE}RON",
    "rum": f"{EU_LANGUAGE}RON",
    "romanian": f"{EU_LANGUAGE}RON",
    "el": f"{EU_LANGUAGE}ELL",
    "ell": f"{EU_LANGUAGE}ELL",
    "gre": f"{EU_LANGUAGE}ELL",
    "greek": f"{EU_LANGUAGE}ELL",
    "bg": f"{EU_LANGUAGE}BUL",
    "bul": f"{EU_LANGUAGE}BUL",
    "bulgarian": f"{EU_LANGUAGE}BUL",
    "hr": f"{EU_LANGUAGE}HRV",
    "hrv": f"{EU_LANGUAGE}HRV",
    "croatian": f"{EU_LANGUAGE}HRV",
    "sk": f"{EU_LANGUAGE}SLK",
    "slk": f"{EU_LANGUAGE}SLK",
    "slovak": f"{EU_LANGUAGE}SLK",
    "sl": f"{EU_LANGUAGE}SLV",
    "slv": f"{EU_LANGUAGE}SLV",
    "slovenian": f"{EU_LANGUAGE}SLV",
    "et": f"{EU_LANGUAGE}EST",
    "est": f"{EU_LANGUAGE}EST",
    "estonian": f"{EU_LANGUAGE}EST",
    "lv": f"{EU_LANGUAGE}LAV",
    "lav": f"{EU_LANGUAGE}LAV",
    "latvian": f"{EU_LANGUAGE}LAV",
    "lt": f"{EU_LANGUAGE}LIT",
    "lit": f"{EU_LANGUAGE}LIT",
    "lithuanian": f"{EU_LANGUAGE}LIT",
    "mt": f"{EU_LANGUAGE}MLT",
    "mlt": f"{EU_LANGUAGE}MLT",
    "maltese": f"{EU_LANGUAGE}MLT",
    "ga": f"{EU_LANGUAGE}GLE",
    "gle": f"{EU_LANGUAGE}GLE",
    "irish": f"{EU_LANGUAGE}GLE",
}

# ---------------------------------------------------------------------------
# Countries / Spatial Coverage (ISO 3166-1 alpha-2 / name -> EU NAL URI)
# ---------------------------------------------------------------------------

COUNTRIES: dict[str, str] = {
    "at": f"{EU_COUNTRY}AUT",
    "aut": f"{EU_COUNTRY}AUT",
    "austria": f"{EU_COUNTRY}AUT",
    "be": f"{EU_COUNTRY}BEL",
    "bel": f"{EU_COUNTRY}BEL",
    "belgium": f"{EU_COUNTRY}BEL",
    "bg": f"{EU_COUNTRY}BGR",
    "bgr": f"{EU_COUNTRY}BGR",
    "bulgaria": f"{EU_COUNTRY}BGR",
    "hr": f"{EU_COUNTRY}HRV",
    "hrv": f"{EU_COUNTRY}HRV",
    "croatia": f"{EU_COUNTRY}HRV",
    "cy": f"{EU_COUNTRY}CYP",
    "cyp": f"{EU_COUNTRY}CYP",
    "cyprus": f"{EU_COUNTRY}CYP",
    "cz": f"{EU_COUNTRY}CZE",
    "cze": f"{EU_COUNTRY}CZE",
    "czech republic": f"{EU_COUNTRY}CZE",
    "czechia": f"{EU_COUNTRY}CZE",
    "dk": f"{EU_COUNTRY}DNK",
    "dnk": f"{EU_COUNTRY}DNK",
    "denmark": f"{EU_COUNTRY}DNK",
    "ee": f"{EU_COUNTRY}EST",
    "est": f"{EU_COUNTRY}EST",
    "estonia": f"{EU_COUNTRY}EST",
    "fi": f"{EU_COUNTRY}FIN",
    "fin": f"{EU_COUNTRY}FIN",
    "finland": f"{EU_COUNTRY}FIN",
    "fr": f"{EU_COUNTRY}FRA",
    "fra": f"{EU_COUNTRY}FRA",
    "france": f"{EU_COUNTRY}FRA",
    "de": f"{EU_COUNTRY}DEU",
    "deu": f"{EU_COUNTRY}DEU",
    "germany": f"{EU_COUNTRY}DEU",
    "deutschland": f"{EU_COUNTRY}DEU",
    "gr": f"{EU_COUNTRY}GRC",
    "grc": f"{EU_COUNTRY}GRC",
    "greece": f"{EU_COUNTRY}GRC",
    "hu": f"{EU_COUNTRY}HUN",
    "hun": f"{EU_COUNTRY}HUN",
    "hungary": f"{EU_COUNTRY}HUN",
    "ie": f"{EU_COUNTRY}IRL",
    "irl": f"{EU_COUNTRY}IRL",
    "ireland": f"{EU_COUNTRY}IRL",
    "it": f"{EU_COUNTRY}ITA",
    "ita": f"{EU_COUNTRY}ITA",
    "italy": f"{EU_COUNTRY}ITA",
    "lv": f"{EU_COUNTRY}LVA",
    "lva": f"{EU_COUNTRY}LVA",
    "latvia": f"{EU_COUNTRY}LVA",
    "lt": f"{EU_COUNTRY}LTU",
    "ltu": f"{EU_COUNTRY}LTU",
    "lithuania": f"{EU_COUNTRY}LTU",
    "lu": f"{EU_COUNTRY}LUX",
    "lux": f"{EU_COUNTRY}LUX",
    "luxembourg": f"{EU_COUNTRY}LUX",
    "mt": f"{EU_COUNTRY}MLT",
    "mlt": f"{EU_COUNTRY}MLT",
    "malta": f"{EU_COUNTRY}MLT",
    "nl": f"{EU_COUNTRY}NLD",
    "nld": f"{EU_COUNTRY}NLD",
    "netherlands": f"{EU_COUNTRY}NLD",
    "the netherlands": f"{EU_COUNTRY}NLD",
    "no": f"{EU_COUNTRY}NOR",
    "nor": f"{EU_COUNTRY}NOR",
    "norway": f"{EU_COUNTRY}NOR",
    "pl": f"{EU_COUNTRY}POL",
    "pol": f"{EU_COUNTRY}POL",
    "poland": f"{EU_COUNTRY}POL",
    "pt": f"{EU_COUNTRY}PRT",
    "prt": f"{EU_COUNTRY}PRT",
    "portugal": f"{EU_COUNTRY}PRT",
    "ro": f"{EU_COUNTRY}ROU",
    "rou": f"{EU_COUNTRY}ROU",
    "romania": f"{EU_COUNTRY}ROU",
    "sk": f"{EU_COUNTRY}SVK",
    "svk": f"{EU_COUNTRY}SVK",
    "slovakia": f"{EU_COUNTRY}SVK",
    "sl": f"{EU_COUNTRY}SVN",
    "si": f"{EU_COUNTRY}SVN",
    "svn": f"{EU_COUNTRY}SVN",
    "slovenia": f"{EU_COUNTRY}SVN",
    "es": f"{EU_COUNTRY}ESP",
    "esp": f"{EU_COUNTRY}ESP",
    "spain": f"{EU_COUNTRY}ESP",
    "se": f"{EU_COUNTRY}SWE",
    "swe": f"{EU_COUNTRY}SWE",
    "sweden": f"{EU_COUNTRY}SWE",
    "ch": f"{EU_COUNTRY}CHE",
    "che": f"{EU_COUNTRY}CHE",
    "switzerland": f"{EU_COUNTRY}CHE",
    "gb": f"{EU_COUNTRY}GBR",
    "gbr": f"{EU_COUNTRY}GBR",
    "uk": f"{EU_COUNTRY}GBR",
    "united kingdom": f"{EU_COUNTRY}GBR",
    "is": f"{EU_COUNTRY}ISL",
    "isl": f"{EU_COUNTRY}ISL",
    "iceland": f"{EU_COUNTRY}ISL",
    "eu": "http://publications.europa.eu/resource/authority/continent/EUROPE",
    "europe": "http://publications.europa.eu/resource/authority/continent/EUROPE",
    "european union": "http://publications.europa.eu/resource/authority/continent/EUROPE",
}

# ---------------------------------------------------------------------------
# Access Rights (EU NAL)
# ---------------------------------------------------------------------------

ACCESS_RIGHTS: dict[str, str] = {
    "public": f"{EU_ACCESS_RIGHT}PUBLIC",
    "open": f"{EU_ACCESS_RIGHT}PUBLIC",
    "open access": f"{EU_ACCESS_RIGHT}PUBLIC",
    "restricted": f"{EU_ACCESS_RIGHT}RESTRICTED",
    "restricted access": f"{EU_ACCESS_RIGHT}RESTRICTED",
    "non-public": f"{EU_ACCESS_RIGHT}NON_PUBLIC",
    "non public": f"{EU_ACCESS_RIGHT}NON_PUBLIC",
    "private": f"{EU_ACCESS_RIGHT}NON_PUBLIC",
    "sensitive": f"{EU_ACCESS_RIGHT}NON_PUBLIC",
    "confidential": f"{EU_ACCESS_RIGHT}NON_PUBLIC",
}

# ---------------------------------------------------------------------------
# Common Open Licenses
# ---------------------------------------------------------------------------

LICENSES: dict[str, str] = {
    "cc0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "cc0 1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "public domain": "https://creativecommons.org/publicdomain/zero/1.0/",
    "cc by": "https://creativecommons.org/licenses/by/4.0/",
    "cc by 4.0": "https://creativecommons.org/licenses/by/4.0/",
    "cc-by-4.0": "https://creativecommons.org/licenses/by/4.0/",
    "cc by sa": "https://creativecommons.org/licenses/by-sa/4.0/",
    "cc by sa 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "cc-by-sa-4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "cc by nc": "https://creativecommons.org/licenses/by-nc/4.0/",
    "cc by nc 4.0": "https://creativecommons.org/licenses/by-nc/4.0/",
    "mit": "https://opensource.org/licenses/MIT",
    "apache 2.0": "https://www.apache.org/licenses/LICENSE-2.0",
    "apache2": "https://www.apache.org/licenses/LICENSE-2.0",
    "proprietary": f"{EU_ACCESS_RIGHT}NON_PUBLIC",
    "not specified": "",
}

# ---------------------------------------------------------------------------
# EU Data Themes (fixed code: HEAL required for all health datasets)
# ---------------------------------------------------------------------------

EU_DATA_THEMES: dict[str, str] = {
    "health": f"{EU_DATA_THEME}HEAL",
    "heal": f"{EU_DATA_THEME}HEAL",
    "science": f"{EU_DATA_THEME}TECH",
    "technology": f"{EU_DATA_THEME}TECH",
    "education": f"{EU_DATA_THEME}EDUC",
    "society": f"{EU_DATA_THEME}SOCI",
    "population": f"{EU_DATA_THEME}SOCI",
    "environment": f"{EU_DATA_THEME}ENVI",
    "government": f"{EU_DATA_THEME}GOVE",
    "economy": f"{EU_DATA_THEME}ECON",
    "agriculture": f"{EU_DATA_THEME}AGRI",
    "energy": f"{EU_DATA_THEME}ENER",
    "transport": f"{EU_DATA_THEME}TRAN",
    "regions": f"{EU_DATA_THEME}REGI",
    "justice": f"{EU_DATA_THEME}JUST",
    "international": f"{EU_DATA_THEME}INTR",
}

# Health data themes (HealthDCAT-AP specific concepts / SNOMED/ICD groupings)
HEALTH_THEMES: dict[str, str] = {
    "cancer": f"{HEALTHDCATAP_NS}Cancer",
    "oncology": f"{HEALTHDCATAP_NS}Cancer",
    "cardiovascular": f"{HEALTHDCATAP_NS}CardiovascularDisease",
    "heart disease": f"{HEALTHDCATAP_NS}CardiovascularDisease",
    "cardiology": f"{HEALTHDCATAP_NS}CardiovascularDisease",
    "mental health": f"{HEALTHDCATAP_NS}MentalHealth",
    "psychiatry": f"{HEALTHDCATAP_NS}MentalHealth",
    "neurology": f"{HEALTHDCATAP_NS}NeurologicalDisease",
    "neurological": f"{HEALTHDCATAP_NS}NeurologicalDisease",
    "diabetes": f"{HEALTHDCATAP_NS}Diabetes",
    "endocrinology": f"{HEALTHDCATAP_NS}EndocrineDisease",
    "respiratory": f"{HEALTHDCATAP_NS}RespiratoryDisease",
    "pulmonology": f"{HEALTHDCATAP_NS}RespiratoryDisease",
    "infectious disease": f"{HEALTHDCATAP_NS}InfectiousDisease",
    "infectious": f"{HEALTHDCATAP_NS}InfectiousDisease",
    "rare disease": f"{HEALTHDCATAP_NS}RareDisease",
    "rare diseases": f"{HEALTHDCATAP_NS}RareDisease",
    "paediatrics": f"{HEALTHDCATAP_NS}Paediatrics",
    "pediatrics": f"{HEALTHDCATAP_NS}Paediatrics",
    "geriatrics": f"{HEALTHDCATAP_NS}Geriatrics",
    "elderly": f"{HEALTHDCATAP_NS}Geriatrics",
    "maternal health": f"{HEALTHDCATAP_NS}MaternalHealth",
    "obstetrics": f"{HEALTHDCATAP_NS}MaternalHealth",
    "pharmacy": f"{HEALTHDCATAP_NS}Pharmacy",
    "medication": f"{HEALTHDCATAP_NS}Pharmacy",
    "pharmacology": f"{HEALTHDCATAP_NS}Pharmacy",
    "surgery": f"{HEALTHDCATAP_NS}Surgery",
    "orthopedics": f"{HEALTHDCATAP_NS}Musculoskeletal",
    "musculoskeletal": f"{HEALTHDCATAP_NS}Musculoskeletal",
    "dermatology": f"{HEALTHDCATAP_NS}Dermatology",
    "skin": f"{HEALTHDCATAP_NS}Dermatology",
    "ophthalmology": f"{HEALTHDCATAP_NS}Ophthalmology",
    "eye": f"{HEALTHDCATAP_NS}Ophthalmology",
    "dental": f"{HEALTHDCATAP_NS}Dental",
    "dentistry": f"{HEALTHDCATAP_NS}Dental",
    "genomics": f"{HEALTHDCATAP_NS}GenomicsTheme",
    "genetics": f"{HEALTHDCATAP_NS}GenomicsTheme",
    "immunology": f"{HEALTHDCATAP_NS}Immunology",
    "allergy": f"{HEALTHDCATAP_NS}Immunology",
    "rheumatology": f"{HEALTHDCATAP_NS}Rheumatology",
    "gastroenterology": f"{HEALTHDCATAP_NS}Gastroenterology",
    "nephrology": f"{HEALTHDCATAP_NS}Nephrology",
    "kidney": f"{HEALTHDCATAP_NS}Nephrology",
    "urology": f"{HEALTHDCATAP_NS}Urology",
    "gynaecology": f"{HEALTHDCATAP_NS}Gynaecology",
    "gynecology": f"{HEALTHDCATAP_NS}Gynaecology",
    "haematology": f"{HEALTHDCATAP_NS}Haematology",
    "hematology": f"{HEALTHDCATAP_NS}Haematology",
    "blood": f"{HEALTHDCATAP_NS}Haematology",
    "covid": f"{HEALTHDCATAP_NS}COVID19",
    "covid-19": f"{HEALTHDCATAP_NS}COVID19",
    "coronavirus": f"{HEALTHDCATAP_NS}COVID19",
}


def normalize_lookup(value: str, mapping: dict[str, str]) -> str | None:
    """Look up a value in a mapping, normalizing case and whitespace."""
    key = value.strip().lower()
    return mapping.get(key)


def resolve_health_category(value: str) -> str:
    """Resolve a health category string to a URI, returning the original if unknown."""
    uri = normalize_lookup(value, HEALTH_CATEGORIES)
    if uri:
        return uri
    # If already looks like a URI, pass through
    if value.startswith("http://") or value.startswith("https://"):
        return value
    # Fall back: construct a local URI
    slug = value.strip().replace(" ", "_").replace("-", "_")
    return f"{HEALTHDCATAP_NS}{slug}"


def resolve_coding_system(value: str) -> str:
    """Resolve a coding system name to a URI."""
    uri = normalize_lookup(value, CODING_SYSTEMS)
    if uri:
        return uri
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return value  # Return as-is (will be used as literal label)


def resolve_language(value: str) -> str | None:
    """Resolve a language code/name to an EU NAL URI."""
    return normalize_lookup(value, LANGUAGES)


def resolve_country(value: str) -> str | None:
    """Resolve a country code/name to an EU NAL URI."""
    return normalize_lookup(value, COUNTRIES)


def resolve_access_rights(value: str) -> str:
    """Resolve access rights string to EU NAL URI."""
    uri = normalize_lookup(value, ACCESS_RIGHTS)
    return uri or f"{EU_ACCESS_RIGHT}{value.upper()}"


def resolve_frequency(value: str) -> str:
    """Resolve update frequency string to EU NAL URI."""
    uri = normalize_lookup(value, UPDATE_FREQUENCIES)
    if uri:
        return uri
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return f"{EU_FREQUENCY}{value.upper()}"


def resolve_license(value: str) -> str:
    """Resolve license string to URI."""
    uri = normalize_lookup(value, LICENSES)
    if uri is not None and uri != "":
        return uri
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return value
