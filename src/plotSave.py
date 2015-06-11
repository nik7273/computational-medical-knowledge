# -*- coding: utf-8 -*-
"PLOTTING FILE"
import matplotlib.pyplot as plt 
import Graphics as artist


def plot_and_save(frequencies, words, ylabel, savefile):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.semilogy(frequencies,'k--',linewidth=3)
    artist.adjust_spines(ax)

    ax.set_xticks(xrange(len(words)))
    ax.set_xticklabels([r'\textbf{\textsc{%s}'%word for word in words],rotation='vertical')
    ax.set_ylabel(artist.format(ylabel))

    plt.tight_layout()
    plt.show()
    plt.savefig(savefile, bbox_inches="tight")

