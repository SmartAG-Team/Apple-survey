import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import os

data = pd.read_excel('.Data/apple_statistical/Apple_2022_statistical _data.xlsx')
pro_py = pd.read_csv('.Data/apple_statistical/Provinces_Eng.csv', index_col=0)
provinces = gpd.read_file('.data/map_boundary_line/province_boundary.shp')
nine = gpd.read_file('.Data/map_boundary_line/national_boundary_line.shp')

map_dict = {py.capitalize():name for name, py in zip(pro_py['0'],pro_py['1'])}
map_dict.update({'Shaanxi':'陕西','Tianjing':'天津'})
data['NAME'] = data.Province.map(map_dict)

df=pd.merge(provinces, data, on='NAME',how='outer')
df = df.to_crs(epsg=4326)

plt.rcParams['xtick.labelsize'] = 8.5
plt.rcParams['ytick.labelsize'] = 8.5
plt.rcParams['font.sans-serif'] = ['Times New Roman']

def formate_labels(p_ax):
    g = p_ax.gridlines(crs= ccrs.PlateCarree(), draw_labels=True, linewidth=0.5, alpha=0.5, linestyle='--')
    g.xlocator = mticker.FixedLocator([75,95,115,135])
    g.ylocator = mticker.FixedLocator([10, 20,30,40,50])
    g.top_labels= False
    g.right_labels = False
    g.xformatter = LONGITUDE_FORMATTER
    g.yformatter = LATITUDE_FORMATTER
    g.xlabel_style = {'size': 8.5}
    g.ylabel_style = {'size': 8.5, 'rotation':90}

fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(11, 6), dpi=300, subplot_kw={'projection': ccrs.PlateCarree()})
axs = axs.flatten()

plt.subplots_adjust(wspace=0.01, hspace=0.2)
for i, column in enumerate(['Planting area (K ha)', 'Production (K ton)', 'Yield (ton per ha)', 'Questionnaire']):
    df.plot(column=column, ax=axs[i], cmap='YlGn', legend=True,
             legend_kwds={"label": f"{column}"},
             missing_kwds={"color": "lightgrey", "hatch": "///"})
    

p1 = provinces.to_crs(4326).plot(facecolor='none', edgecolor='k',ax=axs[0],lw=0.5)
p1.annotate('(a)', xy=(0.06, 0.9), xycoords='axes fraction', size=10, fontweight='bold')
formate_labels(p_ax=p1)
for x, y, label in zip(df.representative_point().x, df.representative_point().y, df['Province']):
    p1.text(x-3, y, label, fontsize=5, fontweight='bold')

p2 = provinces.to_crs(4326).plot(facecolor='none', edgecolor='k',ax=axs[1],lw=0.5)
p2.annotate('(b)', xy=(0.06, 0.9), xycoords='axes fraction', size=10, fontweight='bold')
formate_labels(p_ax=p2)

p3 = provinces.to_crs(4326).plot(facecolor='none', edgecolor='k',ax=axs[2],lw=0.5)
p3.annotate('(c)', xy=(0.06, 0.9), xycoords='axes fraction', size=10, fontweight='bold')
formate_labels(p_ax=p3)

p4 = provinces.to_crs(4326).plot(facecolor='none', edgecolor='k',ax=axs[3],lw=0.5)
p4.annotate('(d)', xy=(0.06, 0.9), xycoords='axes fraction', size=10, fontweight='bold')
formate_labels(p_ax=p4)

nine_extent = [95, 125, 0, 30]
for i, ax in enumerate(axs):
    inset_ax = inset_axes(ax, width="12%", height="25%", loc='lower right')
    inset_ax.set_xlim(*nine_extent[:2])  
    inset_ax.set_ylim(*nine_extent[2:])  
    inset_ax.set_xmargin(0)  
    inset_ax.set_ymargin(0)  

    nine.to_crs(4326).plot(ax=inset_ax, color='k', linewidth=1)
    provinces.to_crs(4326).plot(ax=inset_ax, facecolor='none', edgecolor='gray', linewidth=0.5)

    inset_ax.xaxis.set_visible(False)
    inset_ax.yaxis.set_visible(False)

save_path = "../Figure/statistical_map.jpg"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()

