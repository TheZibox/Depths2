""" This script contains the data analysis for the app"""

import pandas as pd
import os


def analysis(folder):
    # Import depth and v-curve files
    depths = pd.read_csv(os.path.join(folder, 'depths.csv'))
    v_curve = pd.read_csv(os.path.join(folder, 'v_curve.csv'))

    # Obtain column names, number of depths measurements
    depths_col_name = depths.columns
    v_curve_col_names = v_curve.columns
    num_depths = len(depths)

    # Treat depths data: Remove non numeric values
    # More rigorous checks could be implemented for depths and vulnerability for quality
    depths = depths[pd.to_numeric(depths[depths_col_name[0]], errors='coerce').notnull()]

    # Obtain categories column
    v_curve['labels'] = v_curve[v_curve_col_names[0]].astype(str) + "-" + v_curve[v_curve_col_names[1]].astype(str)

    # Extract values for v-curve ranges
    labels = list(v_curve.labels)
    lower_limits = list(v_curve[v_curve_col_names[0]])
    upper_limits = list(v_curve[v_curve_col_names[1]])
    lower_limits.append(upper_limits[-1])

    # Add bin tags to data
    depths['Category'] = pd.cut(depths[depths_col_name[0]], bins=lower_limits, labels=labels)

    # Count bin tags frequency
    depths_ranges = depths['Category'].value_counts(sort=False).reset_index()
    depths_ranges.columns = ['Category', 'Frequency']

    # Extract analysis values for chart and summary
    values = depths_ranges['Frequency']
    labels = depths_ranges['Category']

    top_frequency = depths_ranges.loc[depths_ranges['Frequency'].argmax()]['Frequency']
    top_category = depths_ranges.loc[depths_ranges['Frequency'].argmax()]['Category']

    top_category_damage = v_curve.loc[v_curve['labels'] == top_category][v_curve_col_names[2]].values[0]

    results = {'values':values,
               'labels':labels,
               'top_category':top_category,
               'top_category_damage':top_category_damage,
               'top_frequency':top_frequency,
               'num_depths':num_depths
               }

    return results
