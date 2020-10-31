var myChart = echarts.init(document.getElementById('show'));
var option = {
    title: {
        text: '公司各部门职员人数统计'
    },
    tooltip: {},
    legend: {
        //data: ['职员人数']
    },
    xAxis: {
        data: ["人事部", "后勤部", "安保部", "市场部", "技术部", "新媒体部", "法务部", "董事会", "财务部"]
    },
    yAxis: {},
    series: [{
        name: '职员人数',
        type: 'bar', //柱状图
        data: [990, 0, 0, 907, 961, 943, 0, 1, 1001]
    }]
};
myChart.setOption(option);