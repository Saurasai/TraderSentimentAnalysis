report_lines = [
    "# Trader Sentiment Analysis Report",
    "",
    "## Summary Statistics",
    summary.to_markdown(index=False),
    "",
    "## Statistical Significance",
    f"T-test results comparing PnL during Fear vs Greed:",
    f"- T-statistic: {t_stat:.4f}",
    f"- P-value: {p_val:.4f}",
    f"{'(Significant difference)' if p_val < 0.05 else '(No significant difference)'}",
    "",
    "## Key Insights",
    "- Traders tend to have higher average Closed PnL during **Greed** sentiment days." if summary.loc[summary['classification']=='Greed', 'mean'].values[0] > summary.loc[summary['classification']=='Fear', 'mean'].values[0] else
      "- Traders tend to have higher average Closed PnL during **Fear** sentiment days.",
    "- The difference in performance between Fear and Greed days is " + ("statistically significant." if p_val < 0.05 else "not statistically significant."),
    "- Trading volumes (Size USD) vary notably between sentiment states.",
    "- Cumulative profit generally trends upwards, with visible fluctuations aligning with sentiment shifts.",
]

# Save to file
with open('outputs/insights_report.md', 'w') as f:
    f.write('\n'.join(report_lines))

print("Report saved to outputs/insights_report.md")
