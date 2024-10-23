import QtCharts 2.0
import QtQuick 2.4
ChartView {
   width: 839
   height: 471
   antialiasing: true
   title: 'Ventilation des schémas <b>ACTIFS</b> par blocs : <b>base_demo</b>'
   titleColor: 'black'
   backgroundColor: '#FFFFFF'
   animationOptions: ChartView.AllAnimations
   legend.labelColor: 'black'
   legend.visible: true
   legend.alignment: Qt.AlignTop
   legend.font: QFont('Arial', 14)

      PieSeries {                                                                  
          id: pieIn                                                               
          size: 0.5                                  
          holeSize: 0.15                                  
          PieSlice { label : "<center>Autres</center>"; value : 1; color : '#808080' } 
          PieSlice { label : "<center>Consultation</center>"; value : 2; color : '#ff8d7e' } 
          PieSlice { label : "<center>Données extérieures</center>"; value : 1; color : '#00AC8C' } 
          PieSlice { label : "<center>Données thématiques</center>"; value : 1; color : '#5770BE' } 
          PieSlice { label : "<center>Référentiels</center>"; value : 3; color : '#91ae4f' } 
          PieSlice { label : "<center>Géostandards</center>"; value : 1; color : '#fdcf41' } 
          PieSlice { label : "<center>Données travail</center>"; value : 1; color : '#ff9940' } 
          PieSlice { label : "<center>Administration</center>"; value : 4; color : '#7D4E5B' } 
      }                                                                           
      PieSeries {                                                                 
          id: pieOut                                                              
          size:       0.7                                   
          holeSize:   0.5                                   
          PieSlice { label : "travail"; value : 1; color : '#bfbfbf' } 
          PieSlice { label : "c_agri_agroalimentaire"; value : 1; color : '#ffe3df' } 
          PieSlice { label : "c_agri_exploi_elevage"; value : 1; color : '#ffe3df' } 
          PieSlice { label : "e_amgt_urb_zon_amgt"; value : 1; color : '#bfeae2' } 
          PieSlice { label : "p_OA"; value : 1; color : '#d5dbef' } 
          PieSlice { label : "r_adl_administration"; value : 1; color : '#e4ebd3' } 
          PieSlice { label : "r_admin_express"; value : 1; color : '#e4ebd3' } 
          PieSlice { label : "r_eurostat"; value : 1; color : '#e4ebd3' } 
          PieSlice { label : "s_cadastre_etalab"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "w_test_combo"; value : 1; color : '#ffe6cf' } 
          PieSlice { label : "z_asgard"; value : 1; color : '#bea7ad' } 
          PieSlice { label : "z_asgard_admin"; value : 1; color : '#bea7ad' } 
          PieSlice { label : "z_plume"; value : 1; color : '#bea7ad' } 
          PieSlice { label : "z_plume_recette"; value : 1; color : '#bea7ad' } 
      }                                                                           
   Component.onCompleted: {                                       
   for (var i = 0; i < pieOut.count; i++) {                     
       pieOut.at(i).labelPosition = PieSlice.LabelOutside;      
       pieOut.at(i).labelVisible = true;                        
       pieOut.at(i).borderWidth = 3;                            
   }                                                              
   for (var i = 0; i < pieIn.count; i++) {                     
       pieIn.at(i).labelPosition = PieSlice.LabelInsideNormal; 
       pieIn.at(i).labelVisible = true;                        
       pieIn.at(i).borderWidth = 2;                            
   }                                                              
   }                                                              
}
