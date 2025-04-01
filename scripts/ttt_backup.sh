#!/bin/bash

# Load variables from .env
export $(grep -v '^#' ../.env | xargs)

# Get the current timestamp
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Define the backup file name with the timestamp
BACKUP_FILE="$BACKUP_DIR/ttt_$TIMESTAMP.db"

# Copy the file to the backup directory with the new name
cp "$SOURCE_FILE" "$BACKUP_FILE"
