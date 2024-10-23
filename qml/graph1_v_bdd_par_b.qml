import QtCharts 2.2
import QtQuick 2.11
ChartView {
   id: chartview
   width: 1035
   height: 566
   antialiasing: true
   title: 'Pourcentage par bloc du volume de la base de données Asgard'
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
      PieSlice { label: '<center>Autres</center>'; value: 11.018                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true ;color : '#808080'                         ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>Administration</center>'; value: 0.696                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true ;color : '#7D4E5B'                         ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>Géostandards</center>'; value: 0.0                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true ;color : '#fdcf41'                         ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>Données travail</center>'; value: 1.032                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true ;color : '#ff9940'                         ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>Consultation</center>'; value: 0.18                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true ;color : '#ff8d7e'                         ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>Référentiels</center>'; value: 11.321                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true ;color : '#91ae4f'                         ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
      PieSlice { label: '<center>Données thématiques</center>'; value: 0.0                          ; labelPosition : PieSlice.LabelOutside ;labelVisible : true ;color : '#5770BE'                         ; onClicked: { if (exploded == false)                                                 {exploded = true }                                              else                                                 {exploded = false }                                       }                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }                                                       }
   }
}
