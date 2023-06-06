from django.db import migrations
from django.apps import apps as django_apps

import os
from django.contrib.gis.utils import LayerMapping

# Each key in the nhsenglandregionboundaries_mapping dictionary corresponds to
nhsenglandregionboundaries_mapping = {
    "nhser22cd": "NHSER22CD",
    "nhser22nm": "NHSER22NM",
    "bng_e": "BNG_E",
    "bng_n": "BNG_N",
    "long": "LONG",
    "lat": "LAT",
    "globalid": "GlobalID",
    "geom": "MULTIPOLYGON",
}

app_config = django_apps.get_app_config("epilepsy12")
app_path = app_config.path

NHS_England_Regions_July_2022_EN_BUC_2022 = os.path.join(
    app_path,
    "shape_files",
    "NHS_England_Regions_July_2022_EN_BUC_2022",
    "NHSER_JUL_2022_EN_BUC.shp",
)


def load(apps, schema_editor, verbose=True):
    NHSEnglandRegionBoundaries = apps.get_model(
        "epilepsy12", "NHSEnglandRegionBoundaries"
    )
    lm = LayerMapping(
        NHSEnglandRegionBoundaries,
        NHS_England_Regions_July_2022_EN_BUC_2022,
        nhsenglandregionboundaries_mapping,
        transform=False,
        encoding="utf-8",
    )
    lm.save(strict=True, verbose=verbose)


class Migration(migrations.Migration):
    dependencies = [
        ("epilepsy12", "0010_countryboundaries_integratedcareboardboundaries_and_more"),
    ]

    operations = [migrations.RunPython(load)]