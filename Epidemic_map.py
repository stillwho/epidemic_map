import pandas as pd  # 用于读取excel文件
from pyecharts import options as opts  # 可视化选项
from pyecharts.charts import Timeline, Map  # 时间线、地图
from pyecharts.globals import ThemeType  # 图表主题


src_file = "Epidemic data.xls"

# 疫情地图所用颜色
list_color = ['#F4AD8B', '#EF826F', '#EE806E', '#BD3932 ', '#801D17']
# 读取数据
df = pd.read_excel(io=src_file, usecols=['provinceName', 'province_confirmedCount', 'updateTime'])
# 清洗更新时间
# 按省份日期分组统计-确诊数量
df['updateTime'] = df['updateTime'].astype(str).str[0:10]
df2 = df.groupby(['provinceName', 'updateTime']).apply(
    lambda t: t[t.province_confirmedCount == t.province_confirmedCount.max()])
df2 = df2[['provinceName', 'province_confirmedCount', 'updateTime']]
# 删除重复值
df2 = df2.drop_duplicates()
# 重置索引
df2 = df2.reset_index(drop=True)
df2.head()

df_20200201 = df2[df2['updateTime'].str.contains("2020-02-01")]
df_20200202 = df2[df2['updateTime'].str.contains("2020-02-02")]
df_20200203 = df2[df2['updateTime'].str.contains("2020-02-03")]
df_20200204 = df2[df2['updateTime'].str.contains("2020-02-04")]
df_20200205 = df2[df2['updateTime'].str.contains("2020-02-05")]
df_20200206 = df2[df2['updateTime'].str.contains("2020-02-06")]
df_20200207 = df2[df2['updateTime'].str.contains("2020-02-07")]
df_20200208 = df2[df2['updateTime'].str.contains("2020-02-08")]
df_20200209 = df2[df2['updateTime'].str.contains("2020-02-09")]
df_20200210 = df2[df2['updateTime'].str.contains("2020-02-10")]
df_20200211 = df2[df2['updateTime'].str.contains("2020-02-11")]
df_20200212 = df2[df2['updateTime'].str.contains("2020-02-12")]
df_20200213 = df2[df2['updateTime'].str.contains("2020-02-13")]
df_20200214 = df2[df2['updateTime'].str.contains("2020-02-14")]

df_list = [df_20200201,
           df_20200202,
           df_20200203,
           df_20200204,
           df_20200205,
           df_20200206,
           df_20200207,
           df_20200208,
           df_20200209,
           df_20200210,
           df_20200211,
           df_20200212,
           df_20200213,
           df_20200214]


def timeline_map() -> Timeline:

    tl = Timeline(init_opts=opts.InitOpts(page_title="疫情地图",  # 标题
                                          theme=ThemeType.CHALK,  # 颜色主题
                                          width="1000px",  # 图形宽度
                                          height="600px"),  # 图形高度
                  )
    for idx in range(0, 14):  # 循环14天的数据
        provinces = []
        confirm_value = []
        for item_pv in df_list[idx]["provinceName"]:
            provinces.append(item_pv)
        for item_pc in df_list[idx]["province_confirmedCount"]:
            confirm_value.append(item_pc)

        zipped = zip(provinces, confirm_value)  # 组合2个字段
        f_map = (
            Map(init_opts=opts.InitOpts(width="800px",
                                        height="500px",
                                        page_title="疫情地图",
                                        bg_color="#808080"))
                .add(series_name="确诊数量",
                     data_pair=[list(z) for z in zipped],
                     maptype="china",
                     is_map_symbol_show=False)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="2020.2月全国疫情地图",
                                          subtitle="2月{}日-当天数据\n".format(idx + 1),
                                          pos_left="center", ),
                legend_opts=opts.LegendOpts(
                    is_show=True, pos_top="40px", pos_right="30px"),
                visualmap_opts=opts.VisualMapOpts(
                    is_piecewise=True, range_text=['高', '低'], pieces=[
                        {"min": 10000, "label": '>10000人', "color": "#751d0d"},
                        {"min": 1000, "max": 9999, "label": '1000-9999人', "color": "#ae2a23"},
                        {"min": 500, "max": 999, "label": '500-999人', "color": "#d6564c"},
                        {"min": 100, "max": 499, "label": '100-499人', "color": "#f19178"},
                        {"min": 10, "max": 99, "label": '10-99人', "color": "#f7d3a6"},
                        {"min": 1, "max": 9, "label": '1-9人', "color": "#fdf2d3"},
                        {"min": 0, "max": 0, "label": '0人', "color": "#FFFFFF"}
                    ]),
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                                 markpoint_opts=opts.MarkPointOpts(symbol_size=[90, 90], symbol='circle'),
                                 effect_opts=opts.EffectOpts(is_show='True', )
                                 )
        )
        tl.add(f_map, "{}日".format(idx + 1))
        tl.add_schema(is_timeline_show=True,
                      play_interval=1000,
                      symbol=None,
                      is_loop_play=True
                      )
    return tl


timeline_map().render("Epidemic_map.html")
