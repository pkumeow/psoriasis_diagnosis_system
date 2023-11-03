$(function(){
	changeMap();
})
function changeMap(){
	var myChart= echarts.init(document.getElementById('map'));

	var name_title = "银屑病全国分布图"
	var mapName = 'china'
	var data = [
	//{ name: '湖北', value:4586 },
	{ name: '湖北', value: 5806 },
	{ name: '浙江', value: 537 },
	{ name: '广东', value: 393 },
	{ name: '湖南', value: 332 },
	{ name: '河南', value: 278 },
	{ name: '江西', value: 240 },
	{ name: '安徽', value: 237 },
	{ name: '重庆', value: 206 },
	{ name: '山东', value: 178 },
	{ name: '四川', value: 177 },
	{ name: '江苏', value: 168 },
	{ name: '上海', value: 128 },
	{ name: '北京', value: 121 },
	{ name: '福建', value: 101 },
	{ name: '广西', value: 87 },
	{ name: '河北', value: 82 },
	{ name: '云南', value: 76 },
	{ name: '陕西', value: 63 },
	{ name: '黑龙江', value: 59 },
	{ name: '海南', value: 46 },
	{ name: '辽宁', value: 45 },
	{ name: '山西', value: 39 },
	{ name: '天津', value: 31 },
	{ name: '甘肃', value: 29 },
	{ name: '内蒙古', value: 18 },
	{ name: '宁夏', value: 17 },
	{ name: '吉林', value: 14 },
	{ name: '新疆', value: 14 },
	{ name: '贵州', value: 12 },
	{ name: '香港', value: 12 },
	{ name: '台湾', value: 9 },
	{ name: '青海', value: 8 },
	{ name: '澳门', value: 7 },
	{ name: '西藏', value: 1 },

	];
	
	var option = {
		title: {
			text: name_title,
			x: 'center',
			textStyle: {
				fontSize: 24
			},                
		},
		tooltip: {
			trigger: 'item',
			formatter: function(params) {                        
					var toolTiphtml = ''
					if (isNaN(params.value)){
					toolTiphtml = params.name + '病例: 0例'
					}else{
					toolTiphtml = params.name + '病例: ' + params.value + '例'
					}
					//console.log(toolTiphtml)                        
					return toolTiphtml;                   
			}
		},
		toolbox: {
			feature: {
				saveAsImage: {}
			}
		},
		visualMap: {
			show: true,
			
			left: 'left',
			top: 'bottom',
			seriesIndex: [0],
			type:'piecewise',
			pieces:[
				{min:4000, color: 'rgb(254,57,101)'},
				{min:250, max:3999, color: 'rgb(252,157,154)'},
				{min:100, max:249, color: 'rgb(249,205,173)'},
				{min:10, max:99, color: 'rgb(200,200,169)'},
				{min:1, max:9, color: 'rgb(131,175,155)'},
			],            
			textStyle: {
				color: '#000000'
			}
		},            
		geo: {
			show: true,
			map: mapName,
			
			label: {
				normal: {
					show: true,
					fontSize:12,
				},
				emphasis: {
					show: false,
				}
			},
			roam: false,
			itemStyle: {
				normal: {
					areaColor: '#FFFFFF',
					borderColor: '#666666',
				},
				emphasis: {
					areaColor: '#0099CC',
				}
			}
		},
		series: [
			{
				type: 'map',
				map: mapName,
				geoIndex: 0,  
				
				animation: false,
				itemStyle: {
					normal: { label: { show: true } },
					emphasis: { label: { show: true } }
				}, 
                label: {
					normal: {  
						textStyle: {
							fontSize: 12,
							fontWeight: 'bold',
							color: 'black'
						}
					}
				}, 
				data: data
				
			},
		]
	};
	var Province = "";
	myChart.on('click', function (params){
		var myChart= echarts.init(document.getElementById('map'));
		Province = params.name;
		option1 = {
		    tooltip: {
		        trigger: 'item',
		        formatter: '{b}'
		    },
		    series: [
		        {
		            name: '中国',
		            type: 'map',
		            mapType: Province,
		            selectedMode : 'single',
		            label: {
		                normal: {
		                    show: true
		                },
		                emphasis: {
		                    show: true
		                }
		            },
		             data:[
	                
	            ]
		        }
		    ]
		};
		myChart.on('click', function (params){
			changeMap();
		});
		myChart.setOption(option1);
 		window.addEventListener("resize",function(){
       	 	myChart.resize();
   		});
	});
	
	myChart.setOption(option);
 	window.addEventListener("resize",function(){
        myChart.resize();
   });
}
