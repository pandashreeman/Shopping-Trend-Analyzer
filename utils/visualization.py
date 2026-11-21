import matplotlib.pyplot as plt


# Burgundy and Baby Pink Theme
BURGUNDY = "#800F3F"
DARK_BURGUNDY = "#4A1028"
BABY_PINK = "#FCE7EF"
SOFT_PINK = "#F4B6CC"


def apply_chart_style(ax, title, xlabel="", ylabel=""):

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color=DARK_BURGUNDY
    )

    ax.set_xlabel(xlabel, color=BURGUNDY)
    ax.set_ylabel(ylabel, color=BURGUNDY)

    ax.set_facecolor("white")

    ax.tick_params(colors=DARK_BURGUNDY)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def create_bar_chart(ax, x, y, title, xlabel="", ylabel=""):

    ax.bar(
        x,
        y,
        color=BURGUNDY,
        edgecolor=SOFT_PINK
    )

    apply_chart_style(ax, title, xlabel, ylabel)


def create_line_chart(ax, x, y, title, xlabel="", ylabel=""):

    ax.plot(
        x,
        y,
        color=BURGUNDY,
        marker="o",
        linewidth=2
    )

    apply_chart_style(ax, title, xlabel, ylabel)


def create_pie_chart(ax, labels, values, title):

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=[
            BURGUNDY,
            SOFT_PINK,
            DARK_BURGUNDY,
            "#E8A1BC",
            "#C65B83"
        ]
    )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color=DARK_BURGUNDY
    )