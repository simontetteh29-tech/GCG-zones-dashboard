import streamlit as st
import geopandas as gpd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="GCG Operational Zones Dashboard",
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
# SIDEBAR CONFIG & MAP VERSION TOGGLE
# ==================================================
st.sidebar.header("Map Configurations")
map_version = st.sidebar.radio("Select Map Version", ["Old Map", "New Map"])

# ==================================================
# INITIALIZE ZONE BOUNDARIES BASED ON SELECTION
# ==================================================
gdf["ZONE"] = None

if map_version == "Old Map":
    # --- OLD MAP REGIONAL DEFINITIONS ---
    # Tamale stays as standard tamale configuration
    # Ashanti, Bono, Ahafo, BonoEast -> Kumasi zone
    # Eastern, GreaterAccra, Oti, Volta -> Accra zone
    # Central, Western, WesternNorth -> Kasoa zone
    region_zone_mapping = {
        "Northern": "Tamale",
        "NorthEast": "Tamale",
        "Savannah": "Tamale",
        "UpperEast": "Tamale",
        "UpperWest": "Tamale",
        
        "Ashanti": "Kumasi",
        "Bono": "Kumasi",
        "Ahafo": "Kumasi",
        "BonoEast": "Kumasi",
        
        "Eastern": "Accra",
        "GreaterAccra": "Accra",
        "Oti": "Accra",
        "Volta": "Accra",
        
        "Central": "Kasoa",
        "Western": "Kasoa",
        "WesternNorth": "Kasoa"
    }
    gdf["ZONE"] = gdf["REGION_CLEAN"].map(region_zone_mapping)

else:
    # --- NEW MAP REGIONAL DEFINITIONS ---
    # UpperWest & Savannah -> Question Map zone
    # UpperEast, NorthEast & Northern -> Tamale zone
    # Oti and Volta demarcated together as Ho zone
    region_zone_mapping = {
        "UpperWest": "Proposed Zone",
        "Savannah": "Proposed Zone",
        
        "UpperEast": "Tamale",
        "NorthEast": "Tamale",
        "Northern": "Tamale",
        
        "Volta": "Ho",
        "Oti": "Ho"
    }
    gdf["ZONE"] = gdf["REGION_CLEAN"].map(region_zone_mapping)
    
    # --- NEW MAP DISTRICT LEVEL BREAKDOWNS ---
    # Maintain current Bekwai & Kumasi demarcation
    # Maintain current Accra zone
    # Maintain current Kasoa, Sefwi and Swedru demarcations
    district_zone_mapping = {
        # Kasoa
        "AwutuSenyaEast": "Kasoa", "AwutuSenyaWest": "Kasoa", "GomoaEast": "Kasoa", "Effutu": "Kasoa", 
        "GomoaWest": "Kasoa", "GomoaCentral": "Kasoa", "Ekumfi": "Kasoa","Mfantseman": "Kasoa", 
        "AburaAsebuKwamankese": "Kasoa", "KomendaEdinaEguafoAbirem": "Kasoa", "CapeCoast": "Kasoa",
        "GaSouth": "Kasoa", "WeijaGbawe": "Kasoa",

        # Swedru
        "AgonaWest": "Swedru", "AgonaEast": "Swedru", "AsikumaOdobenBrakwa": "Swedru", 
        "AjumakoEnyanEssiam": "Swedru", "AssinSouth": "Swedru", "AssinCentral": "Swedru", 
        "AssinNorth": "Swedru", "UpperDenkyiraEast": "Swedru", "UpperDenkyiraWest": "Swedru", 
        "TwifoAttiMorkwa": "Swedru", "TwifoHemangLowerDenkyira": "Swedru",  
        

        # Accra
        "Accra": "Accra", "AblekumaCentral": "Accra", "AblekumaNorth": "Accra", 
        "AblekumaWest": "Accra", "Adenta": "Accra", "Ashaiman": "Accra", 
        "AyawasoCentral": "Accra", "AyawasoEast": "Accra", "AyawasoNorth": "Accra", 
        "AyawasoWest": "Accra", "GaCentral": "Accra", "GaEast": "Accra", 
        "GaNorth": "Accra", "GaWest": "Accra", "KponeKatamanso": "Accra", 
        "Krowor": "Accra", "LaDadeKotopon": "Accra", "LaNkwantanangMadina": "Accra", 
        "Ledzokuku": "Accra", "NingoPrampram": "Accra", "OkaikweiNorth": "Accra", 
        "ShaiOsudoku": "Accra", "Tema": "Accra", "TemaWest": "Accra", 
        "KorleKlottey": "Accra", "AdaEast": "Accra", "AdaWest": "Accra",

        # Kumasi
        "Kumasi": "Kumasi", "Kwadaso": "Kumasi", "OldTafo": "Kumasi", 
        "AsokoreMampong": "Kumasi", "Asokwa": "Kumasi", "Suame": "Kumasi", 
        "Oforikrom": "Kumasi", "AsanteAkimNorth": "Kumasi", "KwabreEast": "Kumasi", 
        "AfigyaKwabreSouth": "Kumasi", "AsanteAkimSouth": "Kumasi", "Ejisu": "Kumasi", 
        "Juaben": "Kumasi", "SekyereEast": "Kumasi", "SekyereSouth": "Kumasi", 
        "AfigyaKwabreNorth": "Kumasi", "AsanteAkimCentral": "Kumasi", "Offinso": "Kumasi", 
        "Mampong": "Kumasi", "OffinsoNorth": "Kumasi", "SekyereCentral": "Kumasi", 
        "EjuraSekyedumase": "Kumasi", "SekyereAframPlainsNorth": "Kumasi", "SekyereKumawu": "Kumasi",

        # Bekwai
        "Bosomtwe": "Bekwai", "Bekwai": "Bekwai", "AmansieWest": "Bekwai", 
        "AdansiNorth": "Bekwai", "AhafoAnoSouthEast": "Bekwai", "BosomeFreho": "Bekwai", 
        "Obuasi": "Bekwai", "AhafoAnoSouthWest": "Bekwai", "AmansieCentral": "Bekwai", 
        "ObuasiEast": "Bekwai", "AtwimaMponua": "Bekwai", "AmansieSouth": "Bekwai", 
        "AtwimaNwabiagyaNorth": "Bekwai", "AtwimaNwabiagyaSouth": "Bekwai", "AdansiAsokwa": "Bekwai", 
        "AhafoAnoNorth": "Bekwai", "AtwimaKwanwoma": "Bekwai", "AdansiAkrofuom": "Bekwai", 
        "AdansiSouth": "Bekwai",
    }
    
    district_map = gdf["DISTRICT_CLEAN"].map(district_zone_mapping)
    gdf["ZONE"] = gdf["ZONE"].fillna(district_map)

    # ==================================================
    # NEW MAP REGIONAL ASSIGNMENTS
    # ==================================================

    # Bono Region -> Bekwai
    gdf.loc[gdf["REGION_CLEAN"] == "Bono", "ZONE"] = "Bekwai"

    # Eastern Region -> Accra
    gdf.loc[gdf["REGION_CLEAN"] == "Eastern", "ZONE"] = "Accra"

    # Ahafo Region -> Bekwai
    gdf.loc[gdf["REGION_CLEAN"] == "Ahafo", "ZONE"] = "Bekwai"

    # Bono East Region -> Kumasi
    gdf.loc[gdf["REGION_CLEAN"] == "BonoEast", "ZONE"] = "Kumasi"

    # Western -> Sefwi
    gdf.loc[gdf["REGION_CLEAN"] == "Western", "ZONE"] = (
        gdf.loc[gdf["REGION_CLEAN"] == "Western", "ZONE"]
        .fillna("Sefwi")
    )

    # Western North -> Sefwi
    gdf.loc[gdf["REGION_CLEAN"] == "WesternNorth", "ZONE"] = (
        gdf.loc[gdf["REGION_CLEAN"] == "WesternNorth", "ZONE"]
        .fillna("Sefwi")
    )

# ==================================================
# EASTERN REGION DISTRICT OVERRIDE -> SWEDRU (NEW MAP ONLY)
# ==================================================

if map_version == "New Map":

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

    # Assign selected Eastern districts to Swedru
    gdf.loc[
        eastern_mask & gdf["DISTRICT_CLEAN"].isin(swedru_eastern_districts),
        "ZONE"
    ] = "Swedru"

    # Remaining Eastern districts stay Accra
    gdf.loc[
        eastern_mask & ~gdf["DISTRICT_CLEAN"].isin(swedru_eastern_districts),
        "ZONE"
    ] = "Accra"
# ==================================================
# FINAL CLEANUP
# ==================================================
gdf["ZONE"] = gdf["ZONE"].fillna("Unassigned")

# ==================================================
# SIDEBAR ZONE FILTER
# ==================================================
st.sidebar.markdown("---")
st.sidebar.header("Zone Filter")
zones = ["All Zones"] + sorted(gdf["ZONE"].unique())
selected_zone = st.sidebar.selectbox("Select Zone", zones)

filtered = gdf if selected_zone == "All Zones" else gdf[gdf["ZONE"] == selected_zone]

# ==================================================
# KPI METRICS
# ==================================================
st.subheader(f"Metrics ({map_version})")
c1, c2, c3 = st.columns(3)

c1.metric("Total Districts", len(gdf))
c2.metric("Mapped Districts", len(gdf[gdf["ZONE"] != "Unassigned"]))
c3.metric("Active Zones", gdf[gdf["ZONE"] != "Unassigned"]["ZONE"].nunique())

# ==================================================
# OFFICE LOCATIONS
# ==================================================
office_locations = {
    "Head Office": {"lat": 5.5503375, "lon": -0.2011094},
    "Kasoa Office": {"lat": 5.5306375, "lon": -0.4482031},
    "Tamale Office": {"lat": 9.4111125, "lon": -0.8265156},
    "Kumasi Office": {"lat": 6.6592875, "lon": -1.6200469}
}

if map_version == "New Map":
    office_locations.update({
        "Question Mark": {"lat": 9.85, "lon": -1.85},
        "Swedru Office": {"lat": 5.5415125, "lon": -0.6785781},
        "Ho Office": {"lat": 6.6088125, "lon": 0.4716406},
        "Sefwi Office": {"lat": 6.2113625, "lon": -2.4774844},
        "Bekwai Office": {"lat": 6.4552875, "lon": -1.5875156}
    })

# ==================================================
# FILTER OFFICE MARKERS BASED ON SELECTED ZONE
# ==================================================
zone_office_mapping = {
    "Kasoa": "Kasoa Office",
    "Tamale": "Tamale Office",
    "Kumasi": "Kumasi Office",
    "Accra": "Head Office",      # Accra Zone Office
    "Swedru": "Swedru Office",
    "Ho": "Ho Office",
    "Sefwi": "Sefwi Office",
    "Bekwai": "Bekwai Office",
    "Proposed Zone": "Question Mark"
}

if selected_zone != "All Zones":
    selected_office = zone_office_mapping.get(selected_zone)

    office_locations = {
        office: coords
        for office, coords in office_locations.items()
        if office == selected_office
    }

# ==================================================
# MAP VISUALIZATION
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

for office, data in office_locations.items():

    hover_text = office
    if office == "Head Office":
        hover_text += "<br><b>Oversees all zonal offices</b>"

    # Special handling for Proposed Zone
    if office == "Question Mark":

        fig.add_scattergeo(
            lon=[data["lon"]],
            lat=[data["lat"]],
            mode="text",
            text=["?"],
            textfont=dict(
                size=50,
                color="black"
            ),
            name="Proposed Zone",
            hovertemplate="Proposed Zone Location<extra></extra>"
        )

    else:

        fig.add_scattergeo(
    lon=[data["lon"]],
    lat=[data["lat"]],
    mode="markers+text",
    text=[office],
    textposition="top center",
    textfont=dict(
        color="black",
        size=13,
        family="Arial Black"
    ),
    marker=dict(
        size=14 if office == "Head Office" else 9,
        symbol="star" if office == "Head Office" else "circle"
    ),
    name=office,
    hovertemplate=hover_text + "<extra></extra>"
)
fig.update_layout(
    height=850,
    margin=dict(l=0, r=0, t=0, b=0),
    legend_title_text="Zones / Offices"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# DISTRICT ZONE ASSIGNMENT TABLE
# ==================================================
if selected_zone == "All Zones":
    st.subheader(f"District Zone Assignment ({map_version})")
else:
    st.subheader(
        f"District Zone Assignment - {selected_zone} Zone ({map_version})"
    )

zone_table = (
    filtered[[DISTRICT_COL, REGION_COL, "ZONE"]]
    .sort_values(["ZONE", DISTRICT_COL])
    .reset_index(drop=True)
)

st.dataframe(zone_table, use_container_width=True)

# ==================================================
# UNASSIGNED DISTRICTS MONITORING
# ==================================================
unassigned = gdf[gdf["ZONE"] == "Unassigned"]

if len(unassigned) > 0:
    st.warning(f"{len(unassigned)} districts remain unassigned in {map_version}")
    st.dataframe(unassigned[[DISTRICT_COL, REGION_COL]], use_container_width=True)
else:
    st.success(f"All districts successfully assigned for {map_version}!")
