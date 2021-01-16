# Gapminder Data Visualization

![](animation/life_exp_animation.gif)

## Introduction

Simple Project to visualize the Change in Life Expectancy per Continent. Uses the [Gapminder Life expectancy Dataset](https://www.gapminder.org/data/).

## Project Structure


#### 1. EDA
- Pandas is used for EDA and Data Wrangling

#### 2. Visualization
- Seaborn is used to create a Combination of a Stripplot and a Lineplot

#### 3. Animation
- Imageio is used to create an Animation with the saved Plots

## General Usage

1. Clone the Git repository: `git clone https://github.com/samuelrothen/gapminder_visualization.git`
2. Install the requirements: `pip install requirements.txt`
3. Run `/src/visualization_gapminder.py` to create a single Plot. The Year of the Plot can be set with: `createPlot(df, year = 2016)`
4. To create the Animation, set `create_animation = False` to `True`


## License

Distributed under the MIT License. See `LICENSE` for more Information.
