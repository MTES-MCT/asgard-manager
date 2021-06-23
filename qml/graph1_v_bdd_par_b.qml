import QtCharts 2.2
import QtQuick 2.11
ChartView {
   id: chartview
   width: 870
   height: 460
   antialiasing: true
   title: 'Pourcentage par bloc du volume de la base de données Asgard'
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
      axisX: BarCategoryAxis  { categories: ['Autres', 'BLOC Non référencé (T)', 'Administration', 'Données extérieures', 'Corbeille', 'Géostandards', 'Consultation', 'Données travail', 'Données confidentielles', 'BLOC Non référencé (Y)', 'Référentiels', 'Données thématiques']}
      labelsVisible : true
      labelsPosition : AbstractBarSeries.LabelsInsideEnd 
      BarSet { label: '<center>Autres</center>'; values: [75.79, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];color : '#808080'}
      BarSet { label: '<center>BLOC Non référencé (T)</center>'; values: [0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];color : '#808080'}
      BarSet { label: '<center>Administration</center>'; values: [0, 0, 4.6, 0, 0, 0, 0, 0, 0, 0, 0, 0];color : '#7d4e5b'}
      BarSet { label: '<center>Données extérieures</center>'; values: [0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0];color : '#00ac8c'}
      BarSet { label: '<center>Corbeille</center>'; values: [0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0];color : '#958b62'}
      BarSet { label: '<center>Géostandards</center>'; values: [0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0];color : '#fdcf41'}
      BarSet { label: '<center>Consultation</center>'; values: [0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0];color : '#ff8d7e'}
      BarSet { label: '<center>Données travail</center>'; values: [0, 0, 0, 0, 0, 0, 0, 19.61, 0, 0, 0, 0];color : '#ff9940'}
      BarSet { label: '<center>Données confidentielles</center>'; values: [0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0];color : '#484d7a'}
      BarSet { label: '<center>BLOC Non référencé (Y)</center>'; values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0];color : '#808080'}
      BarSet { label: '<center>Référentiels</center>'; values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0];color : '#91ae4f'}
      BarSet { label: '<center>Données thématiques</center>'; values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0];color : '#ff0000'}
   }
}
