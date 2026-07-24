#!/bin/bash

PRODUCT="sentinel_2_l2a"
JOBS=8

#grids you can mention according to your region. The grid shapefile/KML can be downloaded online.
# --no-sign-request is for no login access to S3 bucket.

for GRID in \
43PFL 43PFM 43PFN \
43PGL 43PGM 43PGN \
43QFK 43QFL \
43QGK 43QGL
do
    ZONE=${GRID:0:2}
    BAND=${GRID:2:1}
    TILE=${GRID:3:2}

    aws s3 ls --recursive --no-sign-request --stac \
    s3://sentinel-cogs/sentinel-s2-l2a-cogs/${ZONE}/${BAND}/${TILE}/ \
    | awk '$4 ~ /L2A\.json$/ {print "s3://sentinel-cogs/" $4}'

done | parallel -j ${JOBS} \
's3-to-dc --stac --no-sign-request {} '"${PRODUCT}"
