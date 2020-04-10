import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pipeline_text import *
import matplotlib.patches as mpatches

plt.rcParams.update({'font.size': 20})


def df_count_entries_by_type(dataframe):
    type_count = dataframe.groupby('type').count().sort_values(by='posts', ascending=True).reset_index()
    return type_count

def plot_barchart_type_frequency(type_count, ei_color=False):
    hist_data = list(type_count['posts'])
    hist_label = list(type_count['type'])
    ei_colors = ['red', 'blue']
    ei_legend = ['Introvert', 'Extrovert']
    red_patch = mpatches.Patch(color=ei_colors[0], label=ei_legend[0])
    blue_patch = mpatches.Patch(color=ei_colors[1], label=ei_legend[1])


    color_by_ei = [ei_colors[hist_label[i][:1]=="E"] for i in range(len(hist_label))]
    y = np.arange(len(hist_data))

    width = 0.8
    fig, ax = plt.subplots(figsize = (10,6))
    if ei_color:
        ax.barh(y, hist_data, width, color = color_by_ei, align = 'center')
        plt.legend(handles=[red_patch, blue_patch], fontsize=14)
        # ax.legend(handles = ei_legend)
        save_name = "images/post_count_by_type_ei.png"
    else:
        ax.barh(y, hist_data, width, color = ['wheat'], align = 'center')
        save_name = "images/post_count_by_type.png"
    
    ax.set_yticks(y)
    ax.set_yticklabels(hist_label, size=14)
    ax.xaxis.grid(True)
    ax.set_ylabel('MBTI Type', size=18, labelpad=6)
    ax.set_xlabel('Users on Website', size=18, labelpad=18)
    fig.tight_layout(pad=0)
    plt.subplots_adjust(left=0.11, right=0.96, top=0.98)
    plt.show()
    fig.savefig(save_name)
    
def plot_post_count_by_length_by_type(df):
    # To define a standard layout of the 4x4 plot per Myers-Briggs convention
    types = {'ISTJ': (0,0),'ISFJ': (0,1),'INFJ': (0,2),'INTJ': (0,3),
         'ISTP': (1,0),'ISFP': (1,1),'INFP': (1,2),'INTP': (1,3),
         'ESTP': (2,0),'ESFP': (2,1),'ENFP': (2,2),'ENTP': (2,3),
         'ESTJ': (3,0),'ESFJ': (3,1),'ENFJ': (3,2),'ENTJ': (3,3)
        }
    
    fig, axs = plt.subplots(4, 4, figsize=(16, 16), sharex=True, sharey=True)

    for i in range(len(list(types.keys()))):
        ax = axs[types[list(types.keys())[i]]]
        ax.grid(True, color='black', alpha=0.5, linestyle='dashed')
        ax.hist(df.loc[list(types.keys())[i],:], bins=20, alpha = 0.75)
        ax.set_xlabel('Length of post (chars)', fontsize=18, labelpad=18)
        ax.set_ylabel('Counts (log)', fontsize=18, labelpad=18)
        ax.set_axisbelow(True)
        ax.text(100, 10000, list(types.keys())[i], fontsize = 18, fontweight='bold', color = 'red',
            bbox={'facecolor': 'white', 'edgecolor': 'white', 'alpha': 0.75, 'pad': 10})
        xvalues = np.arange(0, 251, 50)
        plt.xticks(xvalues)
        ax.set_xticklabels(xvalues, fontsize=16)
        yvalues = np.arange(1, 40001, 10000)
        plt.yticks(yvalues)
        ax.set_yticklabels(yvalues, fontsize=12)
        ax.label_outer()

    plt.yscale("log")
    fig.suptitle('Count of Posts by Post Length for MBTI Types', fontsize=22, fontweight='bold', y = 0.98)
    fig.tight_layout(pad = 2)
    plt.subplots_adjust(top=0.94)
    plt.show()
    fig.savefig("images/post_length_hist_by_type.png", dpi=125)

def replace_names(word_lst, name_set, replacement_val):
    word_lst_with_replacement = [] 
    for word in word_lst:
        if word in name_set:
            val = replacement_val
        else:
            val = word
        word_lst_with_replacement.append(val)
    return word_lst_with_replacement

def remove_newline(text):
    return text.replace('\n', '')

def create_cleaned_textline_from_words(words):
    text = ' '.join([word for word in words])
    return text


if __name__ == "__main__":
    
    df_raw = pd.read_csv('data/mbti_1.csv')
    
    # 1 Count and plot Frequency of entries by type
    df_type_count = df_count_entries_by_type(df_raw)
    plot_barchart_type_frequency(df_type_count, False)
    
    # 2 Counts of Posts by Post Length for Types
    df_raw_no_quote = remove_first_last_quote(df_raw, 'posts')
    df_split_posts = split_df_col_text_by_delim(df_raw_no_quote, 'posts', delim='\|\|\|')
    df_post_lengths = create_post_length_list(df_split_posts, 'posts', 'posts_char_count')
    df_length_lists_by_type = group_post_length_lists_by_type(df_post_lengths, 'type', 'posts_char_count')
    plot_post_count_by_length_by_type(df_length_lists_by_type)
  
  