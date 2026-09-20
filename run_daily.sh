#!/bin/bash

# Daily Fintables Analysis Script

cd /path/to/deneme

# Run analysis
python main.py --period 90 >> logs/analysis_$(date +%Y-%m-%d).log 2>&1

# Backup results
cp output/results.json output/results_$(date +%Y-%m-%d_%H-%M-%S).json

echo "Analysis completed at $(date)" >> logs/daily_runs.log
