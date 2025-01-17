from process_ai_experiment import produce_ai_df
from process_experiment import produce_df
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import r2_score
import seaborn as sns

if __name__ == "__main__":
    ai_df = produce_ai_df()
    df = produce_df()

    ai_medians = ai_df.groupby('name')['rel_len'].median().reset_index()
    ai_medians['participant'] = 'Med. AIs'
    ai_medians = ai_medians[['participant', 'rel_len', 'name']]

    # Calculate the median for each problem
    medians = df.groupby('name')['rel_len'].median().reset_index()
    medians['participant'] = 'Med. participants'

    # Rearrange the columns to match the original DataFrame
    medians = medians[['participant', 'rel_len', 'name']]



    # Append the median rows to the original DataFrame
    df_with_medians = pd.concat([ai_df, medians, ai_medians], ignore_index=True)
    rows_to_drop = df_with_medians[~df_with_medians['participant'].isin(['Med. participants', 'CHATGPT_JSON', 'Med. AIs'])].index
    df_dropped = df_with_medians.drop(index=rows_to_drop)

    sns.barplot(
        data=df_dropped,
        x='name',
        y='rel_len',
        hue='participant',
        palette='tab10'  # Adjust the color palette if needed
    )

    ax = plt.gca()
    ax.set_ylim([0.9, 1.4])
    plt.grid(axis='both', linestyle='--', alpha=0.7)  # Grid lines for better readability
    plt.title('Comparision of participants and AIs', fontsize=16, weight='bold')  # Title
    plt.xlabel('Problem', fontsize=12)  # X-axis label
    plt.ylabel('Relative length', fontsize=12)  # Y-axis label
    # plt.legend(title='Method', fontsize=10)  # Legend with a title
    plt.legend()
    plt.tight_layout()  # Adjust the layout to avoid clipping
    plt.savefig("../figs/AI_part_comparision.png", dpi=300, bbox_inches='tight')
    plt.show()
    print(df_dropped)