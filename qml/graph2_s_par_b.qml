import QtCharts 2.0
import QtQuick 2.4
ChartView {
   width: 831
   height: 476
   antialiasing: true
   title: 'Ventilation des schémas <b>ACTIFS</b> par blocs : <b>geobase_snum</b>'
   titleColor: 'black'
   backgroundColor: '#FFFFFF'
   animationOptions: ChartView.AllAnimations
   legend.visible: false
      PieSeries {                                                                  
          id: pieIn                                                               
          size: 0.5                                  
          holeSize: 0.15                                  
          PieSlice { label : "<center>Consultation</center>"; value : 6; color : '#958b62' } 
          PieSlice { label : "<center>Référentiels</center>"; value : 3; color : '#91ae4f' } 
          PieSlice { label : "<center>Géostandards</center>"; value : 10; color : '#fdcf41' } 
          PieSlice { label : "<center>Administration</center>"; value : 3; color : '#7d4e5b' } 
      }                                                                           
      PieSeries {                                                                 
          id: pieOut                                                              
          size:       0.7                                   
          holeSize:   0.5                                   
          PieSlice { label : "c_agence_urba"; value : 1; color : '#ffaa00' } 
          PieSlice { label : "c_agri_environnement"; value : 1; color : '#ffaa00' } 
          PieSlice { label : "c_foret_gestion"; value : 1; color : '#ffaa00' } 
          PieSlice { label : "c_premier"; value : 1; color : '#ffaa00' } 
          PieSlice { label : "c_risque_minier"; value : 1; color : '#ffaa00' } 
          PieSlice { label : "c_Urba_travaux"; value : 1; color : '#ffaa00' } 
          PieSlice { label : "r_nouveau_schema"; value : 1; color : '#e4ebd3' } 
          PieSlice { label : "r_Referentiel_Urba"; value : 1; color : '#e4ebd3' } 
          PieSlice { label : "r_toto"; value : 1; color : '#e4ebd3' } 
          PieSlice { label : "s_agri_exploi_elevage"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_Dernier_Test"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_didier"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_infra_toto"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_Mon Standard"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_nouveau_schema"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_premier_22"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_titi"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_toto"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "s_tototiti"; value : 1; color : '#fff3d0' } 
          PieSlice { label : "z_asgard"; value : 1; color : '#bea7ad' } 
          PieSlice { label : "z_asgard_admin"; value : 1; color : '#bea7ad' } 
          PieSlice { label : "z_replique"; value : 1; color : '#bea7ad' } 
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
