# Abaqus RPT Parser

This Python script reads `.rpt` files exported from Abaqus containing stress results along integration paths (stress lines). It extracts the stress values for selected types and exports a structured summary in `.csv` format.

## Features

* Supports stress types: `Mises`, `Tresca`, `Max.`, `Min.`, and `Mid.`
* Automatically detects Load Cases and stress line sections
* Maps and extracts relevant stress values for key integration points
* Outputs a clean summary `.csv` file for the selected stress type

## How to Use

1. Place your `.rpt` file in the same directory as this script
2. Edit the `file` variable at the top of the script with your `.rpt` filename
3. Set the desired `stress_type` (e.g., `Min.` or `Mises`)
4. Run the script using Python 3:

```bash
python read_rpt_from_abq.py
```

5. The script will create a `.csv` file named:

```text
<original_filename>_summary_<stress_type>.csv
```

## Example

**Input**:
`linearStress_undeformed.rpt`

**Output**:
`linearStress_undeformed_summary_Min.csv`

## Requirements

* Python 3
* pandas

You can install the required package with:

```bash
pip install pandas
```

## File Structure

Each row in the exported CSV represents a unique stress line section within a given load case. The columns include:

* Load Case
* Section
* (Average) Stress
* Bending Points 1 & 2
* Peak Points 1 & 2

All values correspond to the selected stress type.

## Author

Developed by Brenick Resende
