#Import of Modules and Files


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import imageio
import sys


#Import Function for Gapminder Datasets
def importDF(filename,val_name):
    if filename.endswith('.xlsx'):
        df=pd.read_excel(filename,index_col=0)
    elif filename.endswith('.csv'):
        df=pd.read_csv(filename,index_col=0)
    else:
        return print('Check File-Format!')
    df.columns=df.columns.astype(int)
    df.index.name = 'country'
    df=df.reset_index()
    df = df.melt(id_vars='country',var_name='year', value_name=val_name)
    return df


#Create the Plot
def createPlot(df, year, saveplot=False):
    if year not in df['year'].unique():
        print('Year is not valid!')
        sys.exit()
    
    #List of Continents to give them an fixed order in the plot
    order=['Asia','Europe','Africa','North America','South America','Australia and Oceania']
    
    #Definition of List and Dic for the Lineplot
    years_l=[]
    cont_mean={}
    for c in order:
        cont_mean[c]=[]
    
    #Iterating from 1800 to given year
    #Calculating the mean value for every continent
    #Appending to List in Dic
    for y in range(df['year'].min(),year+1):
        df_year_filt=df[df['year'].isin([y])]
        df_means=df_year_filt.groupby('continent').mean().reset_index()
        for c in order:
            cont_mean[c].append(float(df_means[df_means['continent']==c]['life_exp'].values))
        years_l.append(y)
    
    #Filtering the df by Year
    df_year_filt=df[df['year'].isin([year])]
    #Calculating the mean Values for every Continent
    df_means=df_year_filt.groupby('continent').mean().reset_index()
    #Calculating the mean for whole world in given Year
    world_mean=df_means['life_exp'].mean()
    
    #Define the Figure
    fig1=plt.figure('Life Expectancy Visualization single',(22,11))
    fig1.clf()
    
    #Setting Font Sizes and defining Axis
    sns.set(font_scale = 1.8)
    ax=plt.subplot(121)
    ax2=plt.subplot(122)
    
    #Plotting the Stripplott (all Countries)
    sns.stripplot(y='continent',x='life_exp',order=order,data=df_year_filt,alpha=0.5,ax=ax)
    #Plotting the Stripplott (Continents Mean)
    sns.stripplot(y='continent',x='life_exp',order=order,data=df_means,s=20,ax=ax,jitter=0)
    #Plotting the World Mean Line
    ax.plot([world_mean,world_mean],ax.get_ylim(),c='k')
    #Adding Text to the World Mean Line
    ax.annotate('   Worldwide Average\n    {} Years'.format(int(round(world_mean,0))),(world_mean,ax.get_ylim()[0]-0.2), fontsize=15)
    
    #Adding Year in the Background of the Plot
    ax.text(0.25,0.42,year,size=150,alpha=0.1,transform=ax.transAxes)
    
    #Adding a Vector Image of a Worldmap
    img=plt.imread('../data/wmap.png')
    newax = fig1.add_axes([0.8, 0.8, 0.16, 0.16], zorder=1)
    newax.imshow(img,origin='upper')
    newax.axis('off')
    
    #Plotting the Mean Continent Values over Time in Lineplot
    for c in order:
        ax2.plot(years_l,cont_mean[c],marker='o',markersize=3)
    
    #Setting Labels and Axis Limits
    ax.set_xlim(15,105)
    ax.set_xlabel("Life Expectancy [Years]")
    ax.set_ylabel('')
    ax2.set_xlim(1800,2050)
    ax2.set_ylim(15,105)
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Life Expectancy [Years]')
    
    #Resize the Axis
    plt.tight_layout()

    #Safe the Figure
    if saveplot:
        fig1.savefig(f'../images/lifeexp_{year}.png', dpi=80)



#Import Files
df_continents=pd.read_csv('../data/continents.csv',delimiter=';', encoding = 'ISO-8859-1')
df_life_exp=importDF('../data/gapminder_lifeexpectancy.xlsx','life_exp')


#Merge the Dataset
df=df_life_exp.merge(df_continents,how='left')


#Drop missing Data
df = df[df['continent'].notna()]


#Create single Plot
createPlot(df, year = 2016)

#Set to True to create Animation
create_animation = False


if create_animation:
    #Create multiple Plots and Animation
    for year in df['year'].unique():
        createPlot(df, year, saveplot = True)
    
    images = []
    for year in df['year'].unique():
        filename = f'../images/lifeexp_{year}.png'
        images.append(imageio.imread(filename))
    imageio.mimsave('../animation/life_exp_animation1.gif', images, fps=15)
    