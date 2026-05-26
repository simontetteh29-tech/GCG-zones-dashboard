import streamlit as st
import geopandas as gpd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Ghana Operational Zones Dashboard",
    layout="wide"
)

st.title("GCG Operational Zonal Offices Dashboard")

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    gdf = gpd.read_file("gadm41_GHA_2.json.zip")
    return gdf.to_crs(epsg=4326)

gdf = load_data()

REGION_COL = "NAME_1"
DISTRICT_COL = "NAME_2"

# ==================================================
# CLEAN REGION NAMES
# ==================================================
gdf["REGION_CLEAN"] = (
    gdf[REGION_COL]
    .astype(str)
    .str.replace("-", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.strip()
)

# ==================================================
# CLEAN DISTRICT NAMES
# ==================================================
gdf["DISTRICT_CLEAN"] = (
    gdf[DISTRICT_COL]
    .astype(str)
    .str.replace(" Metropolitan", "", regex=False)
    .str.replace(" Municipal", "", regex=False)
    .str.replace(" District", "", regex=False)
    .str.replace("-", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.strip()
)

# ==================================================
# INITIALIZE ZONE
# ==================================================
gdf["ZONE"] = None

# ==================================================
# REGION → ZONE MAPPING
# ==================================================
region_zone_mapping = {
    "Northern": "Tamale",
    "NorthEast": "Tamale",
    "Savannah": "Tamale",
    "UpperEast": "Tamale",
    "UpperWest": "Tamale",

    "Volta": "Ho",
    "Oti": "Ho",

    "Western": "Sefwi",
    "WesternNorth": "Sefwi",

    "BonoEast": "Kumasi",

    "Bono": "Bekwai",
    "Ahafo": "Bekwai",
}

gdf["ZONE"] = gdf["REGION_CLEAN"].map(region_zone_mapping)

# ==================================================
# DISTRICT → ZONE MAPPING
# ==================================================
district_zone_mapping = {
    # KASOA ZONE
    "AwutuSenyaEast": "Kasoa",
    "AwutuSenyaWest": "Kasoa",
    "GomoaEast": "Kasoa",
    "Effutu": "Kasoa",
    "GomoaWest": "Kasoa",
    "GomoaCentral": "Kasoa",
    "GaSouth": "Kasoa",
    "WeijaGbawe": "Kasoa",

    # SWEDRU ZONE
    "AgonaWest": "Swedru",
    "AgonaEast": "Swedru",
    "AsikumaOdobenBrakwa": "Swedru",
    "AjumakoEnyanEssiam": "Swedru",
    "CapeCoast": "Swedru",
    "Ekumfi": "Swedru",
    "AburaAsebuKwamankese": "Swedru",
    "AssinSouth": "Swedru",
    "AssinCentral": "Swedru",
    "AssinNorth": "Swedru",
    "UpperDenkyiraEast": "Swedru",
    "UpperDenkyiraWest": "Swedru",
    "TwifoAttiMorkwa": "Swedru",
    "TwifoHemangLowerDenkyira": "Swedru",
    "Mfantseman": "Swedru",
    "KomendaEdinaEguafoAbirem": "Swedru",

    # ACCRA ZONE
    "Accra": "Accra",
    "AblekumaCentral": "Accra",
    "AblekumaNorth": "Accra",
    "AblekumaWest": "Accra",
    "Adenta": "Accra",
    "Ashaiman": "Accra",
    "AyawasoCentral": "Accra",
    "AyawasoEast": "Accra",
    "AyawasoNorth": "Accra",
    "AyawasoWest": "Accra",
    "GaCentral": "Accra",
    "GaEast": "Accra",
    "GaNorth": "Accra",
    "GaWest": "Accra",
    "KponeKatamanso": "Accra",
    "Krowor": "Accra",
    "LaDadeKotopon": "Accra",
    "LaNkwantanangMadina": "Accra",
    "Ledzokuku": "Accra",
    "NingoPrampram": "Accra",
    "OkaikweiNorth": "Accra",
    "ShaiOsudoku": "Accra",
    "Tema": "Accra",
    "TemaWest": "Accra",
    "KorleKlottey": "Accra",
    "AdaEast": "Accra",
    "AdaWest": "Accra",

    # KUMASI ZONE
    "Kumasi": "Kumasi",
    "Kwadaso": "Kumasi",
    "OldTafo": "Kumasi",
    "AsokoreMampong": "Kumasi",
    "Asokwa": "Kumasi",
    "Suame": "Kumasi",
    "Oforikrom": "Kumasi",
    "AtwimaKwanwoma": "Kumasi",
    "KwabreEast": "Kumasi",
    "AfigyaKwabreSouth": "Kumasi",
    "AtwimaNwabiagyaSouth": "Kumasi",
    "AtwimaNwabiagyaNorth": "Kumasi",
    "Ejisu": "Kumasi",
    "Juaben": "Kumasi",
    "SekyereEast": "Kumasi",
    "SekyereSouth": "Kumasi",
    "AfigyaKwabreNorth": "Kumasi",
    "AhafoAnoSouthEast": "Kumasi",
    "Offinso": "Kumasi",
    "Mampong": "Kumasi",
    "OffinsoNorth": "Kumasi",
    "SekyereCentral": "Kumasi",
    "EjuraSekyedumase": "Kumasi",
    "SekyereAframPlainsNorth": "Kumasi",
    "SekyereKumawu": "Kumasi",

    # BEKWAI ZONE
    "Bosomtwe": "Bekwai",
    "Bekwai": "Bekwai",
    "AmansieWest": "Bekwai",
    "AdansiNorth": "Bekwai",
    "AsanteAkimCentral": "Bekwai",
    "BosomeFreho": "Bekwai",
    "Obuasi": "Bekwai",
    "AhafoAnoSouthWest": "Bekwai",
    "AmansieCentral": "Bekwai",
    "ObuasiEast": "Bekwai",
    "AtwimaMponua": "Bekwai",
    "AmansieSouth": "Bekwai",
    "AsanteAkimSouth": "Bekwai",
    "AdansiAsokwa": "Bekwai",
    "AhafoAnoNorth": "Bekwai",
    "AsanteAkimNorth": "Bekwai",
    "AdansiAkrofuom": "Bekwai",
    "AdansiSouth": "Bekwai",
}

district_map = gdf["DISTRICT_CLEAN"].map(district_zone_mapping)
gdf["ZONE"] = gdf["ZONE"].fillna(district_map)

# ==================================================
# 🔥 EASTERN REGION OVERRIDE RULES
# ==================================================
swedru_eastern_districts = {
    "UpperWestAkim",
    "WestAkim",
    "Ayensuano",
    "Achiase",
    "AseneMansoAkroso",
    "BirimSouth",
    "Kwabirimdistrict",
    "BirimCentralMunicipal"
}

eastern_mask = gdf["REGION_CLEAN"] == "Eastern"

# Assign selected → Swedru
gdf.loc[
    eastern_mask & gdf["DISTRICT_CLEAN"].isin(swedru_eastern_districts),
    "ZONE"
] = "Swedru"

# Remaining Eastern → Accra
gdf.loc[
    eastern_mask & ~gdf["DISTRICT_CLEAN"].isin(swedru_eastern_districts),
    "ZONE"
] = "Accra"

# ==================================================
# FINAL CLEANUP
# ==================================================
gdf["ZONE"] = gdf["ZONE"].fillna("Unassigned")

# ==================================================
# SIDEBAR FILTER
# ==================================================
st.sidebar.header("Filters")

zones = ["All Zones"] + sorted(gdf["ZONE"].unique())

selected_zone = st.sidebar.selectbox("Select Zone", zones)

filtered = gdf if selected_zone == "All Zones" else gdf[gdf["ZONE"] == selected_zone]

# ==================================================
# KPI METRICS
# ==================================================
c1, c2, c3 = st.columns(3)

c1.metric("Total Districts", len(gdf))
c2.metric("Mapped Districts", len(gdf[gdf["ZONE"] != "Unassigned"]))
c3.metric("Zones", gdf[gdf["ZONE"] != "Unassigned"]["ZONE"].nunique())

# ==================================================
# MAP
# ==================================================
fig = px.choropleth(
    filtered,
    geojson=filtered.__geo_interface__,
    locations=filtered.index,
    color="ZONE",
    hover_name=DISTRICT_COL,
    hover_data=[REGION_COL],
    projection="mercator"
)

fig.update_geos(fitbounds="locations", visible=False)

fig.update_traces(marker_line_width=0.5, marker_line_color="black")

fig.update_layout(height=850, margin=dict(l=0, r=0, t=0, b=0))

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TABLE
# ==================================================
st.subheader("District Zone Assignment")

st.dataframe(
    filtered[[DISTRICT_COL, REGION_COL, "ZONE"]].sort_values(["ZONE", DISTRICT_COL]),
    use_container_width=True
)

# ==================================================
# UNASSIGNED
# ==================================================
unassigned = gdf[gdf["ZONE"] == "Unassigned"]

if len(unassigned) > 0:
    st.warning(f"{len(unassigned)} districts remain unassigned")
    st.dataframe(unassigned[[DISTRICT_COL, REGION_COL]], use_container_width=True)
else:
    st.success("All districts successfully assigned!")
