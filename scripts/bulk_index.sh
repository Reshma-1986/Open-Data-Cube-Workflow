#!/bin/bash

# Define all the grid zones you need to scan
GRIDS=("43PDQ" "43PEQ" "43PER" "43PEN" "43PFN" "43PFP" "43PFM" "43PEM" "43PFL" "43PGL" "43PGK")

echo "Starting automated S3 indexing process..."

for GRID in "${GRIDS[@]}"; do
    # Extract structural path coordinates out of the grid string
    ZONE="${GRID:0:2}"
    BAND="${GRID:2:1}"
    SQUARE="${GRID:3:2}"
    
    # Reconstruct the target subfolder prefix structure 
    PREFIX="sentinel-s2-l2a-cogs/${ZONE}/${BAND}/${SQUARE}/"
    echo "=========================================================="
    echo "Scanning and Indexing Grid: ${GRID}"
    echo "S3 Path: s3://sentinel-cogs/${PREFIX}"
    echo "=========================================================="

    # 1. Recursively find every single JSON metadata file matching the S2A structure
    # 2. Extract and rewrite structural URL prefixes safely to prevent broken pipes
    # 3. Stream straight into your validated s3-to-dc execution parameters
    aws s3 ls "s3://sentinel-cogs/${PREFIX}" --recursive --no-sign-request | \
    grep 'S2A_.*\.json$' | \
    sed "s|^.*${PREFIX}|s3://sentinel-cogs/${PREFIX}|" | \
    s3-to-dc --no-sign-request --stac - sentinel_2_l2a

    echo "Completed processing for grid: ${GRID}"
    echo ""
done

echo "Bulk indexing sequence completed successfully!"
