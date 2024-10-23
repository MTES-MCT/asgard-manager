import QtCharts 2.2
import QtQuick 2.11
ChartView {
   id: chartview
   width: 909
   height: 496
   antialiasing: true
   title: 'Pourcentage du volume des bases de données'
   titleColor: 'black'
   backgroundColor: '#FFFFFF'
   animationOptions: ChartView.AllAnimations
   localizeNumbers : true
   legend.labelColor: 'black'
   legend.visible: true
   legend.alignment: Qt.AlignTop
   legend.font: QFont('Arial', 14)

   Image {                                 
      source: "../icons/logo/logoqml.png"       
      x: 0; y: 0                          
      width: 116; height: 47             
     }                                       
   PieSeries {
      id: pieSeries
      name: 'Noms'
      size: 0.7                                  
      holeSize: 0.15                                  
      onDoubleClicked: {                                                              
          for ( var i = 0; i < pieSeries.count; i++ ) {                                   
              if (pieSeries.at(i).exploded == false)                                                             
                 pieSeries.at(i).exploded = true                                            
              else                                                             
                 pieSeries.at(i).exploded = false                                            
              }                                                                     
                }                                                               
      PieSlice { label: '<center>base_demo</center>'; value: 46.695                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true; exploded : true ; color : '#958B62'                          ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>base_geomatique</center>'; value: 39.855                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true                          ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>plume_rec</center>'; value: 33.178                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true                          ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>geobase_snum</center>'; value: 32.712                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true                          ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>Base_SansAsgard_SansPlume</center>'; value: 31.597                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true                          ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>base_leslie</center>'; value: 22.807                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true                          ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>postgis_31_sample</center>'; value: 21.39                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true                          ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>postgres</center>'; value: 8.119                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true                          ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
   }
}
