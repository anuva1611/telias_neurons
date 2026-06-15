import os
import matplotlib.pyplot as plt

# Input data format: [True Positives, False Positives, False Negatives]
validation_data = {
    "CELL1_TIME1": [42, 2, 3],
    "CELL1_TIME2": [45, 1, 4],
    "CELL2_TIME1": [58, 4, 6],
    "CELL2_TIME2": [62, 3, 8]}

# Calculation 
processed_results = {}

for dataset, counts in validation_data.items():
    tp, fp, fn = counts[0], counts[1], counts[2]
    total = tp + fp # Total tracks initially recorded
    
    # Mathematical equations for accuracy tracking
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    processed_results[dataset] = {"Precision": precision, "Recall": recall, "F1-Score": f1}

# Visualization 
datasets = list(processed_results.keys())
precision_vals = [processed_results[d]["Precision"] for d in datasets]
recall_vals = [processed_results[d]["Recall"] for d in datasets]
f1_vals = [processed_results[d]["F1-Score"] for d in datasets]

x = range(len(datasets))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
# Generate grouped bars side-by-side
ax.bar([i - width for i in x], precision_vals, width, label='Precision', color='greem')
ax.bar(x, recall_vals, width, label='Recall', color='blue')
ax.bar([i + width for i in x], f1_vals, width, label='F1-Score', color='yellow', edgecolor='blue')
ax.set_ylabel('Score Gradient (0.0 - 1.0)')
ax.set_title('Traced Neuron Morphology Accuracy Validation Metrics Across Timepoints')
ax.set_xticks(x)
ax.set_xticklabels(datasets)
ax.set_ylim(0, 1.1) 
ax.legend(loc='upper right')
ax.grid(axis='y', linestyle='--', alpha=0.5)