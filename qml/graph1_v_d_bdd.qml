import QtCharts 2.2
import QtQuick 2.11
ChartView {
   id: chartview
   width: 870
   height: 460
   antialiasing: true
   title: 'Pourcentage du volume des bases de données'
   titleColor: 'black'
   backgroundColor: '#FFFFFF'
   animationOptions: ChartView.AllAnimations
   localizeNumbers : true
   legend.visible: false
   Image {                                 
      source: "../icons/logo/logoqml.png"       
      x: 0; y: 0                          
      width: 116; height: 47             
     }                                       
   anchors.fill: parent

   StackedBarSeries {
      id: barSeries
      axisX: BarCategoryAxis  { categories: ['base_geomatique', 'geobase_snum', 'base_leslie', 'postgis_31_sample', 'postgres']}
      axisY: ValueAxis { min: 0;max: 100; tickCount: 5  } 
      labelsVisible : true
      labelsPosition : AbstractBarSeries.LabelsInsideEnd 
      BarSet { label: '<center>base_geomatique<br><b>33.79 %</b></center>'; values: [33.79, 0, 0, 0, 0]}
      BarSet { label: '<center>geobase_snum<br><b>20.3 %</b></center>'; values: [0, 20.3, 0, 0, 0]; color : '#958B62' }
      BarSet { label: '<center>base_leslie<br><b>19.53 %</b></center>'; values: [0, 0, 19.53, 0, 0]}
      BarSet { label: '<center>postgis_31_sample<br><b>19.16 %</b></center>'; values: [0, 0, 0, 19.16, 0]}
      BarSet { label: '<center>postgres<br><b>7.22 %</b></center>'; values: [0, 0, 0, 0, 7.22]}
   }
}
