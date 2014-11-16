$(document).ready(function(){
    
   //console.log(explorer);
   
   if (explorer) {
        
        console.log(explorer);
        track_changes();
        report_feature_stats(explorer.feature_details);
        generate_histograms(explorer.histograms);
        generate_scatterplots(explorer.scatter_points, explorer.correlations);
   }

});



function track_changes() {
    $('.heading_type_a').unbind('click').bind('click', function(e){
        e.preventDefault();
        $(this).siblings().toggleClass('hidden_class');
    });
    
}


function report_feature_stats(feature_details) {
    for (k  in feature_details) {
        key = "<div class='key_facts_values'>"+k+"</div>";
        max = "<div class='key_facts_values'>"+feature_details[k].max+"</div>";
        min = "<div class='key_facts_values'>"+feature_details[k].min+"</div>";
        mean = "<div class='key_facts_values'>"+feature_details[k].mean+"</div>";
        stdev = "<div class='key_facts_values'>"+feature_details[k].std+"</div>";
    
        row = "<div class='key_facts_row'>"+key+max+min+mean+stdev+"</div>";
        $('.key_facts').append(row);
    }
}

function generate_histograms(histograms){
    
    for (k in histograms) {
        current_key = k;
        current_histogram = histograms[k];
        var keys = [];
        var values = [];
        for (e in current_histogram){
            keys.push(e);
            values.push(current_histogram[e]);
        }
        
        plot_histogram(keys, values, current_key);
    }
    
    function plot_histogram(c_k, c_v, ck){
        $div = "<div class='histogram_block' id="+ck+"></div>";
        $('.histograms').append($div);
        
        Highcharts.setOptions({
            colors: ['rgb(223, 101, 101)', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4']
        });

        
        
        $('#'+ck).highcharts({
            credits: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            chart: {
                type: 'column'
            },
            title: {
                text: 'Histogram ('+ck+')'
            },
            xAxis: {
                categories: c_k
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Frequency'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:f} times</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [{
                name: ck,
                data: c_v
    
            }, ]
        });
        
    }
    
}


function generate_scatterplots(scatter_points, correlations) {
   for (k in scatter_points) {
      plot_scatter_points(scatter_points[k], k, correlations[k]);
      //console.log(correlations[k]);s
   }
}

function plot_scatter_points(data, ck, correlation_point){
   
   var ids_ = ck.split(',')
   id_ = ids_[0]+ids_[1]
    
   $div = "<div class='scatterplot_block' id="+id_+"></div>";
   $('.scatterpoints').append($div);
    
   $('#'+id_).highcharts({
      credits: {
              enabled: false
          },
      chart: {
          type: 'scatter',
          zoomType: 'xy'
      },
      title: {
          text: 'Comparison - '+id_
      },
      subtitle: {
          text: 'Correlation Coefficient: '+correlation_point
      },
      xAxis: {
          title: {
              enabled: true,
              text: ids_[0]
          },
          startOnTick: true,
          endOnTick: true,
          showLastLabel: true
      },
      yAxis: {
          title: {
              text: ids_[1]
          }
      },
      legend: {
          layout: 'vertical',
          align: 'left',
          verticalAlign: 'top',
          x: 100,
          y: 70,
          floating: true,
          backgroundColor: '#EFEFEF',
          borderWidth: 1
      },
      plotOptions: {
          scatter: {
              marker: {
                  radius: 3,
                  states: {
                      hover: {
                          enabled: true,
                          lineColor: 'rgb(100,100,100)'
                      }
                  }
              },
              states: {
                  hover: {
                      marker: {
                          enabled: false
                      }
                  }
              },
              tooltip: {
                  headerFormat: '<b>{series.name}</b><br>',
                  pointFormat: '({point.x}, {point.y})'
              }
          }
      },
      series: [{
          name: id_,
          color: 'rgb(223, 101, 101)',
          data: data
    }]
   });
    
    
    
}
